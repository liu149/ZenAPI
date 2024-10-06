# 设置变量
$DOCKER_USERNAME = "liu149"
$IMAGE_NAME = "zenapi-app"
$TAG = "v1.0"

# 切换到项目根目录
Set-Location (Split-Path $PSScriptRoot)

# 构建 Docker 镜像
docker build -t ${DOCKER_USERNAME}/${IMAGE_NAME}:${TAG} -f local/Dockerfile .

# 推送镜像到 Docker Hub
docker push ${DOCKER_USERNAME}/${IMAGE_NAME}:${TAG}