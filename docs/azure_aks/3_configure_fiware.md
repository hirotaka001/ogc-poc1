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

## register BUTTON-SENSOR service
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: button_sensor" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/idas/ul20/manage/iot/services/ -X POST -d @- <<__EOS__
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
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: button_sensor" -H "Fiware-Servicepath: /*" https://api.tech-sketch.jp/idas/ul20/manage/iot/services/ | jq .
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
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: button_sensor" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/idas/ul20/manage/iot/devices/ -X POST -d @- <<__EOS__
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
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: button_sensor" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/idas/ul20/manage/iot/devices/button_sensor_0000000000000001/ | jq .
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
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: button_sensor" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/button_sensor_0000000000000001/ | jq .
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
mac:$ mosquitto_sub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /# -u iotagent -P XXXXXXXX
```
```bash
mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /button_sensor/button_sensor_0000000000000001/attrs -u iotagent -P XXXXXXXX -m "$d|state|on"
Client mosqpub|92108-Nobuyukin sending CONNECT
Client mosqpub|92108-Nobuyukin received CONNACK
Client mosqpub|92108-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/button_sensor/button_sensor_0000000000000001/attrs', ... (44 bytes))
Client mosqpub|92108-Nobuyukin sending DISCONNECT
```
```bash
mac:$ mosquitto_sub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /# -u iotagent -P XXXXXXXX
...
Client mosqsub|18252-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/button_sensor/button_sensor_0000000000000001/attrs', ... (44 bytes))
2018-06-29T10:34:30.1530236070+0900|state|on
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: button_sensor" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/button_sensor_0000000000000001/ | jq .
{
  "id": "button_sensor_0000000000000001",
  "type": "button_sensor",
  "TimeInstant": {
    "type": "ISO8601",
    "value": "2018-06-29T10:34:30.1530236070+0900",
    "metadata": {}
  },
  "state": {
    "type": "string",
    "value": "on",
    "metadata": {
      "TimeInstant": {
        "type": "ISO8601",
        "value": "2018-06-29T10:34:30.1530236070+0900"
      }
    }
  }
}
```

## register PEPPER service
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/idas/ul20/manage/iot/services/ -X POST -d @- <<__EOS__
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
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-Servicepath: /*" https://api.tech-sketch.jp/idas/ul20/manage/iot/services/ | jq .
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
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/idas/ul20/manage/iot/devices/ -X POST -d @- <<__EOS__
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
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/idas/ul20/manage/iot/devices/ -X POST -d @- <<__EOS__
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
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/idas/ul20/manage/iot/devices/ | jq .
{
  "count": 2,
  "devices": [
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
    },
    {
      "device_id": "pepper_0000000000000002",
      "service": "pepper",
      "service_path": "/",
      "entity_name": "pepper_0000000000000002",
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
  ]
}
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/ | jq .
[
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
  },
  {
    "id": "pepper_0000000000000002",
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
]
```

## test PEPPER command
```bash
mac:$ mosquitto_sub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /# -u iotagent -P XXXXXXXX
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-Servicepath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v1/updateContext -d @-<<__EOS__ | jq .
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
mac:$ mosquitto_sub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /# -u iotagent -P XXXXXXXX
...
Client mosqsub|18252-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/cmd', ... (37 bytes))
pepper_0000000000000001@welcome|start
```
```bash
$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/pepper_0000000000000001/ | jq .
{
  "id": "pepper_0000000000000001",
  "type": "pepper",
  "TimeInstant": {
    "type": "ISO8601",
    "value": "2018-06-29T01:38:36.00Z",
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
        "value": "2018-06-29T01:57:29.219Z"
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
mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /pepper/pepper_0000000000000001/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000001@welcome|start exec"
Client mosqpub|92385-Nobuyukin sending CONNECT
Client mosqpub|92385-Nobuyukin received CONNACK
Client mosqpub|92385-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/cmdexe', ... (42 bytes))
Client mosqpub|92385-Nobuyukin sending DISCONNECT
```
```bash
mac:$ mosquitto_sub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /# -u iotagent -P XXXXXXXX
...
Client mosqsub|18252-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/cmdexe', ... (42 bytes))
pepper_0000000000000001@welcome|start exec
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/pepper_0000000000000001/ | jq .
{
  "id": "pepper_0000000000000001",
  "type": "pepper",
  "TimeInstant": {
    "type": "ISO8601",
    "value": "2018-06-29T01:58:40.00Z",
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
        "value": "2018-06-29T01:58:40.946Z"
      }
    }
  },
  "welcome_status": {
    "type": "commandStatus",
    "value": "OK",
    "metadata": {
      "TimeInstant": {
        "type": "ISO8601",
        "value": "2018-06-29T01:58:40.946Z"
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
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: button_sensor" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v2/subscriptions/ -X POST -d @- <<__EOS__
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
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: button_sensor" -H "Fiware-ServicePath: /" https://api.tech-sketch.jp/orion/v2/subscriptions/ | jq .
[
  {
    "id": "5b358ed7cabb3e96b43251ba",
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
      "lastNotification": "2018-06-29T01:43:51.00Z",
      "attrs": [
        "state"
      ],
      "attrsFormat": "legacy",
      "http": {
        "url": "http://cygnus:5050/notify"
      },
      "lastSuccess": "2018-06-29T01:43:51.00Z"
    }
  }
]
```
```bash
mac:$ kubectl exec mongodb-0 -c mongodb -- mongo sth_button_sensor --eval 'db.getCollection("sth_/_button_sensor_0000000000000001_button_sensor").find()'
MongoDB shell version v3.6.5
connecting to: mongodb://127.0.0.1:27017/sth_button_sensor
MongoDB server version: 3.6.5
{ "_id" : ObjectId("5b358ed7f13180000ab627fc"), "recvTime" : ISODate("2018-06-29T01:43:51.699Z"), "attrName" : "state", "attrType" : "string", "attrValue" : "on" }
```

```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v2/subscriptions/ -X POST -d @- <<__EOS__
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
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-ServicePath: /" https://api.tech-sketch.jp/orion/v2/subscriptions/ | jq .
[
  {
    "id": "5b3590a707f08f3a3ac62b58",
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
      "lastNotification": "2018-06-29T01:58:40.00Z",
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
      "lastSuccess": "2018-06-29T01:58:40.00Z"
    }
  }
]
```
```bash
$ kubectl exec mongodb-0 -c mongodb -- mongo sth_pepper --eval 'db.getCollection("sth_/_pepper_0000000000000001_pepper").find({"attrName": "welcome_status"})'
MongoDB shell version v3.6.5
connecting to: mongodb://127.0.0.1:27017/sth_pepper
MongoDB server version: 3.6.5
{ "_id" : ObjectId("5b359209169675000a7aebcd"), "recvTime" : ISODate("2018-06-29T01:57:29.219Z"), "attrName" : "welcome_status", "attrType" : "commandStatus", "attrValue" : "PENDING" }
{ "_id" : ObjectId("5b359250169675000a7aebd1"), "recvTime" : ISODate("2018-06-29T01:58:40.946Z"), "attrName" : "welcome_status", "attrType" : "commandStatus", "attrValue" : "OK" }
```

## register `start-reception` of reception as a subscriber of BUTTON-SENSOR
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: button_sensor" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v2/subscriptions/ -X POST -d @- <<__EOS__
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
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: button_sensor" -H "Fiware-ServicePath: /" https://api.tech-sketch.jp/orion/v2/subscriptions/ | jq .
[
  {
    "id": "5b358ed7cabb3e96b43251ba",
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
      "lastNotification": "2018-06-29T01:43:51.00Z",
      "attrs": [
        "state"
      ],
      "attrsFormat": "legacy",
      "http": {
        "url": "http://cygnus:5050/notify"
      },
      "lastSuccess": "2018-06-29T01:43:51.00Z"
    }
  },
  {
    "id": "5b35932607f08f3a3ac62b59",
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
      "lastNotification": "2018-06-29T02:02:14.00Z",
      "attrs": [
        "state"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://reception:8888/notify/start-reception/"
      },
      "lastSuccess": "2018-06-29T02:02:14.00Z"
    }
  }
]
```

## register `finish-reception` of reception as a subscriber of PEPPER
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v2/subscriptions/ -X POST -d @- <<__EOS__
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
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-ServicePath: /" https://api.tech-sketch.jp/orion/v2/subscriptions/ | jq .
[
  {
    "id": "5b3590a707f08f3a3ac62b58",
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
      "lastNotification": "2018-06-29T02:02:14.00Z",
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
      "lastSuccess": "2018-06-29T02:02:14.00Z"
    }
  },
  {
    "id": "5b35935fcabb3e96b43251bb",
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
      "lastNotification": "2018-06-29T02:03:11.00Z",
      "attrs": [
        "face",
        "dest"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://reception:8888/notify/finish-reception/"
      },
      "lastSuccess": "2018-06-29T02:03:11.00Z"
    }
  }
]
```

## register `record-reception` of ledger as a subscriber of PEPPER
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v2/subscriptions/ -X POST -d @- <<__EOS__
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
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-ServicePath: /" https://api.tech-sketch.jp/orion/v2/subscriptions/ | jq .
[
  {
    "id": "5b3590a707f08f3a3ac62b58",
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
      "lastNotification": "2018-06-29T02:02:14.00Z",
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
      "lastSuccess": "2018-06-29T02:02:14.00Z"
    }
  },
  {
    "id": "5b35935fcabb3e96b43251bb",
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
      "lastNotification": "2018-06-29T02:03:11.00Z",
      "attrs": [
        "face",
        "dest"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://reception:8888/notify/finish-reception/"
      },
      "lastSuccess": "2018-06-29T02:03:11.00Z"
    }
  },
  {
    "id": "5b35944007f08f3a3ac62b5a",
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
      "lastNotification": "2018-06-29T02:06:56.00Z",
      "attrs": [
        "face",
        "dest"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://ledger:8888/notify/record-reception/"
      }
    }
  }
]
```
