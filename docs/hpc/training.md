Training
========


This outlines the training sessions as planned for the cluster operations team,
including associated materials. This page will be updated as the sessions occur.

### **Videos**

Here are the videos we recorded for miscellaneous training. They will be tagged
where appropriate.

**Session 1: High Level Overview and Introduction to Documentation**

[Recording](http://link.to.recording.mp4)

---

### **Session 1: Introduction to the AS-Built HPC Cluster: Architecture and Capabilities**

This introductory session provides a comprehensive overview of the newly built HPC cluster featuring NVIDIA DGX-2 GPU systems, designed to accelerate data science and AI workflows. The session begins with a review of the AS-Built documentation, including detailed descriptions of the hardware and software configurations, network topology, and storage solutions. Attendees will explore architectural diagrams that visualize the cluster's components, connections, and data flow, offering insights into its overall design and capabilities.

The session will also introduce Kubernetes, the orchestration platform installed on the cluster, covering its role in managing containerized workloads, ensuring scalability, and maintaining high availability. Key Kubernetes concepts such as pods, services, and deployments will be explained, laying the foundation for deeper exploration in subsequent sessions.

Participants will gain an understanding of the cluster's infrastructure, the rationale behind design decisions, and how Kubernetes fits into the broader system architecture. This session will set the stage for leveraging the full potential of the HPC cluster in advanced AI and data science projects.

### **Session 2: Managing and Orchestrating Workloads with Kubernetes on DGX-2 Systems**

This session delves into the practical aspects of managing and orchestrating workloads on the DGX-2 systems using Kubernetes. Participants will learn how to deploy, monitor, and scale containerized applications in the HPC environment, leveraging Kubernetes to optimize resource utilization and maintain operational efficiency.

The session will cover key Kubernetes components, including nodes, pods, services, and namespaces, and how they interact within the cluster. Attendees will also explore best practices for creating and managing Kubernetes manifests, configuring resource requests and limits, and implementing scheduling strategies tailored to high-performance workloads.

Through hands-on exercises, participants will gain experience in deploying AI and data science workloads, using Kubernetes’ built-in tools for monitoring and troubleshooting. By the end of this session, attendees will be equipped with the knowledge and skills needed to efficiently manage and orchestrate complex workloads on the DGX-2 systems.

### **Session 3: Scaling AI and Machine Learning Workflows with Kubeflow**

This session focuses on Kubeflow, the Kubernetes-native platform designed to simplify the deployment, scaling, and management of machine learning (ML) workflows on the DGX-2 cluster. Participants will learn how to leverage Kubeflow’s comprehensive suite of tools to build, train, and deploy ML models at scale, harnessing the full power of the DGX-2 systems.

The session will cover key components of Kubeflow, including Pipelines, Katib for hyperparameter tuning, and KFServing for model serving. Attendees will explore how these tools integrate with Kubernetes to automate and streamline the entire ML lifecycle, from data preparation to model deployment.

Through guided examples, participants will gain hands-on experience in setting up and managing Kubeflow pipelines, optimizing model performance, and monitoring ML workflows. By the end of this session, attendees will understand how to scale AI and ML projects effectively, maximizing the capabilities of the HPC cluster.

### **Session 4: Optimizing Data Science Pipelines: Best Practices on DGX-2**

In this session, participants will explore strategies and best practices for optimizing data science pipelines on the DGX-2 cluster. The focus will be on enhancing performance, reducing latency, and improving the efficiency of data processing and model training workflows.

Attendees will learn about the unique capabilities of DGX-2 systems, including multi-GPU parallelism, NVLink interconnects, and how to leverage these features to accelerate data science workloads. The session will also cover techniques for optimizing data pipelines, such as efficient data loading, preprocessing, and distribution across GPUs.

Real-world examples and case studies will be presented to illustrate how these best practices can be applied to common data science challenges. By the end of this session, participants will have a deeper understanding of how to fine-tune their data science pipelines to fully exploit the DGX-2’s performance potential.

### **Session 5: Advanced Resource Management and Scheduling with Run:AI**

The final session in this series focuses on advanced resource management and scheduling techniques using Run:AI, a platform designed to optimize GPU utilization in AI and data science workloads. Participants will learn how Run:AI integrates with Kubernetes to provide dynamic resource allocation, job scheduling, and workload prioritization, ensuring maximum efficiency on the DGX-2 cluster.

The session will cover key Run:AI features, including fractional GPU allocation, GPU over-subscription, and intelligent job scheduling. Attendees will explore how these capabilities enable more flexible and efficient use of GPU resources, reducing idle time and accelerating time-to-completion for AI projects.

Through practical exercises, participants will gain hands-on experience in configuring and managing Run:AI in a production environment, learning how to monitor GPU usage, adjust scheduling policies, and optimize resource allocation dynamically. By the end of this session, attendees will be well-prepared to manage and optimize AI workloads on the DGX-2 cluster using Run:AI’s advanced features.

