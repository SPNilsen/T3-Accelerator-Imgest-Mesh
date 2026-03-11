# **Documentation of Chosen Frameworks and Algorithms**

## **Introduction**

For the Modeling Phase of Project ARMOR, the selection of frameworks and
algorithms is guided by the need to develop robust solutions for two distinct
tasks:

1. **Binary Classifier (Lens Presentation)**: A monolithic model for pass/fail
   classification of lenses.
2. **Defect-Specific Models**: Individual models targeting specific defect types
   such as edge chips, bubble scatter, and center tears.

The chosen frameworks and algorithms are optimized for scalability, precision,
and compatibility with the project’s objectives, leveraging both GPU
acceleration and cutting-edge research.

---

## **Frameworks**

### **Summary of Frameworks for Consideration**

| **Framework**       | **Key Focus**                     | **COCO Support** | **Best Use Case**                                                  | **GPU Optimization** |
|----------------------|-----------------------------------|------------------|--------------------------------------------------------------------|-----------------------|
| **Detectron2**       | Object Detection & Segmentation  | Native           | Advanced research and object detection tasks                      | Excellent             |
| **MMDetection**      | Modular Object Detection         | Native           | Highly customizable object detection pipelines                    | Excellent             |
| **YOLOv8**           | Real-Time Object Detection       | Native           | Fast, real-time defect detection                                   | Excellent             |
| **OpenVINO**         | Inference Acceleration           | Conversion       | Edge-based defect detection with optimized models                 | Good                  |
| **TensorFlow Object Detection** | Production Object Detection | Native           | Production-ready pipelines for TensorFlow models                  | Excellent             |
| **FastSAM**          | Generalized Segmentation         | Partial          | Rapid segmentation without extensive retraining                   | Good                  |
| **MONAI**            | Segmentation & Medical Imaging   | Customizable     | Pixel-level defect detection requiring precision                  | Excellent             |
| **Keras**            | Simplified Deep Learning         | Partial          | Rapid prototyping and model experimentation                       | Good                  |
| **PyTorch**          | General Deep Learning            | Native           | Research-focused model development and custom architectures       | Excellent             |
| **DeepLab**          | Semantic Image Segmentation      | Partial          | Specialized for high-precision segmentation tasks                 | Excellent             |


### **Binary Classifier**
The binary classifier for lens presentation focuses on high-speed classification
with a focus on maintaining compatibility with production environments.

#### **Frameworks**

- **TensorFlow Object Detection**:
    - **Why Chosen**: Production-ready pipelines, strong ecosystem, and high compatibility with real-world deployment.
    - **Advantages**:
        - Extensive pre-trained models for transfer learning.
        - Strong TensorBoard support for visualization and debugging.
        - Scalable for high-throughput environments.
- **YOLOv8**:
    - **Why Chosen**: Extremely fast inference time, making it ideal for real-time production systems.
    - **Advantages**:
        - Lightweight and highly efficient.
        - Easy integration with existing workflows.
        - High performance for binary tasks.
- **Keras**:
    - **Why Chosen**: Simplifies rapid prototyping and experimentation.
    - **Advantages**:
        - High-level API for TensorFlow.
        - Fast implementation and testing for simpler tasks.


### **Defect-Specific Models**
Defect-specific models require precision and adaptability to classify and detect
multiple defect types. These models leverage frameworks designed for modularity
and advanced segmentation.

#### **Frameworks**
- **Detectron2**:
    - **Why Chosen**: State-of-the-art performance for object detection and segmentation.
    - **Advantages**:
        - Highly modular and customizable.
        - Strong pre-trained model library for transfer learning.
        - Excellent support for COCO-format annotations.
- **MMDetection**:
    - **Why Chosen**: Designed for modular object detection pipelines with high customization.
    - **Advantages**:
        - Easy configuration for defect-specific tasks.
        - Seamless integration with various datasets and metrics.
- **MONAI**:
    - **Why Chosen**: Tailored for medical imaging tasks requiring pixel-level precision.
    - **Advantages**:
        - Excellent for fine-grained segmentation.
        - Built-in support for advanced data augmentation and preprocessing.
- **DeepLab**:
    - **Why Chosen**: Highly effective for semantic segmentation tasks.
    - **Advantages**:
        - Specialized for detailed segmentation patterns.
        - Strong performance in low-contrast image analysis.

---

## **Algorithms**

### **Binary Classifier**
- **Algorithm**: Convolutional Neural Networks (CNNs)
    - **Reason**: Effective for image classification tasks with high accuracy and speed.
    - **Implementation**: Transfer learning with pre-trained models such as EfficientNet or ResNet.
    - **Metrics**: Precision, recall, F1 score, and ROC-AUC.

### **Defect-Specific Models**
- **Object Detection**:
    - Algorithms: Faster R-CNN, YOLOv8
    - **Reason**: Balances speed and accuracy for detecting specific defects.
    - **Implementation**: Region-based object detection and single-shot detection.
    - **Metrics**: mAP (mean Average Precision) for defect-specific bounding boxes.

- **Segmentation**:
    - Algorithms: Mask R-CNN, U-Net, DeepLabv3+
    - **Reason**: Effective for precise segmentation of defects like edge tears or center debris.
    - **Implementation**: Pixel-level annotation and segmentation pipelines.
    - **Metrics**: IoU (Intersection over Union), Dice coefficient.

---

## **Modeling Assumptions**

- The input images are well-annotated and accurately represent defect types.
- Transfer learning can accelerate training and improve accuracy for limited datasets.
- GPU acceleration is available for all frameworks to optimize training and inference.
- COCO-format annotations are consistent and compatible with the selected frameworks.

