# 6. monitoring fiware cluster

## view metrics of prometheus

```bash
mac:$ kubectl --namespace monitoring port-forward $(kubectl get pod --namespace monitoring -l prometheus=kube-prometheus -l app=prometheus -o template --template "{{(index .items 0).metadata.name}}") 9090:9090
```
```bash
mac:$ open http://localhost:9090/
```

## open grafana

```bash
mac:$ kubectl --namespace monitoring port-forward $(kubectl get pod --namespace monitoring -l app=ogc-kube-prometheus-grafana -o template --template "{{(index .items 0).metadata.name}}") 3000:3000
```
```bash
mac:$ open http://localhost:3000/
```

* login grafana as `admin/${GRAFANA_ADMIN_PASSWORD}`
