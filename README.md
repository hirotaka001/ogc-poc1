# Robot Platform using FIWARE

This repository construct a robot platform using [FIWARE](http://www.fiware.org/) on [Microsoft Azure AKS](https://azure.microsoft.com/en-us/services/kubernetes-service/)

## Description
The collaboration of robots, people and environments will help us to improve our productivity and to support the elderly people effectively.
This Robot Platform is aimed to realize this concept.

![ogc_poc_architecture.png](/docs/images/ogc_poc_architecture.png)

|component|summary|
|:--|:--|
|[kubernetes](https://kubernetes.io/)|Container Orchestration Platform|
|[API Gateway](https://www.getambassador.io/)|API Gateway|
|[auth](https://github.com/tech-sketch/fiware-ambassador-auth)|Authorization and Authentication component working with API Gateway|
|[FIWARE orion](https://catalogue-server.fiware.org/enablers/publishsubscribe-context-broker-orion-context-broker)|Publish/Subscribe Context Broker|
|[FIWARE cygnus](https://catalogue-server.fiware.org/enablers/cygnus)|Data collection and Persistence Agent|
|[FIWARE iotagent-ul](https://catalogue-server.fiware.org/enablers/backend-device-management-idas)|Backend Device Management Agent|
|[RabbitMQ](https://www.rabbitmq.com/)|Distributed Message Queue|
|[MongoDB](https://www.mongodb.com/)|Document-oriented NoSQL Database|
|[Prometheus](https://prometheus.io/)|Monitoring and Alerting toolkit|
|[Grafana](https://grafana.com/)|Analytics and Alerting platform for time series metrics|
|[Elasticsearch](https://www.elastic.co/products/elasticsearch)|Distributed search and analytics engine|
|[fluentd](https://www.fluentd.org/)|Data collector for unified logging layer|
|[Kibana](https://www.elastic.co/products/kibana)|Visualize the Elasticsearch data|

## Experiment to prove our concept
We and University of Aizu have been performed an experiment to guide a visitor by collaborating with heterogeneous robots, IoT devices and people through this Robot Platform on Nov. 6th - 8th , 2018.

Please show a short video of our experiment.

[![video](http://img.youtube.com/vi/D9NPxxYgPa0/0.jpg)](https://youtu.be/D9NPxxYgPa0)

## Requirements

* Microsoft Azure AKS
    * when you use monitoring & logging, you have to use the vm series which supports `Premium Storage` such as `Dsv3-series`.

||version|
|:--|:--|
|region|japaneast|
|kubernetes|1.11.2|

## Related repositories
### ROS
* [ROS bridge](https://github.com/ogcaizu/ogc-poc1-ros)
* [External camera](https://github.com/ogcaizu/uoa_ex_cam_sys_ros)

### Tablet for guide robot
* [Tablet application for guide robot](https://github.com/ogcaizu/ogc-poc1-robot-ipad)

### IoT devices
* [Button and LED](https://github.com/ogcaizu/ogc-poc1-device)

## License

[Apache License 2.0](/LICENSE)

## Copyright
Copyright (c) 2018 [TIS Inc.](https://www.tis.co.jp/)
