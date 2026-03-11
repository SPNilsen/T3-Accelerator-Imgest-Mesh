from pathlib import Path
from datetime import datetime


def emit_placeholder_frame(output_dir: str, filename_prefix: str, frame_number: int) -> str:
    outdir = Path(output_dir)
    outdir.mkdir(parents=True, exist_ok=True)

    filename = f"{filename_prefix}-{frame_number:05d}.txt"
    path = outdir / filename

    content = (
        f"demo frame {frame_number}\n"
        f"created: {datetime.utcnow().isoformat()}Z\n"
    )

    path.write_text(content, encoding="utf-8")
    return str(path)