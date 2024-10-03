# FastAPI 学习项目

这个项目是为了学习FastAPI而创建的。在这里，我将记录我的学习过程、重要概念和实践经验。

## 学习内容

### 1. 创建基本的FastAPI应用

- 使用FastAPI创建了一个简单的Web应用
- 学习了如何定义一个基本的路由

#### 安装必要的包

首先，我们需要安装FastAPI和一个ASGI服务器（如Uvicorn）。在命令行中运行以下命令：

### 2. 本地启动服务

要在本地启动FastAPI服务，请按照以下步骤操作：

1. 确保您已经安装了所有必要的依赖。如果还没有安装，请运行：
   ```bash
   pip install -r requirements.txt
   ```

2. 在项目根目录下，运行以下命令启动服务：
   ```bash
   uvicorn main:app --reload
   ```
   这将启动开发服务器，并在文件更改时自动重新加载。

3. 打开浏览器并访问 http://127.0.0.1:8000 。您应该能看到FastAPI的欢迎页面。

4. 要访问API文档，请访问 http://127.0.0.1:8000/docs 。

5. 要停止服务器，请在命令行中按 Ctrl+C。

注意：在生产环境中，您应该使用更强大的ASGI服务器，如Gunicorn与Uvicorn workers。

### 3. Docker 操作

#### 构建 Docker 镜像

要构建 Docker 镜像，请在项目根目录下运行以下命令：

```bash
docker build -t your-dockerhub-username/zenapi-app:latest .
```

请将 `your-dockerhub-username` 替换为您的 Docker Hub 用户名。

#### 推送镜像到 Docker Hub

首先，确保您已经登录到 Docker Hub：

```bash
docker login
```

然后，推送镜像：

```bash
docker push your-dockerhub-username/zenapi-app:latest
```

#### 在 Docker 容器中运行应用

要在 Docker 容器中运行应用，请使用以下命令：

```bash
docker run -d -p 80:80 your-dockerhub-username/zenapi-app:latest
```

这将在后台运行容器，并将容器的 80 端口映射到主机的 80 端口。

现在，您可以通过访问 http://localhost 来查看您的应用。

要停止容器，首先找到容器 ID：

```bash
docker ps
```

然后停止容器：

```bash
docker stop <container-id>
```

### 4. 部署到 Kubernetes

要将应用部署到 Kubernetes 集群，请按照以下步骤操作：

1. 确保您已经安装并配置了 kubectl，并且可以连接到您的 Kubernetes 集群。

2. 应用 Kubernetes 配置文件：

   ```bash
   kubectl apply -f deployment.yaml
   kubectl apply -f service.yaml
   kubectl apply -f hpa.yaml
   ```

3. 如果您的集群中没有 metrics-server，请应用 components.yaml：

   ```bash
   kubectl apply -f components.yaml
   ```

4. 检查部署状态：

   ```bash
   kubectl get deployments
   kubectl get pods
   kubectl get services
   kubectl get hpa
   ```

5. 获取服务的外部 IP（如果使用 LoadBalancer 类型）：

   ```bash
   kubectl get services zenapi-service
   ```

   注意：如果您使用的是 Minikube，可能需要运行 `minikube service zenapi-service` 来访问服务。

6. 使用获取到的 IP 地址访问您的应用。

7. 监控 HPA：

   ```bash
   kubectl get hpa zenapi-hpa --watch
   ```

   这将显示 HPA 的当前状态，并在发生变化时更新。

8. 清理资源（当您想要删除部署时）：

   ```bash
   kubectl delete -f deployment.yaml
   kubectl delete -f service.yaml
   kubectl delete -f hpa.yaml
   ```

注意：请确保您的 Kubernetes 集群有足够的资源来运行这些部署。根据您的具体环境，可能需要调整 deployment.yaml 和 hpa.yaml 中的资源请求和限制。

### 5. 部署到 Google Kubernetes Engine (GKE)

要将应用部署到 Google Kubernetes Engine (GKE)，请按照以下步骤操作：

1. 确保您已经安装并配置了 Google Cloud SDK，并且可以使用 `gcloud` 命令。

2. 确保您已经创建了一个 GKE 集群。如果没有，可以使用以下命令创建：
   ```bash
   gcloud container clusters create my-gke --zone asia-east1 --num-nodes=3
   ```

3. 配置 kubectl 以使用您的 GKE 集群：
   ```bash
   gcloud container clusters get-credentials my-gke --zone asia-east1
   ```

4. 使用 Cloud Build 构建和部署应用。根据您的需求，可以选择以下两种方式之一：

   a. 构建新镜像并部署：
   ```bash
   gcloud builds submit --config cloudbuild.yaml --substitutions=_BUILD_IMAGE=true,_IMAGE_TAG=v1.0.0
   ```

   b. 仅更新部署（使用现有镜像）：
   ```bash
   gcloud builds submit --config cloudbuild.yaml --substitutions=_BUILD_IMAGE=false,_IMAGE_TAG=v1.0.0
   ```

   注意：请根据您的实际版本号更改 `v1.0.0`。

5. 等待部署完成。您可以使用以下命令检查部署状态：
   ```bash
   kubectl get deployments
   kubectl get pods
   kubectl get services
   ```

6. 获取服务的外部 IP 地址：
   ```bash
   kubectl get services zenapi-gke-service
   ```

7. 使用获取到的外部 IP 地址访问您的应用。

8. 如果需要更新应用，只需要重复步骤 4，根据需要选择是否构建新镜像。

9. 清理资源（当您想要删除部署时）：
   ```bash
   kubectl delete -f gke-deployment.yaml
   ```

注意：
- 确保您的 GCP 项目有足够的配额来运行 GKE 集群和部署您的应用。
- 记得在不使用时删除集群以避免不必要的费用。
- 根据您的安全要求，考虑配置网络策略和 RBAC。
