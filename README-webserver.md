## Preamble

This webserver container is built to align with OpenShift-style restricted
security practices, which is important for deployment onto the Cisco AI Pod
environment running Red Hat OpenShift. Rather than assuming root privileges, the
container uses an unprivileged NGINX image and listens on port 8080 instead of
80. This avoids the common problems caused by OpenShift’s default behavior of
assigning a random non-root UID to running containers. The NGINX configuration
also writes its PID and temporary files under /tmp, which is the expected
pattern for non-root container execution. In short, this keeps the image
lightweight for local CLI testing while also making it structurally compatible
with how workloads are typically run inside OpenShift.  ￼



## Build

limactl start
lima nerdctl build -t nginx-itworks -f resources/Containerfile-webserver .

## Run

lima nerdctl run --rm -it \
  -p 8080:8080 \
  -v $(pwd)/docs/assets/images/t3-imgest-mesh.png:/usr/share/nginx/html/t3-imgest-mesh.png:ro \
  nginx-itworks


...then launch `http://localhost:8080`

## Scrub-a-dub-dub...

lima nerdctl images
lima nerdctl rmi nginx-itworks
