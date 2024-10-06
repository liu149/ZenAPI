#!/bin/bash

# 设置变量
DOCKER_USERNAME="liu149"
IMAGE_NAME="zenapi-app"
TAG="latest"

# 切换到项目根目录
cd "$(dirname "$0")/.."

# 构建 Docker 镜像
docker build -t $DOCKER_USERNAME/$IMAGE_NAME:$TAG -f Dockerfile .

# 推送镜像到 Docker Hub
docker push $DOCKER_USERNAME/$IMAGE_NAME:$TAG