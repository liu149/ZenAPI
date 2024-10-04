# FastAPI GCP 学习项目

这个项目的主要目的是通过使用 FastAPI 来熟悉 Google Cloud Platform (GCP)。在这里，我将记录学习过程、重要概念和实践经验。

## 项目概述

本项目使用 FastAPI 构建一个简单的 Web 应用，并将其部署到 Google Kubernetes Engine (GKE)。通过这个过程，我们将学习如何：

1. 创建基本的 FastAPI 应用
2. 使用 Docker 容器化应用
3. 使用 Google Cloud Build 自动构建和部署
4. 在 GKE 上运行和管理应用
5. 配置 Cloud DNS 进行域名管理

## 学习内容

### 1. 创建基本的 FastAPI 应用

- 使用 FastAPI 创建了一个简单的 Web 应用
- 学习了如何定义基本路由和处理请求

### 2. 本地开发和测试

在本地开发和测试 FastAPI 应用：

1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 运行应用：
   ```bash
   uvicorn main:app --reload
   ```

3. 访问 http://127.0.0.1:8000 查看应用
4. 访问 http://127.0.0.1:8000/docs 查看 API 文档

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

### 6. 配置域名和 Cloud DNS

为了使用自定义域名访问我们的应用，我们需要配置 Cloud DNS：

1. 在 Google Cloud Console 中，进入 Cloud DNS 服务。

2. 创建一个新的 DNS 区域，或使用现有的区域。

3. 添加一个新的 DNS 记录：
   - 记录类型：A
   - 名称：您想要使用的子域名（例如：api）
   - IPv4 地址：您的 GKE 服务的外部 IP 地址

4. 在您的域名注册商处，将域名的 NS（名称服务器）记录更新为 Google Cloud DNS 提供的名称服务器。

5. 等待 DNS 传播（可能需要几分钟到几小时）。

现在，您可以通过您配置的域名（例如：http://api.yourdomain.com）来访问您的 FastAPI 应用。

注意：
- 确保您的域名已经注册并且您有权限管理它。
- DNS 更改可能需要一些时间来全球传播，请耐心等待。
- 考虑配置 HTTPS 以增强安全性。您可以使用 Google-managed SSL 证书或自己的 SSL 证书。

### 下一步计划


- 实现 CI/CD 流程
- 配置 HTTPS
- 探索 GCP 的监控和日志功能
- 研究 GCP 的扩展性和高可用性特性

通过这个项目，我们不仅学习了 FastAPI 的使用，更重要的是深入了解了 GCP 的各种服务和最佳实践，包括容器化、Kubernetes 部署、自动构建和部署，以及域名管理。
