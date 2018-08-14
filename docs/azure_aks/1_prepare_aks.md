# 1. prepare Microsoft Azure AKS

Prepare [Microsoft Azure AKS](https://azure.microsoft.com/en-us/services/container-service/) by following steps:

1. [login Azure](#login-azure)
1. [create DNS zone](#create-dns-zone-of-examplecom)
1. [create resource group](#create-resource-group)
1. [start private registry](#start-private-registry-on-azure-container-registry)
1. [start face API service](#start-face-api-service)
1. [start kubernetes](#start-kubernetes-on-azure-aks)
1. [install helm](#install-helm)


## login Azure

```bash
mac:$ az login --tenant tenant.onmicrosoft.com
```

## create DNS zone of "tech-sketch.jp"

```bash
mac:$ az group create --name dns-zone --location japaneast
```

```bash
mac:$ az network dns zone create --resource-group dns-zone --name "tech-sketch.jp"
```

```bash
mac:$ az network dns zone show --resource-group dns-zone --name "tech-sketch.jp" | jq ".nameServers"
[
  "ns1-XX.azure-dns.com.",
  "ns2-XX.azure-dns.net.",
  "ns3-XX.azure-dns.org.",
  "ns4-XX.azure-dns.info."
]
```

## create resource group

```bash
mac:$ az group create --name ogc-poc1 --location japaneast
```

## start private registry on Azure Container Registry

```bash
mac:$ az acr create --resource-group ogc-poc1 --name ogcacr --sku Basic
mac:$ export REPOSITORY=$(az acr show --resource-group ogc-poc1 --name ogcacr | jq '.loginServer' -r); echo ${REPOSITORY}
```

```bash
mac:$ az acr login --name ogcacr
```

## start Face API service

```bash
mac:$ az cognitiveservices account create --kind Face --location japaneast --name faceapi --resource-group ogc-poc1 --sku S0 --yes
```
```bash
mac:$ az cognitiveservices account show --name faceapi --resource-group ogc-poc1
{
  "endpoint": "https://japaneast.api.cognitive.microsoft.com/face/v1.0",
  "etag": "\"00002f1f-0000-0000-0000-5b70cc430000\"",
  "id": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/ogc-poc1/providers/Microsoft.CognitiveServices/accounts/faceapi",
  "internalId": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "kind": "Face",
  "location": "japaneast",
  "name": "faceapi",
  "provisioningState": "Succeeded",
  "resourceGroup": "ogc-poc1",
  "sku": {
    "name": "S0",
    "tier": null
  },
  "tags": null,
  "type": "Microsoft.CognitiveServices/accounts"
}
```
```bash
mac:$ export FACE_API_BASEURL=$(az cognitiveservices account show --name faceapi --resource-group ogc-poc1 | jq .endpoint -r);echo ${FACE_API_BASEURL}
https://japaneast.api.cognitive.microsoft.com/face/v1.0
```
```bash
mac:$ export FACE_API_KEY=$(az cognitiveservices account keys list --name faceapi --resource-group ogc-poc1 | jq .key1 -r);echo ${FACE_API_KEY}
ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ
```

## start kubernetes on Azure AKS

```bash
mac:$ az provider register -n Microsoft.Compute
mac:$ az provider register -n Microsoft.Storage
mac:$ az provider register -n Microsoft.Network
mac:$ az provider register -n Microsoft.ContainerService
```

```bash
mac:$ az provider show -n Microsoft.Compute | jq '.registrationState' -r
Registered
mac:$ az provider show -n Microsoft.Storage | jq '.registrationState' -r
Registered
mac:$ az provider show -n Microsoft.Network | jq '.registrationState' -r
Registered
mac:$ az provider show -n Microsoft.ContainerService | jq '.registrationState' -r
Registered
```

```bash
mac:$ az aks create --resource-group ogc-poc1 --name ogc-poc1-aks --node-count 4 --ssh-key-value $HOME/.ssh/azure.pub --enable-rbac --node-vm-size Standard_D2s_v3 --kubernetes-version 1.11.1
```

```bash
mac:$ az aks get-credentials --resource-group ogc-poc1 --name ogc-poc1-aks
```

```bash
mac:$ CLIENT_ID=$(az aks show --resource-group ogc-poc1 --name ogc-poc1-aks --query "servicePrincipalProfile.clientId" --output tsv);echo ${CLIENT_ID}
mac:$ ACR_ID=$(az acr show --name ogcacr --resource-group ogc-poc1 --query "id" --output tsv); echo ${ACR_ID}
mac:$ az role assignment create --assignee ${CLIENT_ID} --role Reader --scope ${ACR_ID}
```

```bash
mac:$ kubectl get nodes
NAME                       STATUS    ROLES     AGE       VERSION
aks-nodepool1-23249322-0   Ready     agent     8m        v1.11.1
aks-nodepool1-23249322-1   Ready     agent     8m        v1.11.1
aks-nodepool1-23249322-2   Ready     agent     8m        v1.11.1
aks-nodepool1-23249322-3   Ready     agent     8m        v1.11.1
```

## setup rbac

```bash
mac:$ kubectl apply -f rbac/dashboard-rbac.yaml
```
```bash
mac:$ kubectl get serviceaccounts -n kube-system | grep kubernetes-dashboard
kubernetes-dashboard                 1         12m
```

```bash
mac:$ kubectl apply -f rbac/tiller-rbac.yaml
```
```bash
mac:$ kubectl get serviceaccounts -n kube-system | grep tiller
tiller                               1         19s
```

```bash
mac:$ kubectl apply -f rbac/default-rbac.yaml
```
```bash
mac:$ kubectl get clusterroles | grep default-read
default-read                                                           1m
```

## install helm
```bash
mac:$ helm version --client
Client: &version.Version{SemVer:"v2.9.1", GitCommit:"20adb27c7c5868466912eebdf6664e7390ebe710", GitTreeState:"clean"}
```

```bash
mac:$ helm init --service-account tiller
mac:$ helm repo update
```

```bash
mac:$ kubectl get pods --all-namespaces | grep tiller
kube-system   tiller-deploy-759cb9df9-88gmw           1/1       Running   0          1m
```

```bash
mac:$ helm version
Client: &version.Version{SemVer:"v2.9.1", GitCommit:"20adb27c7c5868466912eebdf6664e7390ebe710", GitTreeState:"clean"}
Server: &version.Version{SemVer:"v2.9.1", GitCommit:"20adb27c7c5868466912eebdf6664e7390ebe710", GitTreeState:"clean"}
```
