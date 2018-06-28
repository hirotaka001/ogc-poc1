# 3. configure fiware on AKS

Configure fiware on AKS by following steps:

1. [register "BUTTON-SENSOR" service](#register-button-sensor-service)
1. [register "BUTTON-SENSOR" device](#register-button-sensor-device)
1. [test "BUTTON-SENSOR" attribute](#test-button-sensor-attribute)
1. [register "PEPPER" service](#register-pepper-service)
1. [register "PEPPER" device](#register-pepper-device)
1. [test "PEPPER" command](#test-pepper-command)
1. [register cygnus](#register-cygnus)
1. [register "reception" as a subscriber of "BUTTON-SENSOR"](#register-reception-as-a-subscriber-of-button-sensor)

**In the following document, replace "example.com" with your domain.**

## register BUTTON-SENSOR service
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: button_sensor" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.cloudconductor.jp/idas/ul20/manage/iot/services/ -X POST -d @- <<__EOS__
{
  "services": [
    {
      "apikey": "button_sensor",
      "cbroker": "http://orion:1026",
      "resource": "/iot/d",
      "entity_type": "button_sensor"
    }
  ]
}
__EOS__
```
```bash
mac:$ $ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: button_sensor" -H "Fiware-Servicepath: /*" https://api.cloudconductor.jp/idas/ul20/manage/iot/services/ | jq .
{
  "count": 1,
  "services": [
    {
      "_id": "5b2c702076c6700001471a69",
      "subservice": "/",
      "service": "button_sensor",
      "apikey": "button_sensor",
      "resource": "/iot/d",
      "__v": 0,
      "attributes": [],
      "lazy": [],
      "commands": [],
      "entity_type": "button_sensor",
      "internal_attributes": [],
      "static_attributes": []
    }
  ]
}
```

## register BUTTON-SENSOR device
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: button_sensor" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.cloudconductor.jp/idas/ul20/manage/iot/devices/ -X POST -d @- <<__EOS__
{
  "devices": [
    {
      "device_id": "button_sensor_0000000000000001",
      "entity_name": "button_sensor_0000000000000001",
      "entity_type": "button_sensor",
      "timezone": "Asia/Tokyo",
      "protocol": "UL20",
      "attributes": [
        {
          "name": "state",
          "type": "string"
        }
      ],
      "transport": "MQTT"
    }
  ]
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: button_sensor" -H "Fiware-Servicepath: /" https://api.cloudconductor.jp/idas/ul20/manage/iot/devices/button_sensor_0000000000000001/ | jq .
{
  "device_id": "button_sensor_0000000000000001",
  "service": "button_sensor",
  "service_path": "/",
  "entity_name": "button_sensor_0000000000000001",
  "entity_type": "button_sensor",
  "transport": "MQTT",
  "attributes": [
    {
      "object_id": "state",
      "name": "state",
      "type": "string"
    }
  ],
  "lazy": [],
  "commands": [],
  "static_attributes": [],
  "protocol": "UL20"
}
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: button_sensor" -H "Fiware-Servicepath: /" https://api.cloudconductor.jp/orion/v2/entities/button_sensor_0000000000000001/ | jq .
{
  "id": "button_sensor_0000000000000001",
  "type": "button_sensor",
  "TimeInstant": {
    "type": "ISO8601",
    "value": " ",
    "metadata": {}
  },
  "state": {
    "type": "string",
    "value": " ",
    "metadata": {}
  }
}
```

## test BUTTON-SENSOR attribute
```bash
mac:$ mosquitto_sub -h mqtt.cloudconductor.jp -p 8883 --cafile ./secrets/ca.crt -d -t /# -u iotagent -P XXXXXXXX
```
```bash
mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.cloudconductor.jp -p 8883 --cafile ./secrets/ca.crt -d -t /button_sensor/button_sensor_0000000000000001/attrs -u iotagent -P XXXXXXXX -m "$d|state|on"
Client mosqpub|92108-Nobuyukin sending CONNECT
Client mosqpub|92108-Nobuyukin received CONNACK
Client mosqpub|92108-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/button_sensor/button_sensor_0000000000000001/attrs', ... (44 bytes))
Client mosqpub|92108-Nobuyukin sending DISCONNECT
```
```bash
mac:$ mosquitto_sub -h mqtt.cloudconductor.jp -p 8883 --cafile ./secrets/ca.crt -d -t /# -u iotagent -P XXXXXXXX
...
Client mosqsub|32291-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/button_sensor/button_sensor_0000000000000001/attrs', ... (44 bytes))
2018-06-22T15:15:53.1529648153+0900|state|on
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: button_sensor" -H "Fiware-Servicepath: /" https://api.cloudconductor.jp/orion/v2/entities/button_sensor_0000000000000001/ | jq .
{
  "id": "button_sensor_0000000000000001",
  "type": "button_sensor",
  "TimeInstant": {
    "type": "ISO8601",
    "value": "2018-06-22T15:15:53.1529648153+0900",
    "metadata": {}
  },
  "state": {
    "type": "string",
    "value": "on",
    "metadata": {
      "TimeInstant": {
        "type": "ISO8601",
        "value": "2018-06-22T15:15:53.1529648153+0900"
      }
    }
  }
}
```

## register PEPPER service
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.cloudconductor.jp/idas/ul20/manage/iot/services/ -X POST -d @- <<__EOS__
{
  "services": [
    {
      "apikey": "pepper",
      "cbroker": "http://orion:1026",
      "resource": "/iot/d",
      "entity_type": "pepper"
    }
  ]
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-Servicepath: /*" https://api.cloudconductor.jp/idas/ul20/manage/iot/services/ | jq .
{
  "count": 1,
  "services": [
    {
      "_id": "5b2c70b2a74ba7000166da17",
      "subservice": "/",
      "service": "pepper",
      "apikey": "pepper",
      "resource": "/iot/d",
      "__v": 0,
      "attributes": [],
      "lazy": [],
      "commands": [],
      "entity_type": "pepper",
      "internal_attributes": [],
      "static_attributes": []
    }
  ]
}
```

## register PEPPER device
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.cloudconductor.jp/idas/ul20/manage/iot/devices/ -X POST -d @- <<__EOS__
{
  "devices": [
    {
      "device_id": "pepper_0000000000000001",
      "entity_name": "pepper_0000000000000001",
      "entity_type": "pepper",
      "timezone": "Asia/Tokyo",
      "protocol": "UL20",
      "attributes": [
        {
          "name": "face",
          "type": "string"
        }, {
          "name": "dest",
          "type": "string"
        }
      ],
      "commands": [
        {
          "name": "welcome",
          "type": "string"
        }, {
          "name": "handover",
          "type": "string"
        }, {
          "name": "facedetect",
          "type": "string"
        }, {
          "name": "retry",
          "type": "string"
        }
      ],
      "transport": "MQTT"
    }
  ]
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.cloudconductor.jp/idas/ul20/manage/iot/devices/ -X POST -d @- <<__EOS__
{
  "devices": [
    {
      "device_id": "pepper_0000000000000002",
      "entity_name": "pepper_0000000000000002",
      "entity_type": "pepper",
      "timezone": "Asia/Tokyo",
      "protocol": "UL20",
      "attributes": [
        {
          "name": "face",
          "type": "string"
        }, {
          "name": "dest",
          "type": "string"
        }
      ],
      "commands": [
        {
          "name": "welcome",
          "type": "string"
        }, {
          "name": "handover",
          "type": "string"
        }, {
          "name": "facedetect",
          "type": "string"
        }, {
          "name": "retry",
          "type": "string"
        }
      ],
      "transport": "MQTT"
    }
  ]
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-Servicepath: /" https://api.cloudconductor.jp/idas/ul20/manage/iot/devices/pepper_0000000000000001/ | jq .
{
  "device_id": "pepper_0000000000000001",
  "service": "pepper",
  "service_path": "/",
  "entity_name": "pepper_0000000000000001",
  "entity_type": "pepper",
  "transport": "MQTT",
  "attributes": [
    {
      "object_id": "face",
      "name": "face",
      "type": "string"
    },
    {
      "object_id": "dest",
      "name": "dest",
      "type": "string"
    }
  ],
  "lazy": [],
  "commands": [
    {
      "object_id": "welcome",
      "name": "welcome",
      "type": "string"
    },
    {
      "object_id": "handover",
      "name": "handover",
      "type": "string"
    },
    {
      "object_id": "facedetect",
      "name": "facedetect",
      "type": "string"
    },
    {
      "object_id": "retry",
      "name": "retry",
      "type": "string"
    }
  ],
  "static_attributes": [],
  "protocol": "UL20"
}
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-Servicepath: /" https://api.cloudconductor.jp/orion/v2/entities/pepper_0000000000000001/ | jq .
{
  "id": "pepper_0000000000000001",
  "type": "pepper",
  "TimeInstant": {
    "type": "ISO8601",
    "value": " ",
    "metadata": {}
  },
  "dest": {
    "type": "string",
    "value": " ",
    "metadata": {}
  },
  "face": {
    "type": "string",
    "value": " ",
    "metadata": {}
  },
  "facedetect_info": {
    "type": "commandResult",
    "value": " ",
    "metadata": {}
  },
  "facedetect_status": {
    "type": "commandStatus",
    "value": "UNKNOWN",
    "metadata": {}
  },
  "handover_info": {
    "type": "commandResult",
    "value": " ",
    "metadata": {}
  },
  "handover_status": {
    "type": "commandStatus",
    "value": "UNKNOWN",
    "metadata": {}
  },
  "retry_info": {
    "type": "commandResult",
    "value": " ",
    "metadata": {}
  },
  "retry_status": {
    "type": "commandStatus",
    "value": "UNKNOWN",
    "metadata": {}
  },
  "welcome_info": {
    "type": "commandResult",
    "value": " ",
    "metadata": {}
  },
  "welcome_status": {
    "type": "commandStatus",
    "value": "UNKNOWN",
    "metadata": {}
  },
  "welcome": {
    "type": "string",
    "value": "",
    "metadata": {}
  },
  "handover": {
    "type": "string",
    "value": "",
    "metadata": {}
  },
  "facedetect": {
    "type": "string",
    "value": "",
    "metadata": {}
  },
  "retry": {
    "type": "string",
    "value": "",
    "metadata": {}
  }
}
```

## test PEPPER command
```bash
mac:$ mosquitto_sub -h mqtt.cloudconductor.jp -p 8883 --cafile ./secrets/ca.crt -d -t /# -u iotagent -P XXXXXXXX
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-Servicepath: /" -H "Content-Type: application/json" https://api.cloudconductor.jp/orion/v1/updateContext -d @-<<__EOS__ | jq .
{
  "contextElements": [
    {
      "id": "pepper_0000000000000001",
      "isPattern": "false",
      "type": "pepper",
      "attributes": [
        {
          "name": "welcome",
          "value": "start"
        }
      ]
    }
  ],
  "updateAction": "UPDATE"
}
__EOS__
```
```bash
mac:$ mosquitto_sub -h mqtt.cloudconductor.jp -p 8883 --cafile ./secrets/ca.crt -d -t /# -u iotagent -P XXXXXXXX
...
Client mosqsub|32291-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/cmd', ... (37 bytes))
pepper_0000000000000001@welcome|start
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-Servicepath: /" https://api.cloudconductor.jp/orion/v2/entities/pepper_0000000000000001/ | jq .
{
  "id": "pepper_0000000000000001",
  "type": "pepper",
  "TimeInstant": {
    "type": "ISO8601",
    "value": "2018-06-22T04:21:44.00Z",
    "metadata": {}
  },
  "dest": {
    "type": "string",
    "value": " ",
    "metadata": {}
  },
  "face": {
    "type": "string",
    "value": " ",
    "metadata": {}
  },
  "facedetect_info": {
    "type": "commandResult",
    "value": " ",
    "metadata": {}
  },
  "facedetect_status": {
    "type": "commandStatus",
    "value": "UNKNOWN",
    "metadata": {}
  },
  "handover_info": {
    "type": "commandResult",
    "value": " ",
    "metadata": {}
  },
  "handover_status": {
    "type": "commandStatus",
    "value": "UNKNOWN",
    "metadata": {}
  },
  "retry_info": {
    "type": "commandResult",
    "value": " ",
    "metadata": {}
  },
  "retry_status": {
    "type": "commandStatus",
    "value": "UNKNOWN",
    "metadata": {}
  },
  "welcome_info": {
    "type": "commandResult",
    "value": " ",
    "metadata": {}
  },
  "welcome_status": {
    "type": "commandStatus",
    "value": "PENDING",
    "metadata": {
      "TimeInstant": {
        "type": "ISO8601",
        "value": "2018-06-22T04:21:44.067Z"
      }
    }
  },
  "welcome": {
    "type": "string",
    "value": "",
    "metadata": {}
  },
  "handover": {
    "type": "string",
    "value": "",
    "metadata": {}
  },
  "facedetect": {
    "type": "string",
    "value": "",
    "metadata": {}
  },
  "retry": {
    "type": "string",
    "value": "",
    "metadata": {}
  }
}
```

```bash
mac:$ mosquitto_pub -h mqtt.cloudconductor.jp -p 8883 --cafile ./secrets/ca.crt -d -t /pepper/pepper_0000000000000001/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000001@welcome|start exec"
Client mosqpub|92385-Nobuyukin sending CONNECT
Client mosqpub|92385-Nobuyukin received CONNACK
Client mosqpub|92385-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/cmdexe', ... (42 bytes))
Client mosqpub|92385-Nobuyukin sending DISCONNECT
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-Servicepath: /" https://api.cloudconductor.jp/orion/v2/entities/pepper_0000000000000001/ | jq .
{
  "id": "pepper_0000000000000001",
  "type": "pepper",
  "TimeInstant": {
    "type": "ISO8601",
    "value": "2018-06-22T04:22:41.00Z",
    "metadata": {}
  },
  "dest": {
    "type": "string",
    "value": " ",
    "metadata": {}
  },
  "face": {
    "type": "string",
    "value": " ",
    "metadata": {}
  },
  "facedetect_info": {
    "type": "commandResult",
    "value": " ",
    "metadata": {}
  },
  "facedetect_status": {
    "type": "commandStatus",
    "value": "UNKNOWN",
    "metadata": {}
  },
  "handover_info": {
    "type": "commandResult",
    "value": " ",
    "metadata": {}
  },
  "handover_status": {
    "type": "commandStatus",
    "value": "UNKNOWN",
    "metadata": {}
  },
  "retry_info": {
    "type": "commandResult",
    "value": " ",
    "metadata": {}
  },
  "retry_status": {
    "type": "commandStatus",
    "value": "UNKNOWN",
    "metadata": {}
  },
  "welcome_info": {
    "type": "commandResult",
    "value": "start exec",
    "metadata": {
      "TimeInstant": {
        "type": "ISO8601",
        "value": "2018-06-22T04:22:41.606Z"
      }
    }
  },
  "welcome_status": {
    "type": "commandStatus",
    "value": "OK",
    "metadata": {
      "TimeInstant": {
        "type": "ISO8601",
        "value": "2018-06-22T04:22:41.606Z"
      }
    }
  },
  "welcome": {
    "type": "string",
    "value": "",
    "metadata": {}
  },
  "handover": {
    "type": "string",
    "value": "",
    "metadata": {}
  },
  "facedetect": {
    "type": "string",
    "value": "",
    "metadata": {}
  },
  "retry": {
    "type": "string",
    "value": "",
    "metadata": {}
  }
}
```

## register cygnus
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: button_sensor" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.cloudconductor.jp/orion/v2/subscriptions/ -X POST -d @- <<__EOS__
{
  "subject": {
    "entities": [{
      "idPattern": "button_sensor.*",
      "type": "button_sensor"
    }]
  },
  "notification": {
    "http": {
      "url": "http://cygnus:5050/notify"
    },
    "attrs": ["state"],
    "attrsFormat": "legacy"
  }
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: button_sensor" -H "Fiware-ServicePath: /" https://api.cloudconductor.jp/orion/v2/subscriptions/ | jq .
[
  {
    "id": "5b2c7ad4c682df4861905ac7",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "button_sensor.*",
          "type": "button_sensor"
        }
      ],
      "condition": {
        "attrs": []
      }
    },
    "notification": {
      "timesSent": 1,
      "lastNotification": "2018-06-22T04:28:04.00Z",
      "attrs": [
        "state"
      ],
      "attrsFormat": "legacy",
      "http": {
        "url": "http://cygnus:5050/notify"
      },
      "lastSuccess": "2018-06-22T04:28:04.00Z"
    }
  }
]
```
```bash
mac:$ kubectl exec mongodb-0 -c mongodb -- mongo sth_button_sensor --eval 'db.getCollection("sth_/_button_sensor_0000000000000001_button_sensor").find()'
MongoDB shell version v3.6.5
connecting to: mongodb://127.0.0.1:27017/sth_button_sensor
MongoDB server version: 3.6.5
{ "_id" : ObjectId("5b2c7bd579828d000af5ae1b"), "recvTime" : ISODate("2018-06-22T04:32:21.299Z"), "attrName" : "state", "attrType" : "string", "attrValue" : "on" }
```

```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.cloudconductor.jp/orion/v2/subscriptions/ -X POST -d @- <<__EOS__
{
  "subject": {
    "entities": [{
      "idPattern": "pepper.*",
      "type": "pepper"
    }]
  },
  "notification": {
    "http": {
      "url": "http://cygnus:5050/notify"
    },
    "attrs": ["dest", "face", "welcome_status", "handover_status", "facedetect_status", "retry_status"],
    "attrsFormat": "legacy"
  }
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-ServicePath: /" https://api.cloudconductor.jp/orion/v2/subscriptions/ | jq .
[
  {
    "id": "5b2c7f073f343a30cd7b65df",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "pepper.*",
          "type": "pepper"
        }
      ],
      "condition": {
        "attrs": []
      }
    },
    "notification": {
      "timesSent": 5,
      "lastNotification": "2018-06-22T04:49:16.00Z",
      "attrs": [
        "dest",
        "face",
        "welcome_status",
        "handover_status",
        "facedetect_status",
        "retry_status"
      ],
      "attrsFormat": "legacy",
      "http": {
        "url": "http://cygnus:5050/notify"
      },
      "lastSuccess": "2018-06-22T04:49:17.00Z"
    }
  }
]
```
```bash
mac:$ kubectl exec mongodb-0 -c mongodb -- mongo sth_pepper --eval 'db.getCollection("sth_/_pepper_0000000000000001_pepper").find()'
{ "_id" : ObjectId("5b2c7fb669d383000a97c3a6"), "recvTime" : ISODate("2018-06-22T04:48:54.951Z"), "attrName" : "facedetect_status", "attrType" : "commandStatus", "attrValue" : "UNKNOWN" }
{ "_id" : ObjectId("5b2c7fb669d383000a97c3a7"), "recvTime" : ISODate("2018-06-22T04:48:54.951Z"), "attrName" : "handover_status", "attrType" : "commandStatus", "attrValue" : "UNKNOWN" }
{ "_id" : ObjectId("5b2c7fb669d383000a97c3a8"), "recvTime" : ISODate("2018-06-22T04:48:54.951Z"), "attrName" : "retry_status", "attrType" : "commandStatus", "attrValue" : "UNKNOWN" }
{ "_id" : ObjectId("5b2c7fb669d383000a97c3a9"), "recvTime" : ISODate("2018-06-22T04:48:54.922Z"), "attrName" : "welcome_status", "attrType" : "commandStatus", "attrValue" : "PENDING" }
{ "_id" : ObjectId("5b2c7fcd79828d000af5ae20"), "recvTime" : ISODate("2018-06-22T04:49:16.996Z"), "attrName" : "facedetect_status", "attrType" : "commandStatus", "attrValue" : "UNKNOWN" }
{ "_id" : ObjectId("5b2c7fcd79828d000af5ae21"), "recvTime" : ISODate("2018-06-22T04:49:16.996Z"), "attrName" : "handover_status", "attrType" : "commandStatus", "attrValue" : "UNKNOWN" }
{ "_id" : ObjectId("5b2c7fcd79828d000af5ae22"), "recvTime" : ISODate("2018-06-22T04:49:16.996Z"), "attrName" : "retry_status", "attrType" : "commandStatus", "attrValue" : "UNKNOWN" }
{ "_id" : ObjectId("5b2c7fcd79828d000af5ae23"), "recvTime" : ISODate("2018-06-22T04:49:16.973Z"), "attrName" : "welcome_status", "attrType" : "commandStatus", "attrValue" : "OK" }
```

## register reception as a subscriber of BUTTON-SENSOR
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: button_sensor" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.cloudconductor.jp/orion/v2/subscriptions/ -X POST -d @- <<__EOS__
{
  "subject": {
    "entities": [{
      "idPattern": "button_sensor.*",
      "type": "button_sensor"
    }],
    "condition": {
      "attrs": ["state"]
    }
  },
  "notification": {
    "http": {
      "url": "http://reception:8888/notify/start-reception/"
    },
    "attrs": ["state"]
  }
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: button_sensor" -H "Fiware-ServicePath: /" https://api.cloudconductor.jp/orion/v2/subscriptions/ | jq .
[
  {
    "id": "5b2c7ad4c682df4861905ac7",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "button_sensor.*",
          "type": "button_sensor"
        }
      ],
      "condition": {
        "attrs": []
      }
    },
    "notification": {
      "timesSent": 2,
      "lastNotification": "2018-06-22T04:32:21.00Z",
      "attrs": [
        "state"
      ],
      "attrsFormat": "legacy",
      "http": {
        "url": "http://cygnus:5050/notify"
      },
      "lastSuccess": "2018-06-22T04:32:21.00Z"
    }
  },
  {
    "id": "5b2c814dc682df4861905ac8",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "button_sensor.*",
          "type": "button_sensor"
        }
      ],
      "condition": {
        "attrs": [
          "state"
        ]
      }
    },
    "notification": {
      "timesSent": 1,
      "lastNotification": "2018-06-22T04:55:41.00Z",
      "attrs": [
        "state"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://reception:8888/notify/start-reception/"
      },
      "lastSuccess": "2018-06-22T04:55:41.00Z"
    }
  }
]
```

## register reception as a subscriber of PEPPER
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.cloudconductor.jp/orion/v2/subscriptions/ -X POST -d @- <<__EOS__
{
  "subject": {
    "entities": [{
      "idPattern": "pepper.*",
      "type": "pepper"
    }],
    "condition": {
      "attrs": ["face", "dest"]
    }
  },
  "notification": {
    "http": {
      "url": "http://reception:8888/notify/finish-reception/"
    },
    "attrs": ["face", "dest"]
  }
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-ServicePath: /" https://api.cloudconductor.jp/orion/v2/subscriptions/ | jq .
[
  {
    "id": "5b31c29b27b17a9c32812b35",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "pepper.*",
          "type": "pepper"
        }
      ],
      "condition": {
        "attrs": []
      }
    },
    "notification": {
      "timesSent": 6,
      "lastNotification": "2018-06-26T08:58:53.00Z",
      "attrs": [
        "dest",
        "face",
        "welcome_status",
        "handover_status",
        "facedetect_status",
        "retry_status"
      ],
      "attrsFormat": "legacy",
      "http": {
        "url": "http://cygnus:5050/notify"
      },
      "lastSuccess": "2018-06-26T08:58:53.00Z"
    }
  },
  {
    "id": "5b3200c4ba29c9f2c7cc1922",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "pepper.*",
          "type": "pepper"
        }
      ],
      "condition": {
        "attrs": [
          "face",
          "dest"
        ]
      }
    },
    "notification": {
      "timesSent": 1,
      "lastNotification": "2018-06-26T09:00:52.00Z",
      "attrs": [
        "face",
        "dest"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://reception:8888/notify/finish-reception/"
      },
      "lastSuccess": "2018-06-26T09:00:52.00Z"
    }
  }
]
```
## register ledger as a subscriber of PEPPER
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.cloudconductor.jp/orion/v2/subscriptions/ -X POST -d @- <<__EOS__
{
  "subject": {
    "entities": [{
      "idPattern": "pepper.*",
      "type": "pepper"
    }],
    "condition": {
      "attrs": ["face", "dest"]
    }
  },
  "notification": {
    "http": {
      "url": "http://ledger:8888/notify/record-reception/"
    },
    "attrs": ["face", "dest"]
  }
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-ServicePath: /" https://api.cloudconductor.jp/orion/v2/subscriptions/ | jq .
[
  {
    "id": "5b31c29b27b17a9c32812b35",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "pepper.*",
          "type": "pepper"
        }
      ],
      "condition": {
        "attrs": []
      }
    },
    "notification": {
      "timesSent": 41,
      "lastNotification": "2018-06-28T00:47:24.00Z",
      "attrs": [
        "dest",
        "face",
        "welcome_status",
        "handover_status",
        "facedetect_status",
        "retry_status"
      ],
      "attrsFormat": "legacy",
      "http": {
        "url": "http://cygnus:5050/notify"
      },
      "lastSuccess": "2018-06-28T00:47:24.00Z"
    }
  },
  {
    "id": "5b3200c4ba29c9f2c7cc1922",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "pepper.*",
          "type": "pepper"
        }
      ],
      "condition": {
        "attrs": [
          "face",
          "dest"
        ]
      }
    },
    "notification": {
      "timesSent": 17,
      "lastNotification": "2018-06-28T00:46:55.00Z",
      "attrs": [
        "face",
        "dest"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://reception:8888/notify/finish-reception/"
      },
      "lastSuccess": "2018-06-28T00:46:55.00Z"
    }
  },
  {
    "id": "5b34324a50a63601fc455002",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "pepper.*",
          "type": "pepper"
        }
      ],
      "condition": {
        "attrs": [
          "face",
          "dest"
        ]
      }
    },
    "notification": {
      "timesSent": 1,
      "lastNotification": "2018-06-28T00:56:42.00Z",
      "attrs": [
        "face",
        "dest"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://ledger:8888/notify/record-reception/"
      },
      "lastSuccess": "2018-06-28T00:56:42.00Z"
    }
  }
]
```
