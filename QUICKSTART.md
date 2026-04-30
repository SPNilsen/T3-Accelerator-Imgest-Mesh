# Imgest-Mesh Quick Start Guide

Get the Imgest-Mesh documentation system and pipeline services running in minutes.

---

## Windows with Docker Desktop

> **For Windows users**, Docker Desktop is the easiest path. The sections below use `lima nerdctl` (macOS/Linux) — swap every `lima nerdctl` with `docker` and every `limactl` command can be skipped entirely.

### Prerequisites (Windows)

- **Docker Desktop for Windows** — [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
  - Enable **WSL 2 backend** during install (recommended over Hyper-V)
  - After install, open Docker Desktop and confirm the whale icon in the system tray shows "Docker Desktop is running"
- **Git for Windows** — [https://git-scm.com/download/win](https://git-scm.com/download/win)
- **Windows Terminal or Git Bash** — for running the commands below
- **8 GB+ RAM** and **5 GB free disk space**

### Verify Docker is Ready (PowerShell or Git Bash)

```powershell
docker --version
docker info
```

Expected: version line and engine info with no errors.

---

### Corporate Proxy / SSL Inspection (Netskope)

If pip installs fail with `CERTIFICATE_VERIFY_FAILED` or `self-signed certificate in certificate chain`, your corporate proxy (e.g. Netskope) is intercepting TLS. Pass `--build-arg SKIP_SSL_VERIFY=true` to any `docker build` command to add `--trusted-host` flags for `pypi.org` and `files.pythonhosted.org`. **Omit this flag in prod/CI.**

```powershell
# Dev (corporate laptop) — bypass SSL verification
docker build --build-arg SKIP_SSL_VERIFY=true -t camera-test -f resources/camera/Containerfile resources/camera

# Prod / CI — default behavior, SSL enforced
docker build -t camera-test -f resources/camera/Containerfile resources/camera
```

---

### Option 1 (Windows): Documentation Server

```powershell
# From the repo root — build the custom MkDocs image
# Add --build-arg SKIP_SSL_VERIFY=true if on a corporate network
docker build -t mkdocs -f resources/mkdocs/Container .

# Run the live-reload dev server
docker run --rm -it -p 8000:8000 -v ${PWD}:/docs:ro squidfunk/mkdocs-material
```

> **PowerShell note:** use `${PWD}` for the current directory. In cmd.exe use `%cd%` instead.

Open **http://localhost:8000** in your browser.

Stop with `Ctrl+C`.

---

### Option 2 (Windows): Pipeline Services (Full Stack)

Open four separate PowerShell/Terminal tabs from the repo root.

**Tab 1 — Camera Service (port 8081)**

```powershell
docker build --build-arg SKIP_SSL_VERIFY=true -t camera-test -f resources/camera/Containerfile resources/camera
docker run --rm -it -p 8081:8081 camera-test
```

**Tab 2 — Orchestrator Service (port 8082)**

```powershell
docker build --build-arg SKIP_SSL_VERIFY=true -t orchestrator-test -f resources/orchestrator/Containerfile resources/orchestrator
docker run --rm -it -p 8082:8082 orchestrator-test
```

**Tab 3 — Inference Service (port 8083)**

```powershell
# Create the models directory if it doesn't exist
New-Item -ItemType Directory -Force -Path resources/inference/models

docker build --build-arg SKIP_SSL_VERIFY=true -t inference-test -f resources/inference/Containerfile resources/inference
docker run --rm -it -p 8083:8083 inference-test
```

**Verify all three (Tab 4 or browser)**

```powershell
curl http://localhost:8081/healthz
curl http://localhost:8082/healthz
curl http://localhost:8083/healthz
```

Each should return `{"status":"healthy"}`.

Stop each service with `Ctrl+C` in its tab.

---

### Option 3 (Windows): Webserver + Static Docs (NGINX)

```powershell
# Build the MkDocs static site into ./site
docker run --rm -it -v ${PWD}:/docs squidfunk/mkdocs-material build

# Build the NGINX webserver image (no pip installs — no SSL flag needed)
docker build -t nginx-itworks -f resources/webserver/Containerfile resources/webserver

# Run the webserver (serves on port 8080)
docker run --rm -it -p 8080:8080 nginx-itworks
```

Open **http://localhost:8080**.

---

### Windows Troubleshooting

**"CERTIFICATE_VERIFY_FAILED" / "self-signed certificate in certificate chain"**
Netskope (or another corporate proxy) is intercepting TLS. Add `--build-arg SKIP_SSL_VERIFY=true` to your `docker build` command. See the **Corporate Proxy / SSL Inspection** section above.

**"docker: command not found"**
Docker Desktop wasn't added to PATH. Restart your terminal after install, or reinstall and ensure "Add to PATH" is checked.

**"Port already in use"**
Find and stop the blocking process:
```powershell
netstat -ano | findstr :8081   # replace port as needed
taskkill /PID <PID> /F
```

**Volume mounts not working / empty site**
- In Docker Desktop → Settings → Resources → File Sharing, ensure your drive (e.g. `C:\`) is listed.
- Use forward slashes or `${PWD}` — avoid backslash paths in volume flags.

**WSL 2 kernel update required**
Follow the prompt in Docker Desktop or run:
```powershell
wsl --update
```

**Container exits immediately**
Check logs:
```powershell
docker ps -a                      # find container id
docker logs <container_id>
```

---

## Prerequisites (macOS / Linux)

### Required
- **Lima** - For containerization on macOS/Windows (or Docker/Podman on Linux)
- **Nerdctl** - Container CLI (installed via Lima)
- **Git** - For cloning and managing the repo

### Recommended
- **curl** - For health checks
- **8GB+ RAM** - For running multiple containerized services
- **5GB free disk space** - For container images and documentation

### Check Prerequisites

```bash
# Verify Lima is installed
limactl --version

# Start Lima (if not already running)
limactl start

# Verify nerdctl is available
lima nerdctl --version
```

---

## Option 1: Documentation System (Recommended First Step)

The documentation is built with **MkDocs Material** and runs in a containerized environment.

### 1. Start the Documentation Server (Development)

```bash
# Build the MkDocs container
lima nerdctl build -t mkdocs -f resources/mkdocs/Containerfile .

# Run the live-reload documentation server
lima nerdctl run --rm -it \
  -p 8000:8000 \
  -v ${PWD}:/docs:ro \
  squidfunk/mkdocs-material
```

### 2. View the Documentation

Open your browser to: **http://localhost:8000**

### 3. Verify It Works

- ✓ Landing page loads
- ✓ Navigate to "Operational Challenges" tab
- ✓ Check the CRISP-DM section
- ✓ View the Project Management blog posts

### Stop the Server

Press `Ctrl+C` in the terminal, or:

```bash
lima nerdctl stop mkdocs
lima nerdctl rmi mkdocs
```

---

## Option 2: Pipeline Services (Full Stack Demo)

The Imgest-Mesh pipeline consists of 4 coordinated microservices. Run each in a separate terminal.

### 1. Camera Service (Image Source)

**Terminal 1:**

```bash
# Build
lima nerdctl build -t camera-test -f resources/camera/Containerfile resources/camera

# Run
lima nerdctl run --rm -it \
  -p 8081:8081 \
  camera-test

# Verify
curl http://localhost:8081/healthz
```

Expected output: `{"status":"healthy"}`

### 2. Orchestrator Service (Router)

**Terminal 2:**

```bash
# Build
lima nerdctl build -t orchestrator-test -f resources/orchestrator/Containerfile resources/orchestrator

# Run
lima nerdctl run --rm -it \
  -p 8082:8082 \
  orchestrator-test

# Verify
curl http://localhost:8082/healthz
```

Expected output: `{"status":"healthy"}`

### 3. Inference Service (AI Model)

**Terminal 3:**

```bash
# Create model directory
mkdir -p resources/inference/models

# Build
lima nerdctl build -t inference-test -f resources/inference/Containerfile resources/inference

# Run
lima nerdctl run --rm -it \
  -p 8083:8083 \
  inference-test

# Verify
curl http://localhost:8083/healthz
```

Expected output: `{"status":"healthy"}`

### 4. Status Checks

Once all three services are running, check their status endpoints:

```bash
# Camera status
curl http://localhost:8081/status | json_pp

# Orchestrator status
curl http://localhost:8082/status | json_pp

# Inference status
curl http://localhost:8083/status | json_pp
```

### Stop All Services

Press `Ctrl+C` in each terminal to shut down gracefully.

---

## Option 3: Webserver + Documentation Container

For a production-like deployment, serve the built documentation via NGINX.

### Build and Run Documentation Site

```bash
# Build the MkDocs static site
lima nerdctl run --rm -it \
  -v ${PWD}:/docs \
  squidfunk/mkdocs-material build

# Build the webserver container
lima nerdctl build -t nginx-itworks -f resources/webserver/Containerfile resources/webserver

# Run webserver
lima nerdctl run --rm -it \
  -p 8080:8080 \
  -v ${PWD}/site:/usr/share/nginx/html:ro \
  nginx-itworks
```

Open browser to: **http://localhost:8080**

---

## Troubleshooting

### "Command not found: lima"
- Install Lima from: https://github.com/lima-vm/lima/releases
- On macOS: `brew install lima`

### "Container already exists"
Clean up old containers:
```bash
lima nerdctl ps -a
lima nerdctl rm <container_id>
```

### "Port already in use"
Kill the process using the port:
```bash
# macOS/Linux
lsof -i :8000  # or :8081, :8082, etc.
kill -9 <PID>
```

### "Permission denied" on mounted volumes
Ensure you're running commands from the project root directory with proper path expansion:
```bash
# Verify current directory
pwd

# Should output something like: /Users/username/path/to/t3-imgest-mesh
```

### Docker/Podman Instead of Lima?
If you're on Linux or Windows (Docker Desktop), substitute `lima nerdctl` with `docker` or `podman`:
```bash
# Replace:
lima nerdctl build ... 
# With:
docker build ...
# or:
podman build ...
```
Windows users: see the **Windows with Docker Desktop** section at the top of this guide.

---

## What's Next?

### Explore the Code
- **Camera Service**: `resources/camera/` - Image ingestion logic
- **Inference Service**: `resources/inference/` - Model inference placeholder
- **Orchestrator**: `resources/orchestrator/` - File routing logic
- **Webserver**: `resources/webserver/` - NGINX configuration

### Customize the Documentation
- Edit markdown files in `docs/`
- Run MkDocs in dev mode (Option 1) to see live changes
- Configuration: `mkdocs.yml`

### Deploy to Kubernetes/OpenShift
- See `resources/k8s/` for example manifests
- Follow deployment guide: `docs/hpc/` section
- Reference deployment platform: Cisco AI Pod + Red Hat OpenShift

### Modify Pipeline Services
1. Make code changes in `resources/{camera,inference,orchestrator}/app/`
2. Rebuild containers: `lima nerdctl build -t <service-name> ...`
3. Rerun with same command

---

## Quick Command Reference

```bash
# List running containers
lima nerdctl ps

# List all images
lima nerdctl images

# Stop a container
lima nerdctl stop <container_id>

# Remove an image
lima nerdctl rmi <image_name>

# View container logs
lima nerdctl logs <container_id>

# Stop Lima VM
limactl stop
```

---

## Documentation

- **Main README**: [README.md](README.md)
- **Pandoc Workflow**: [README-pandoc.md](README-pandoc.md) (legacy, single-doc generation)
- **MkDocs Config**: [mkdocs.yml](mkdocs.yml)
- **Project Docs**: http://localhost:8000 (when running)

---

**Questions?** Check the FAQ at `docs/t3/faq.md` or review specific service READMEs:
- `resources/camera/README.md`
- `resources/inference/README.md`
- `resources/orchestrator/README.md`
- `resources/webserver/README.md`
