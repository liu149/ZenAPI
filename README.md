# FastAPI GCP 学习项目

这个项目的主要目的是通过使用 FastAPI 来熟悉 Google Cloud Platform (GCP)。在这里，我将记录学习过程、重要概念和实践经验。

## 目录
1. [创建基本的 FastAPI 应用](#1-创建基本的-fastapi-应用)
2. [在 Docker 容器中运行应用](#2-在-docker-容器中运行应用)，
4. [将应用部署到本地 Kubernetes 集群](#4-将应用部署到本地-kubernetes-集群)
5. [将应用部署到 GKE](#5-将应用部署到-gke)
6. [使用 Google Cloud Build 自动构建和部署](#6-使用-google-cloud-build-自动构建和部署)
7. [使用 External DNS 自动管理 DNS 记录](#7-使用-external-dns-自动管理-dns-记录)
8. [GKE 上使用 Ingress](#8-gke-上使用-ingress)
9. [使用 Cloud Run 部署服务和作业](#9-使用-cloud-run-部署服务和作业)


### 1. 创建基本的 FastAPI 应用

- 使用 FastAPI 创建了一个简单的 Web 应用
- 安装依赖：
  ```bash
  pip install -r requirements.txt
  ```

- 运行项目：
  ```bash
  uvicorn src.main:app --reload
  ```

这将启动 FastAPI 应用，并在代码更改时自动重新加载。

- 创建了基本的路由，包括根路由 `/` 和健康检查路由 `/health`
- 添加了数据库连接测试路由 `/db-test`
- 实现了基本的单元测试

访问应用和文档：
- 应用主页：http://localhost:80
- API 文档：http://localhost:80/docs


### 2. 在 Docker 容器中运行应用

#### 构建 Docker 镜像
首先，确保您已经登录到 Docker Hub：

```bash
docker login
```

要构建 Docker 镜像并推送到 Docker Hub，请在项目根目录下运行以下命令：
# 构建 Docker 镜像
```bash
docker build -t ${DOCKER_USERNAME}/${IMAGE_NAME}:${TAG} -f Dockerfile .
```

# 推送镜像到 Docker Hub
```bash
docker push ${DOCKER_USERNAME}/${IMAGE_NAME}:${TAG}
```


# 运行Docker

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

### 3. 部署到本地 Kubernetes 集群

1. 确保您已经安装并配置了 kubectl，并且可以连接到您的本地 Kubernetes 集群（如 Minikube 或 Docker Desktop Kubernetes）。

2. 运行部署脚本：

   ```bash
   kubectl apply -f local/kubernetes-config.yaml
   ```

   这些脚本会自动应用必要的 Kubernetes 配置文件并检查部署状态。

3. 获取服务的外部 IP（如果使用 LoadBalancer 类型）：

   ```bash
   kubectl get services zenapi-service
   ```

   注意：如果您使用的是 Minikube，可能需要运行 `minikube service zenapi-service` 来访问服务。

4. 使用获取到的 IP 地址访问您的应用。

5. 监控 HPA：

   ```bash
   kubectl get hpa zenapi-hpa --watch
   ```

   这将显示 HPA 的当前状态，并在发生变化时更新。

6. 清理资源（当您想要删除部署时）：

   ```bash
   kubectl delete -f local/kubenetes-config.yaml
   ```

注意：请确保您的本地 Kubernetes 集群有足够的资源来运行这些部署。根据您的具体环境，可能需要调整 deployment.yaml 和 hpa.yaml 中的资源请求和限制。

### 4. 部署到 Google Kubernetes Engine (GKE)

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

4. 设置 Cloud Build 触发器：
   a. 在 Google Cloud Console 中，导航到 Cloud Build > 触发器。
   b. 点击"创建触发器"。
   c. 选择您的源代码仓库（例如 GitHub）。
   d. 配置触发器：
      - 名称：给触发器起一个描述性的名称（例如："Deploy to GKE"）
      - 事件：选择"推送到分支"
      - 源：选择您的仓库和分支（例如 main）
      - 配置文件：选择"Cloud Build 配置文件"，并指定路径为 gcp/cloudbuild.yaml
      - 替代变量：
        _CLOUDSDK_COMPUTE_ZONE: asia-east1
        _CLOUDSDK_CONTAINER_CLUSTER: my-gke
        _BUILD_IMAGE: true
        _ACTION: apply
   e. 点击"创建"保存触发器。

5. 触发部署：
   - 手动触发：在 Cloud Build 触发器页面，找到您刚创建的触发器，点击"运行"。
   - 自动触发：推送更改到您配置的 Git 分支。

6. 监控部署：
   - 在 Cloud Build > 历史记录中查看构建进度。
   - 使用以下命令检查部署状态：
     ```bash
     kubectl get deployments
     kubectl get pods
     kubectl get services
     ```

7. 获取服务的外部 IP 地址：
   ```bash
   kubectl get services zenapi-gke-service
   ```

8. 使用获取到的外部 IP 地址访问您的应用。

9. 如果需要更新应用，只需要推送更改到 Git 仓库，触发器将自动启动新的部署。

10. 清理资源（当您想要删除部署时）：
    - 手动触发构建，设置 _ACTION 为 delete
    - 或者使用 kubectl：
      ```bash
      kubectl delete -f gcp/gke-deployment.yaml
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

### 切换 Kubernetes 集群

在使用多个 Kubernetes 集群时，您可能需要在它们之间切换。以下是一些有用的命令：

1. 查看当前的集群上下文：
   ```bash
   kubectl config current-context
   ```

2. 查看所有可用的集群上下文：
   ```bash
   kubectl config get-contexts
   ```

3. 切换到特定的集群上下文：
   ```bash
   kubectl config use-context <context-name>
   ```

4. 对于 GKE 集群，使用 gcloud 命令切换：
   ```bash
   gcloud container clusters get-credentials <cluster-name> --zone <zone> --project <project-id>
   ```

确保在执行部署或其他操作之前，您已经切换到了正确的集群上下文。


### 9. 使用 Cloud Run 部署服务和作业

#### a. 创建服务账号

创建一个名为 `cloudbuild-sa` 的服务账号，并确保它具有以下权限：

- Artifact Registry Administrator
- Cloud Run Admin
- Logs Writer
- Service Account User
- Storage Admin

#### b. 部署到 Cloud Run

使用以下命令部署服务：gcloud builds submit --config=gcp/cloudRun/cloudbuild.yaml

