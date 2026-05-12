# Role Profile — DevOps

## Scope in this project
Container build + deployment automation:
- Containerfiles under `resources/{camera,inference,orchestrator,webserver}/`
- K8s/OpenShift manifests under `resources/k8s/`
- Image registry: `registry.gitlab.com/dosayles/t3-imgest-mesh/*`

## Current state
- **webserver** is the only service with K8s manifests (Deployment, Service, Route)
- Uses Alpine nginx-unprivileged on port 8080
- OpenShift Route (no TLS yet)
- No CI/CD pipeline file checked in — GitLab runner implied

## Gaps to fill
- camera/orchestrator/inference need manifests
- No docker-compose for local dev
- No ImageStream/BuildConfig if going native OpenShift
- TLS on the Route for production demo
