# 6. monitoring fiware cluster

## view metrics

### open prometheus
```bash
mac:$ kubectl --namespace monitoring port-forward $(kubectl get pod --namespace monitoring -l prometheus=kube-prometheus -l app=prometheus -o template --template "{{(index .items 0).metadata.name}}") 9090:9090
```
```bash
mac:$ open http://localhost:9090/
```

1. open http://localhost:9090/targets and check that all states are UP

## view log

### open kibana
```bash
mac:$ kubectl --namespace monitoring port-forward $(kubectl get pod -l k8s-app=kibana-logging --namespace monitoring -o template --template "{{(index .items 0).metadata.name}}") 5601:5601
```
```bash
mac:$ open http://localhost:5601/
```

1. configure `Index Pattern` as `logstash-*`
1. configure `Time Filter field name` as `@timestamp`

### open grafana
```bash
mac:$ kubectl --namespace monitoring port-forward $(kubectl get pod --namespace monitoring -l app=ogc-kube-prometheus-grafana -o template --template "{{(index .items 0).metadata.name}}") 3000:3000
```
```bash
mac:$ open http://localhost:3000/
```

1. login grafana as `admin/${GRAFANA_ADMIN_PASSWORD}`
1. Add ElasticSearch datasource
    * Name: `elasticsearch`
    * Type: `Elasticsearch`
    * URL: `http://elasticsearch-logging:9200`
    * Access: `Server(Default)`
    * Index name: `logstash-*`
    * Time field name: `@timestamp`
    * Version: `5.6+`
1. Add Slack incomming webhook as Notification channel
1. import `monitoring/dashboard_persistent_volumes.json`
1. import `monitoring/dashboard_elasticsearch.json`
    * edit and save `External Camera Error` panel to change Notification
