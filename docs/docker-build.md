# How to compile docker image locally

Now this project has used github's automatic docker compilation function. This document is provided for friends who need to compile docker images locally.

1. Install docker
```
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
2. Compile the docker image
```
#Enter the project root directory
#Compile server
docker build -t xiaozhi-esp32-server:server_latest -f ./Dockerfile-server .
# Compile web
docker build -t xiaozhi-esp32-server:web_latest -f ./Dockerfile-web .

# After compilation is completed, you can use docker-compose to start the project
# docker-compose.yml You need to modify it to the image version compiled by yourself
cd main/xiaozhi-server
docker-compose up -d
```
