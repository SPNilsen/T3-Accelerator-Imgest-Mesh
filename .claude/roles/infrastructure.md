# Role Profile — Infrastructure

## Scope in this project
Kubernetes / OpenShift platform, GPU scheduling, networking for the demo target.

## Target platform
**Cisco AI Pod** with:
- NVIDIA GPU-accelerated compute nodes
- High-performance storage + high-bandwidth networking
- Red Hat OpenShift orchestration
- Integrated registry, RBAC, Routes

## Portability targets
- Vanilla Kubernetes (any cloud/on-prem)
- NVIDIA GPU infrastructure
- HPC clusters (SLURM + K8s hybrid — see `docs/hpc/`)

## Considerations
- GPU operator + device-plugin for NVIDIA
- Route vs Ingress (OpenShift-specific vs portable)
- Image pull secrets for GitLab registry
- Pod security (Alpine nginx-unprivileged already aligns with OpenShift's restricted SCC)
