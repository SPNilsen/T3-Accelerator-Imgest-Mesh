## Build

limactl start
lima nerdctl build -t nginx-itworks -f resources/Dockerfile-webserver .

## Run

limactl start
lima nerdctl run --rm -it -p 8080:80 nginx-itworks

then launch `http://localhost:8080`


