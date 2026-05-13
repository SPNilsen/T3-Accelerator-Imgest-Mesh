"""
One-shot model conversion: Detectron2 .pt  ->  ONNX  ->  TensorRT engine

Run on a CUDA-capable machine that has the model weights available:

    python resources/inference/scripts/convert_model.py \
        --model-path /path/to/lens_defect.pt \
        --output-dir resources/inference/models/

Requirements (install separately on the conversion host — not in the
inference container's base requirements.txt):
    pip install torch torchvision detectron2 onnx onnxruntime tensorrt pycuda

The script is intentionally not imported at container start — it is a
developer/ops utility. The .engine output is what the inference container
loads at runtime.
"""

import argparse
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Detectron2 -> ONNX
# ---------------------------------------------------------------------------

def export_to_onnx(model_path: Path, output_path: Path, input_h: int, input_w: int) -> Path:
    import torch
    import onnx
    from detectron2.config import get_cfg
    from detectron2 import model_zoo
    from detectron2.engine import DefaultPredictor
    from detectron2.export import TracingAdapter

    print(f"[1/3] Loading Detectron2 model from {model_path} ...")

    cfg = get_cfg()
    cfg.merge_from_file(
        model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml")
    )
    cfg.MODEL.WEIGHTS = str(model_path)
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
    cfg.MODEL.DEVICE = "cuda" if _cuda_available() else "cpu"
    # Input size must match what the model was trained on — override if different
    cfg.INPUT.MIN_SIZE_TEST = input_h
    cfg.INPUT.MAX_SIZE_TEST = input_w

    predictor = DefaultPredictor(cfg)
    model = predictor.model
    model.eval()

    # Dummy input: NCHW float32, values in [0, 255]
    dummy = torch.zeros(1, 3, input_h, input_w, dtype=torch.float32)
    if cfg.MODEL.DEVICE == "cuda":
        dummy = dummy.cuda()

    print(f"[1/3] Tracing model with dummy input shape {list(dummy.shape)} ...")

    # Wrap via TracingAdapter so Detectron2's pre/post-processing is captured
    inputs = [{"image": dummy[0]}]
    adapter = TracingAdapter(model, inputs, allow_non_tensor_inputs=True)
    adapter.eval()

    with torch.no_grad():
        torch.onnx.export(
            adapter,
            (dummy,),
            str(output_path),
            opset_version=16,
            input_names=["image"],
            output_names=["boxes", "scores", "labels"],
            dynamic_axes={
                "image":  {0: "batch", 2: "height", 3: "width"},
                "boxes":  {0: "num_detections"},
                "scores": {0: "num_detections"},
                "labels": {0: "num_detections"},
            },
            verbose=False,
        )

    print(f"[1/3] Validating ONNX graph ...")
    model_onnx = onnx.load(str(output_path))
    onnx.checker.check_model(model_onnx)
    print(f"[1/3] ONNX export OK  ->  {output_path}  ({output_path.stat().st_size / 1e6:.1f} MB)")
    return output_path


# ---------------------------------------------------------------------------
# ONNX -> TensorRT engine
# ---------------------------------------------------------------------------

def export_to_trt(onnx_path: Path, engine_path: Path, fp16: bool = True, workspace_gb: int = 4) -> Path:
    import tensorrt as trt

    print(f"[2/3] Converting ONNX -> TensorRT engine (fp16={fp16}, workspace={workspace_gb} GB) ...")

    TRT_LOGGER = trt.Logger(trt.Logger.WARNING)
    builder = trt.Builder(TRT_LOGGER)
    network = builder.create_network(1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH))
    parser = trt.OnnxParser(network, TRT_LOGGER)

    with open(onnx_path, "rb") as f:
        if not parser.parse(f.read()):
            for i in range(parser.num_errors):
                print(f"  ONNX parse error: {parser.get_error(i)}", file=sys.stderr)
            raise RuntimeError("ONNX parsing failed — see errors above")

    config = builder.create_builder_config()
    config.set_memory_pool_limit(trt.MemoryPoolType.WORKSPACE, workspace_gb * (1 << 30))

    if fp16 and builder.platform_has_fast_fp16:
        config.set_flag(trt.BuilderFlag.FP16)
        print("[2/3] FP16 precision enabled")
    else:
        print("[2/3] FP16 not available — falling back to FP32")

    # Optimization profile for dynamic shapes
    profile = builder.create_optimization_profile()
    inp = network.get_input(0)
    # min / opt / max batch=1, spatial dims match training resolution
    h, w = inp.shape[2], inp.shape[3]
    profile.set_shape(inp.name, (1, 3, h, w), (1, 3, h, w), (1, 3, h, w))
    config.add_optimization_profile(profile)

    print("[2/3] Building engine (this may take several minutes on first run) ...")
    serialized = builder.build_serialized_network(network, config)
    if serialized is None:
        raise RuntimeError("TensorRT engine build failed")

    with open(engine_path, "wb") as f:
        f.write(serialized)

    size_mb = engine_path.stat().st_size / 1e6
    layer_count = network.num_layers
    print(f"[2/3] Engine written  ->  {engine_path}  ({size_mb:.1f} MB, {layer_count} layers)")
    return engine_path


# ---------------------------------------------------------------------------
# Smoke test
# ---------------------------------------------------------------------------

def smoke_test(engine_path: Path, input_h: int, input_w: int) -> None:
    import numpy as np
    import tensorrt as trt
    import pycuda.driver as cuda
    import pycuda.autoinit  # noqa: F401 — initialises CUDA context

    print("[3/3] Smoke-testing engine ...")
    TRT_LOGGER = trt.Logger(trt.Logger.WARNING)
    runtime = trt.Runtime(TRT_LOGGER)

    with open(engine_path, "rb") as f:
        engine = runtime.deserialize_cuda_engine(f.read())

    context = engine.create_execution_context()
    dummy = np.zeros((1, 3, input_h, input_w), dtype=np.float32)
    d_input = cuda.mem_alloc(dummy.nbytes)
    cuda.memcpy_htod(d_input, dummy)

    # Allocate outputs (generous fixed sizes for detection outputs)
    d_boxes  = cuda.mem_alloc(4 * 4 * 1000)   # max 1000 detections
    d_scores = cuda.mem_alloc(4 * 1000)
    d_labels = cuda.mem_alloc(4 * 1000)

    context.execute_v2([int(d_input), int(d_boxes), int(d_scores), int(d_labels)])
    print("[3/3] Smoke test passed — engine executes without error")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _cuda_available() -> bool:
    try:
        import torch
        return torch.cuda.is_available()
    except ImportError:
        return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert Detectron2 .pt model to TensorRT engine")
    parser.add_argument("--model-path",  required=True, help="Path to the trained .pt weights file")
    parser.add_argument("--output-dir",  default="resources/inference/models/", help="Directory for output files")
    parser.add_argument("--input-height", type=int, default=800, help="Model input height in pixels (default: 800)")
    parser.add_argument("--input-width",  type=int, default=800, help="Model input width in pixels (default: 800)")
    parser.add_argument("--no-fp16",     action="store_true", help="Disable FP16 — use FP32 precision")
    parser.add_argument("--workspace-gb", type=int, default=4, help="TensorRT workspace size in GB (default: 4)")
    parser.add_argument("--skip-smoke-test", action="store_true", help="Skip engine smoke test")
    args = parser.parse_args()

    model_path = Path(args.model_path)
    if not model_path.exists():
        print(f"ERROR: model file not found: {model_path}", file=sys.stderr)
        sys.exit(1)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    stem = model_path.stem
    onnx_path   = output_dir / f"{stem}.onnx"
    engine_path = output_dir / f"{stem}.engine"

    onnx_path   = export_to_onnx(model_path, onnx_path, args.input_height, args.input_width)
    engine_path = export_to_trt(onnx_path, engine_path, fp16=not args.no_fp16, workspace_gb=args.workspace_gb)

    if not args.skip_smoke_test:
        smoke_test(engine_path, args.input_height, args.input_width)

    print(f"\nConversion complete.")
    print(f"  ONNX   : {onnx_path}")
    print(f"  Engine : {engine_path}")
    print(f"\nSet MODEL_ENGINE_PATH={engine_path} in the inference container.")


if __name__ == "__main__":
    main()
