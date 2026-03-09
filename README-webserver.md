## Build

limactl start
lima nerdctl build -t nginx-itworks -f resources/Dockerfile-webserver .

## Run

lima nerdctl run --rm -it \
  -p 8080:80 \
  -v $(pwd)/docs/assets/images/t3-imgest-mesh.png:/usr/share/nginx/html/t3-imgest-mesh.png:ro \
  nginx-itworks


...then launch `http://localhost:8080`

## Scrub-a-dub-dub...

lima nerdctl images
lima nerdctl rmi nginx-itworks
