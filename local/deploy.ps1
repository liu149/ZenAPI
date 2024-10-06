# 切换到项目根目录
Set-Location (Split-Path $PSScriptRoot)

# 应用 Kubernetes 配置
Write-Host "Applying Kubernetes configurations..."

# 应用合并后的配置文件
kubectl apply -f local/kubernetes-config.yaml

# 如果需要 metrics-server（仅在本地 Kubernetes 集群中需要）
# kubectl apply -f local/components.yaml

Write-Host "Deployment completed. Checking status..."

# 检查部署状态
kubectl get deployments
kubectl get services
kubectl get hpa

Write-Host "Deployment process finished."