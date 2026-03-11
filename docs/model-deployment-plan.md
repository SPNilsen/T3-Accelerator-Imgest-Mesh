# Model Deployment: Generative Model on GCP Vertex AI

## Overview
This document outlines the steps to deploy a generative AI model using GCP
Vertex AI. The process involves setting up the GCP environment, uploading the
model to Vertex AI Model Registry, and creating an endpoint for serving
predictions.

---

## Steps to Deploy the Model

### 1. **Setup Environment**
1. Authenticate with GCP:
    ```bash
    gcloud auth login
    gcloud config set project [PROJECT_ID]
    ```
2. Confirm necessary APIs are enabled:
    ```bash
    gcloud services enable aiplatform.googleapis.com storage.googleapis.com
    ```

---

### 2. **Prepare Model Artifact**
1. Save the trained model locally or export it from the training script.
2. Upload the model artifact to a Cloud Storage bucket:
    ```bash
    gsutil cp [MODEL_ARTIFACT] gs://[BUCKET_NAME]/[MODEL_PATH]
    ```

---

### 3. **Create Vertex AI Model**
1. Define the model specifications:
    - **Model Framework**: TensorFlow, PyTorch, Scikit-learn, etc.
    - **Container Image**: Prebuilt serving containers from Vertex AI or a custom container.
2. Use the following CLI command to register the model:
    ```bash
    gcloud ai models upload \
      --region=us-central1 \
      --display-name="[MODEL_NAME]" \
      --container-image-uri=[SERVING_IMAGE_URI] \
      --artifact-uri=gs://[BUCKET_NAME]/[MODEL_PATH]
    ```

---

### 4. **Deploy Model to Endpoint**
1. Create a Vertex AI endpoint:
    ```bash
    gcloud ai endpoints create \
      --region=us-central1 \
      --display-name="[ENDPOINT_NAME]"
    ```
2. Deploy the model to the endpoint:
    ```bash
    gcloud ai endpoints deploy-model [ENDPOINT_ID] \
      --model=[MODEL_ID] \
      --region=us-central1 \
      --machine-type="n1-standard-4"
    ```

---

### 5. **Test the Deployed Model**
Use the Vertex AI Python SDK to test the deployed model:
```python
from google.cloud import aiplatform

endpoint = aiplatform.Endpoint(endpoint_name="[ENDPOINT_NAME]")

response = endpoint.predict(instances=[INPUT_INSTANCE])
print("Prediction:", response.predictions)
```

## Best Practices

- Monitoring: Use Vertex AI Monitoring for prediction drift and latency tracking.
- Scaling: Configure auto-scaling based on traffic patterns.
- Security: Restrict access to endpoints using IAM roles or VPC Service
Controls.

## Troubleshooting

| **Issue**               | **Possible Cause**                   | **Solution**                          |
|--------------------------|---------------------------------------|---------------------------------------|
| Model not uploading      | Incorrect bucket permissions         | Verify IAM roles for the storage bucket. |
| Prediction failure       | Input schema mismatch                | Check the input format and schema.    |
| High latency             | Insufficient machine type or replicas | Upgrade the machine type or add more replicas. |
| Endpoint not reachable   | Endpoint configuration error         | Verify endpoint creation and deployment steps. |
| Model version not found  | Incorrect model ID or version number | Double-check the model ID and version. |


## Next Steps

1.	Integrate the endpoint with your application for real-time or batch predictions.
2.	Explore Vertex AI Experiments for continuous model improvement.
3.	Document usage metrics for further optimization.

## Resources

- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
  Comprehensive guide to using Vertex AI for model development, deployment, and monitoring.

- [Prebuilt Serving Containers](https://cloud.google.com/vertex-ai/docs/predictions/pre-built-containers)
  Details on available serving containers for various frameworks.

- [GCP CLI Reference](https://cloud.google.com/sdk/gcloud/reference)
  Reference documentation for GCP command-line tools.

- [Vertex AI Pricing](https://cloud.google.com/vertex-ai/pricing)
  Information on pricing models for Vertex AI services.

- [Cloud Storage Documentation](https://cloud.google.com/storage/docs)
  Instructions for setting up and managing GCP storage buckets.

- [Vertex AI Monitoring](https://cloud.google.com/vertex-ai/docs/monitoring)
  Overview of monitoring tools for deployed models.



