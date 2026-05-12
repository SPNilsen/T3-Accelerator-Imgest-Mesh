# Project ARMOR Models

This page, layout, and possibly even existence may change as this project
evolves. For now, the "deliverables" or Outputs will be contained within the
CRISP-DM pages. This project may dictate a change in that layout as it
progresses...



???- success "Logic Engine -  Notebook run/results - 2/18"
    [Download PDF](/armor/annotation-logic-notebook.pdf)

    ![Annotation Logic Notebook](<../armor/annotation-logic-notebook.pdf>){type=application/pdf style="min-height:87vh;width:100%"}


???- example "Baseline Multi-Input CNN Dev Report 2/14"

    _**NOTE**: These were first pass non-considered models, demonstrating process flow._

    | Model | size | version | notes |
    |-------|------|---------|-------|
    | [Trained H5 Model](/armor/baseline-multi‑input-cnn.h5) | 169MiB | 1.1 | initial pipeline established |
    | [Trained Tflite Model](/armor/baseline-multi‑input-cnn.h5) | 14MiB | 1.3 | |


???- example "Model Development Report 2/14"

    _**NOTE**: This R report was early process flow...switching to Python obfuscated the need for this report._

    ![Image Classification Model Development Report for Baseline Multi‑Input CNN](<../armor/baseline-multi-input-cnn.pdf>){type=application/pdf style="min-height:87vh;width:100%"}



???- success "Stage1 modeling work"
    | Model | size | version | notes |
    |-------|------|---------|-------|
    | [Trained Monolithic Model](/armor/stg1/stg1_best.pt) | 43MiB | YourTimeIsGonnaCome | stg1 development at pause for stg2 |
    | [Stage1 GPU Metrics](/armor/stg1/stg1_gpu_metrics.csv) | 30KiB | n/a | GPU specifics |
    | [Stage1 Test Images](/armor/stg1/stg1_test_images.txt) | 103KiB | n/a | Test Images list |
    | [Stage1 Missing Files](/armor/stg1/stg1_missing_files_0.txt) | 223B | n/a | Missing Files list |
    | [Stage1 Epoch Metrics](/armor/stg1/stg1_epoch_metrics_0.json) | 1.9KiB | n/a | Epoch metrics |

    ![Stage1 Training Report](<../armor/stg1/train-rprt.pdf>){type=application/pdf style="min-height:87vh;width:100%"}


???- success "Stage2 Computer Vision modeling work"
    ![Roboflow results](./stg2/17.24.47.png)
    ![Roboflow results](./stg2/17.25.43.png)

    ----
    To run the code base:

    - Recommend creating a virtual python environment and activating
    - run pip install inference-sdk
    - place images in the same directory as the code base
    - copy over the code base below
    - run the program

    [Roboflow Codebase for inferencing](/armor/stg2/roboflow-codebase.py)

    [Roboflow Video for inferencing](/armor/stg2/roboflow-run.mp4) 67MiB
