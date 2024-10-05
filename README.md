# FastAPI GCP 学习项目

这个项目的主要目的是通过使用 FastAPI 来熟悉 Google Cloud Platform (GCP)。在这里，我将记录学习过程、重要概念和实践经验。

## 项目概述

本项目使用 FastAPI 构建一个简单的 Web 应用，并将其部署到 Google Kubernetes Engine (GKE)。通过这个过程，我们将学习如何：

1. 创建基本的 FastAPI 应用
2. 使用 Docker 容器化应用
3. 使用 Google Cloud Build 自动构建和部署
4. 在 GKE 上运行和管理应用
5. 配置 Cloud DNS 进行域名管理
6. 使用 External DNS 自动管理 DNS 记录

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

### 6. External DNS 配置

为了自动管理 DNS 记录，我们使用了 External DNS。以下是详细的配置步骤：

1. 创建 Google Cloud Service Account：
   - 在 Google Cloud Console 中，导航到 "IAM & Admin" > "Service Accounts"
   - 点击 "Create Service Account"
   - 输入服务账号名称（例如：external-dns-sa）
   - 为服务账号分配以下角色：
     - DNS Administrator

External DNS 通过监听 Kubernetes API 服务器来发现新的服务和 ingress 资源，然后根据这些资源的配置自动在 DNS 提供商（如 Google Cloud DNS）中创建相应的 DNS 记录。这大大简化了在 Kubernetes 环境中管理 DNS 记录的过程。

#### b. 创建 IAM 服务账号并分配权限

1. 创建 IAM 服务账号：
   ```bash
   gcloud iam service-accounts create external-dns --display-name "External DNS"
   ```

2. 为服务账号分配 DNS 管理员角色：
   ```bash
   gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
     --member serviceAccount:external-dns@YOUR_PROJECT_ID.iam.gserviceaccount.com \
     --role roles/dns.admin
   ```

#### c. 开启 GKE 集群的 Workload Identity

1. 更新现有集群以启用 Workload Identity：
   ```bash
   gcloud container clusters update YOUR_CLUSTER_NAME \
     --zone YOUR_CLUSTER_ZONE \
     --workload-pool=YOUR_PROJECT_ID.svc.id.goog
   ```

2. 配置 IAM 服务账号以允许 Kubernetes 服务账号使用它：
   ```bash
   gcloud iam service-accounts add-iam-policy-binding \
     --role roles/iam.workloadIdentityUser \
     --member "serviceAccount:YOUR_PROJECT_ID.svc.id.goog[YOUR_K8S_NAMESPACE/external-dns]" \
     external-dns@YOUR_PROJECT_ID.iam.gserviceaccount.com
   ```

#### d. 配置 DNS 和其他准备工作

1. 确保在 GCP 控制台中启用了 Cloud DNS API。

2. 手动创建 DNS zone（如果还没有）：
   ```bash
   gcloud dns managed-zones create YOUR_ZONE_NAME --dns-name YOUR_DOMAIN --description "Managed by External DNS"
   ```

#### e. 部署 External DNS

1. 应用 external-dns-sa.yaml 文件来创建必要的 Kubernetes 资源：
   ```bash
   kubectl apply -f external-dns-sa.yaml
   ```

2. 检查 External DNS 的部署状态：
   ```bash
   kubectl get pods -l app=external-dns
   ```

3. 查看 External DNS 的日志以确保它正在正常工作：
   ```bash
   kubectl logs -f $(kubectl get pods -l app=external-dns -o name)
   ```

#### f. 使用 External DNS

在您的服务或 Ingress 资源中，添加以下注解来让 External DNS 自动创建 DNS 记录：

```yaml
annotations:
  external-dns.alpha.kubernetes.io/hostname: your-service.your-domain.com
```

注意：确保将上述配置中的占位符（如 YOUR_PROJECT_ID、YOUR_CLUSTER_NAME、YOUR_CLUSTER_ZONE、YOUR_ZONE_NAME、YOUR_DOMAIN）替换为您的实际值。

这个配置使用 Workload Identity 来安全地授权 External DNS 访问 Google Cloud DNS，无需使用服务账号密钥文件。通过这种方式，我们提高了安全性，并简化了凭证管理。