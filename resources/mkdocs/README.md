Project Documentation
=====================

This is the master documentation sharing tool for projects, including PMO and As
Built documentation...


## Features

- **Project Management**: All aspects of the PMO from kickoff through closeout
- **Customizeable**: Add customization quickly and easily for unique requirements
- **Portable**: Dockerized and self-contained for portability

- **NOTE!!**: This doc updated 5/8 for `containerd` inlieu of _Docker_


## Demo

![Demo](docs/img/das-docs-demo.webp)


## Tech Stack

- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) - Foundation
- [Vega-Lite](https://vega.github.io/vega-lite/) - Grammar of Interactive Graphics
- ~~[Docker](https://www.docker.com/) - Containerization~~
- [Containerd](https://github.com/containerd) - Containerization
- [Nerdctl](https://github.com/containerd/nerdctl/) - Containerization Controls
- [Lima]()
- [Markdown](https://www.markdownguide.org/basic-syntax/) - Primary language
- [NGINX](https://www.nginx.com/) - Web server component


## Getting Started

---

### Prerequisites

Here's what you need to be able to Project Documentation:

- Containerd

- Editor of choice for Markdown files

**NOTE**: There are two Docker files involved, one to build the "site creation" and a
second one for "site publishing"


### 1. Clone the repository

```
clone
```

### 2. Build the image

```
lima nerdctl build -f resources/Containerfile-docs -t squidfunk/mkdocs-material .
```

### 3. IF NET NEW, initialize a new project

**NOTE**: This is not (always) necessary as the repo should contain the
foundational aspects of the documentation to be created. This is for a net-new
project of other origin.

```
lima nerdctl run --rm -it -v ${PWD}:/docs squidfunk/mkdocs-material new .
```

### 4. (Normal) Previewing project as you edit / change

```
lima nerdctl run --rm -it -p 8000:8000 -v ${PWD}:/docs:ro squidfunk/mkdocs-material
```

### 5. Open the app in your browser

Visit [http://localhost:8000](http://localhost:8000) in your browser.

**NOTE**: Javascript blockers will affect this in a variety of ways...accept JS.


## Publishing the Project Documentation

### 1. Build the finished site

```
lima nerdctl run --rm -it -v ${PWD}:/docs squidfunk/mkdocs-material build
```

- If necessary move `${PWD}/site` to wherever hosting...

### 2. Build container image

**NOTE**: Mind your tags!

```
lima nerdctl build -f Dockerfile-websvr -t registry.gitlab.com/dosayles/repo:tag .
```

### 3. Upload image to Gitlab repository

```
i? push registry.gitlab.com/dosayles/repo:tag
```

### 4. Pull container onto client system

```
sudo docker login registry.gitlab.com
sudo docker pull registry.gitlab.com/dosayles/repo:tag
sudo docker run --name t3-docs -d -p 8080:80 registry.gitlab.com/dosayles/repo:tag
```


## References

- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/creating-your-site/)
- [Building docker image w Plugins](https://squidfunk.github.io/mkdocs-material/getting-started/)


## Fast reference commands for cat/copy/paste purposes

```
pkill -SIGHUP -f /Applications/Docker.app 'docker serve'

limactl start
lima nerdctl build -t mkdocs -f resources/mkdocs/Containerfile .

lima nerdctl run --rm -it -p 8000:8000 -v ${PWD}:/docs:ro squidfunk/mkdocs-material

lima nerdctl rmi mkdocs
```

