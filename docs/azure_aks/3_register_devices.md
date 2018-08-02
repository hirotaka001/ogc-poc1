# 3. register devices on AKS

Configure fiware on AKS by following steps:

1. [register "BUTTON-SENSOR" service](#register-button-sensor-service)
1. [register "BUTTON-SENSOR" device](#register-button-sensor-device)
1. [test "BUTTON-SENSOR" attribute](#test-button-sensor-attribute)
1. [register "PEPPER" service](#register-pepper-service)
1. [register "PEPPER" device](#register-pepper-device)
1. [test "PEPPER" command](#test-pepper-command)
1. [test "PEPPER" attribute](#test-pepper-attribute)
1. [register "ROBOT" service](#register-robot-service)
1. [register "ROBOT" device](#register-robot-device)
1. [test "ROBOT" command](#test-robot-command)
1. [test "ROBOT" attribute](#test-robot-attribute)
1. [register "CAMERA" service](#register-camera-service)
1. [register "CAMERA" device](#register-camera-device)
1. [test "CAMERA" command](#test-camera-command)
1. [test "CAMERA" attribute](#test-camera-attribute)
1. [register "DEST-LED" service](#register-dest-led-service)
1. [register "DEST-LED" device](#register-dest-led-device)
1. [test "DEST-LED" command](#test-dest-led-command)
1. [register "DEST-HUMAN-SENSOR" service](#register-dest-human-sensor-service)
1. [register "DEST-HUMAN-SENSOR" device](#register-dest-human-sensor-device)
1. [test "DEST-HUMAN-SENSOR" attribute](#test-dest-human-sensor-attribute)

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

## test PEPPER attribute
```bash
mac:$ mosquitto_sub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /# -u iotagent -P XXXXXXXX
```
```bash
mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /pepper/pepper_0000000000000001/attrs -u iotagent -P XXXXXXXX -m "$d|face|/path/to/face.jpg|dest|destination room"
Client mosqpub|78924-Nobuyukin sending CONNECT
Client mosqpub|78924-Nobuyukin received CONNACK
Client mosqpub|78924-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/attrs', ... (80 bytes))
Client mosqpub|78924-Nobuyukin sending DISCONNECT
```
```bash
mac:$ mosquitto_sub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /# -u iotagent -P XXXXXXXX
...
Client mosqsub|77879-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/attrs', ... (80 bytes))
2018-07-04T09:30:32.1530664232+0900|face|/path/to/face.jpg|dest|destination room
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/pepper_0000000000000001/ | jq .
{
  "id": "pepper_0000000000000001",
  "type": "pepper",
  "TimeInstant": {
    "type": "ISO8601",
    "value": "2018-07-04T09:30:32.1530664232+0900",
    "metadata": {}
  },
  "dest": {
    "type": "string",
    "value": "destination room",
    "metadata": {
      "TimeInstant": {
        "type": "ISO8601",
        "value": "2018-07-04T09:30:32.1530664232+0900"
      }
    }
  },
  "face": {
    "type": "string",
    "value": "/path/to/face.jpg",
    "metadata": {
      "TimeInstant": {
        "type": "ISO8601",
        "value": "2018-07-04T09:30:32.1530664232+0900"
      }
    }
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
        "value": "2018-07-04T00:21:29.759Z"
      }
    }
  },
  "welcome_status": {
    "type": "commandStatus",
    "value": "OK",
    "metadata": {
      "TimeInstant": {
        "type": "ISO8601",
        "value": "2018-07-04T00:21:29.759Z"
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

## register ROBOT service
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/idas/ul20/manage/iot/services/ -X POST -d @- <<__EOS__
{
  "services": [
    {
      "apikey": "guide_robot",
      "cbroker": "http://orion:1026",
      "resource": "/iot/d",
      "entity_type": "guide_robot"
    }
  ]
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /*" https://api.tech-sketch.jp/idas/ul20/manage/iot/services/ | jq .
{
  "count": 1,
  "services": [
    {
      "_id": "5b3b140f714ee900015538f0",
      "subservice": "/",
      "service": "robot",
      "apikey": "guide_robot",
      "resource": "/iot/d",
      "__v": 0,
      "attributes": [],
      "lazy": [],
      "commands": [],
      "entity_type": "guide_robot",
      "internal_attributes": [],
      "static_attributes": []
    }
  ]
}
```

## register ROBOT device
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/idas/ul20/manage/iot/devices/ -X POST -d @- <<__EOS__
{
  "devices": [
    {
      "device_id": "guide_robot_0000000000000001",
      "entity_name": "guide_robot_0000000000000001",
      "entity_type": "guide_robot",
      "timezone": "Asia/Tokyo",
      "protocol": "UL20",
      "attributes": [
        {
          "name": "time",
          "type": "string"
        }, {
          "name": "r_mode",
          "type": "string"
        }, {
          "name": "x",
          "type": "float"
        }, {
          "name": "y",
          "type": "float"
        }, {
          "name": "theta",
          "type": "float"
        }
      ],
      "commands": [
        {
          "name": "robot_request",
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
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/idas/ul20/manage/iot/devices/ -X POST -d @- <<__EOS__
{
  "devices": [
    {
      "device_id": "guide_robot_0000000000000002",
      "entity_name": "guide_robot_0000000000000002",
      "entity_type": "guide_robot",
      "timezone": "Asia/Tokyo",
      "protocol": "UL20",
      "attributes": [
        {
          "name": "time",
          "type": "string"
        }, {
          "name": "r_mode",
          "type": "string"
        }, {
          "name": "x",
          "type": "float"
        }, {
          "name": "y",
          "type": "float"
        }, {
          "name": "theta",
          "type": "float"
        }
      ],
      "commands": [
        {
          "name": "robot_request",
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
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/idas/ul20/manage/iot/devices/guide_robot_0000000000000001/ | jq .
{
  "device_id": "guide_robot_0000000000000001",
  "service": "robot",
  "service_path": "/",
  "entity_name": "guide_robot_0000000000000001",
  "entity_type": "guide_robot",
  "transport": "MQTT",
  "attributes": [
    {
      "object_id": "time",
      "name": "time",
      "type": "string"
    },
    {
      "object_id": "r_mode",
      "name": "r_mode",
      "type": "string"
    },
    {
      "object_id": "x",
      "name": "x",
      "type": "float"
    },
    {
      "object_id": "y",
      "name": "y",
      "type": "float"
    },
    {
      "object_id": "theta",
      "name": "theta",
      "type": "float"
    }
  ],
  "lazy": [],
  "commands": [
    {
      "object_id": "robot_request",
      "name": "robot_request",
      "type": "string"
    }
  ],
  "static_attributes": [],
  "protocol": "UL20"
}
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000001/ | jq .
{
  "id": "guide_robot_0000000000000001",
  "type": "guide_robot",
  "TimeInstant": {
    "type": "ISO8601",
    "value": " ",
    "metadata": {}
  },
  "r_mode": {
    "type": "string",
    "value": " ",
    "metadata": {}
  },
  "robot_request_info": {
    "type": "commandResult",
    "value": " ",
    "metadata": {}
  },
  "robot_request_status": {
    "type": "commandStatus",
    "value": "UNKNOWN",
    "metadata": {}
  },
  "theta": {
    "type": "float",
    "value": " ",
    "metadata": {}
  },
  "time": {
    "type": "string",
    "value": " ",
    "metadata": {}
  },
  "x": {
    "type": "float",
    "value": " ",
    "metadata": {}
  },
  "y": {
    "type": "float",
    "value": " ",
    "metadata": {}
  },
  "robot_request": {
    "type": "string",
    "value": "",
    "metadata": {}
  }
}
```

* check `guide_robot_0000000000000002` by the same procedure.

## test ROBOT command
```bash
mac:$ mosquitto_sub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /# -u iotagent -P XXXXXXXX
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v1/updateContext -d @-<<__EOS__ | jq .
{
  "contextElements": [
    {
      "id": "guide_robot_0000000000000001",
      "isPattern": "false",
      "type": "guide_robot",
      "attributes": [
        {
          "name": "robot_request",
          "value": "r_cmd|Navi|pos.x|123.4|pos.y|-987.6"
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
Client mosqsub|15957-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000001/cmd', ... (78 bytes))
guide_robot_0000000000000001@robot_request|r_cmd|Navi|pos.x|123.4|pos.y|-987.6
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000001/ | jq .
{
  "id": "guide_robot_0000000000000001",
  "type": "guide_robot",
  "TimeInstant": {
    "type": "ISO8601",
    "value": "2018-08-01T02:21:08.00Z",
    "metadata": {}
  },
  "r_mode": {
    "type": "string",
    "value": " ",
    "metadata": {}
  },
  "robot_request_info": {
    "type": "commandResult",
    "value": " ",
    "metadata": {}
  },
  "robot_request_status": {
    "type": "commandStatus",
    "value": "PENDING",
    "metadata": {
      "TimeInstant": {
        "type": "ISO8601",
        "value": "2018-08-01T02:21:08.148Z"
      }
    }
  },
  "theta": {
    "type": "float",
    "value": " ",
    "metadata": {}
  },
  "time": {
    "type": "string",
    "value": " ",
    "metadata": {}
  },
  "x": {
    "type": "float",
    "value": " ",
    "metadata": {}
  },
  "y": {
    "type": "float",
    "value": " ",
    "metadata": {}
  },
  "robot_request": {
    "type": "string",
    "value": "",
    "metadata": {}
  }
}
```
```bash
mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /guide_robot/guide_robot_0000000000000001/cmdexe -u iotagent -P XXXXXXXX -m "guide_robot_0000000000000001@robot_request|result,success/time,2018-08-01 11:21:07/r_cmd,Navi/pos.x,123.4/pos.y,-987.6"
Client mosqpub|80036-Nobuyukin sending CONNECT
Client mosqpub|80036-Nobuyukin received CONNACK
Client mosqpub|80036-Nobuyukin sending PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000001/cmdexe', ... (118 bytes))
Client mosqpub|80036-Nobuyukin sending DISCONNECT
```
```bash
mac:$ mosquitto_sub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /# -u iotagent -P XXXXXXXX
...
Client mosqsub|15957-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000001/cmdexe', ... (118 bytes))
guide_robot_0000000000000001@robot_request|result,success/time,2018-08-01 11:21:07/r_cmd,Navi/pos.x,123.4/pos.y,-987.6
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000001/ | jq .
{
  "id": "guide_robot_0000000000000001",
  "type": "guide_robot",
  "TimeInstant": {
    "type": "ISO8601",
    "value": "2018-08-01T02:21:08.00Z",
    "metadata": {}
  },
  "r_mode": {
    "type": "string",
    "value": " ",
    "metadata": {}
  },
  "robot_request_info": {
    "type": "commandResult",
    "value": "result,success/time,2018-08-01 11:21:07/r_cmd,Navi/pos.x,123.4/pos.y,-987.6",
    "metadata": {
      "TimeInstant": {
        "type": "ISO8601",
        "value": "2018-08-01T02:21:08.148Z"
      }
    }
  },
  "robot_request_status": {
    "type": "commandStatus",
    "value": "OK",
    "metadata": {
      "TimeInstant": {
        "type": "ISO8601",
        "value": "2018-08-01T02:21:08.148Z"
      }
    }
  },
  "theta": {
    "type": "float",
    "value": " ",
    "metadata": {}
  },
  "time": {
    "type": "string",
    "value": " ",
    "metadata": {}
  },
  "x": {
    "type": "float",
    "value": " ",
    "metadata": {}
  },
  "y": {
    "type": "float",
    "value": " ",
    "metadata": {}
  },
  "robot_request": {
    "type": "string",
    "value": "",
    "metadata": {}
  }
}
```

* test `guide_robot_0000000000000002` by the same procedure.

## test ROBOT attribute
```bash
mac:$ mosquitto_sub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /# -u iotagent -P XXXXXXXX
```
```bash
mac$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /guide_robot/guide_robot_0000000000000001/attrs -u iotagent -P XXXXXXXX -m "$d|time|2018-09-08 07:06:05|r_mode|Navi|x|0.1|y|0.2|theta|0.3"
Client mosqpub|80236-Nobuyukin sending CONNECT
Client mosqpub|80236-Nobuyukin received CONNACK
Client mosqpub|80236-Nobuyukin sending PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000001/attrs', ... (90 bytes))
Client mosqpub|80236-Nobuyukin sending DISCONNECT
```
```bash
mac:$ mosquitto_sub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /# -u iotagent -P XXXXXXXX
...
Client mosqsub|15957-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000001/attrs', ... (90 bytes))
2018-08-01T11:28:39.949474+0900|time|2018-09-08 07:06:05|r_mode|Navi|x|0.1|y|0.2|theta|0.3
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000001/ | jq .
{
  "id": "guide_robot_0000000000000001",
  "type": "guide_robot",
  "TimeInstant": {
    "type": "ISO8601",
    "value": "2018-08-01T11:28:39.949474+0900",
    "metadata": {}
  },
  "r_mode": {
    "type": "string",
    "value": "Navi",
    "metadata": {
      "TimeInstant": {
        "type": "ISO8601",
        "value": "2018-08-01T11:28:39.949474+0900"
      }
    }
  },
  "robot_request_info": {
    "type": "commandResult",
    "value": "result,success/time,2018-08-01 11:21:07/r_cmd,Navi/pos.x,123.4/pos.y,-987.6",
    "metadata": {
      "TimeInstant": {
        "type": "ISO8601",
        "value": "2018-08-01T02:21:08.148Z"
      }
    }
  },
  "robot_request_status": {
    "type": "commandStatus",
    "value": "OK",
    "metadata": {
      "TimeInstant": {
        "type": "ISO8601",
        "value": "2018-08-01T02:21:08.148Z"
      }
    }
  },
  "theta": {
    "type": "float",
    "value": "0.3",
    "metadata": {
      "TimeInstant": {
        "type": "ISO8601",
        "value": "2018-08-01T11:28:39.949474+0900"
      }
    }
  },
  "time": {
    "type": "string",
    "value": "2018-09-08 07:06:05",
    "metadata": {
      "TimeInstant": {
        "type": "ISO8601",
        "value": "2018-08-01T11:28:39.949474+0900"
      }
    }
  },
  "x": {
    "type": "float",
    "value": "0.1",
    "metadata": {
      "TimeInstant": {
        "type": "ISO8601",
        "value": "2018-08-01T11:28:39.949474+0900"
      }
    }
  },
  "y": {
    "type": "float",
    "value": "0.2",
    "metadata": {
      "TimeInstant": {
        "type": "ISO8601",
        "value": "2018-08-01T11:28:39.949474+0900"
      }
    }
  },
  "robot_request": {
    "type": "string",
    "value": "",
    "metadata": {}
  }
}
```

* test `guide_robot_0000000000000002` by the same procedure.

## register CAMERA service
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: camera" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/idas/ul20/manage/iot/services/ -X POST -d @- <<__EOS__
{
  "services": [
    {
      "apikey": "external_camera",
      "cbroker": "http://orion:1026",
      "resource": "/iot/d",
      "entity_type": "external_camera"
    }
  ]
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: camera" -H "Fiware-Servicepath: /*" https://api.tech-sketch.jp/idas/ul20/manage/iot/services/ | jq .
{
  "count": 1,
  "services": [
    {
      "_id": "5b3b3152fd223d000164ee62",
      "subservice": "/",
      "service": "camera",
      "apikey": "external_camera",
      "resource": "/iot/d",
      "__v": 0,
      "attributes": [],
      "lazy": [],
      "commands": [],
      "entity_type": "external_camera",
      "internal_attributes": [],
      "static_attributes": []
    }
  ]
}
```

## register CAMERA device
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: camera" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/idas/ul20/manage/iot/devices/ -X POST -d @- <<__EOS__
{
  "devices": [
    {
      "device_id": "external_camera_0000000000000011",
      "entity_name": "external_camera_0000000000000011",
      "entity_type": "external_camera",
      "timezone": "Asia/Tokyo",
      "protocol": "UL20",
      "attributes": [
        {
          "name": "time",
          "type": "string"
        }, {
          "name": "c_mode",
          "type": "string"
        }, {
          "name": "num_p",
          "type": "int"
        }, {
          "name": "position",
          "type": "string"
        }
      ],
      "commands": [
        {
          "name": "external_camera_request",
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
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: camera" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/idas/ul20/manage/iot/devices/ -X POST -d @- <<__EOS__
{
  "devices": [
    {
      "device_id": "external_camera_0000000000000012",
      "entity_name": "external_camera_0000000000000012",
      "entity_type": "external_camera",
      "timezone": "Asia/Tokyo",
      "protocol": "UL20",
      "attributes": [
        {
          "name": "time",
          "type": "string"
        }, {
          "name": "c_mode",
          "type": "string"
        }, {
          "name": "num_p",
          "type": "int"
        }, {
          "name": "position",
          "type": "string"
        }
      ],
      "commands": [
        {
          "name": "external_camera_request",
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
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: camera" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/idas/ul20/manage/iot/devices/ -X POST -d @- <<__EOS__
{
  "devices": [
    {
      "device_id": "external_camera_0000000000000021",
      "entity_name": "external_camera_0000000000000021",
      "entity_type": "external_camera",
      "timezone": "Asia/Tokyo",
      "protocol": "UL20",
      "attributes": [
        {
          "name": "time",
          "type": "string"
        }, {
          "name": "c_mode",
          "type": "string"
        }, {
          "name": "num_p",
          "type": "int"
        }, {
          "name": "position",
          "type": "string"
        }
      ],
      "commands": [
        {
          "name": "external_camera_request",
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
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: camera" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/idas/ul20/manage/iot/devices/external_camera_0000000000000011/ | jq .
{
  "device_id": "external_camera_0000000000000011",
  "service": "camera",
  "service_path": "/",
  "entity_name": "external_camera_0000000000000011",
  "entity_type": "external_camera",
  "transport": "MQTT",
  "attributes": [
    {
      "object_id": "time",
      "name": "time",
      "type": "string"
    },
    {
      "object_id": "c_mode",
      "name": "c_mode",
      "type": "string"
    },
    {
      "object_id": "num_p",
      "name": "num_p",
      "type": "int"
    },
    {
      "object_id": "position",
      "name": "position",
      "type": "string"
    }
  ],
  "lazy": [],
  "commands": [
    {
      "object_id": "external_camera_request",
      "name": "external_camera_request",
      "type": "string"
    }
  ],
  "static_attributes": [],
  "protocol": "UL20"
}
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: camera" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/external_camera_0000000000000011/ | jq .
{
  "id": "external_camera_0000000000000011",
  "type": "external_camera",
  "TimeInstant": {
    "type": "ISO8601",
    "value": " ",
    "metadata": {}
  },
  "c_mode": {
    "type": "string",
    "value": " ",
    "metadata": {}
  },
  "external_camera_request_info": {
    "type": "commandResult",
    "value": " ",
    "metadata": {}
  },
  "external_camera_request_status": {
    "type": "commandStatus",
    "value": "UNKNOWN",
    "metadata": {}
  },
  "num_p": {
    "type": "int",
    "value": " ",
    "metadata": {}
  },
  "position": {
    "type": "string",
    "value": " ",
    "metadata": {}
  },
  "time": {
    "type": "string",
    "value": " ",
    "metadata": {}
  },
  "external_camera_request": {
    "type": "string",
    "value": "",
    "metadata": {}
  }
}
```

* check `external_camera_0000000000000012` and `external_camera_0000000000000021` by the same procedure.

## test CAMERA command
```bash
mac:$ mosquitto_sub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /# -u iotagent -P XXXXXXXX
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: camera" -H "Fiware-Servicepath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v1/updateContext -d @-<<__EOS__ | jq .
{
  "contextElements": [
    {
      "id": "external_camera_0000000000000011",
      "isPattern": "false",
      "type": "external_camera",
      "attributes": [
        {
          "name": "external_camera_request",
          "value": "c_cmd|Monitor"
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
Client mosqsub|77879-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/external_camera/external_camera/cmd', ... (65 bytes))
external_camera_0000000000000011@external_camera_request|c_cmd|Monitor
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: camera" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/external_camera_0000000000000011/ | jq .
{
  "id": "external_camera_0000000000000011",
  "type": "external_camera",
  "TimeInstant": {
    "type": "ISO8601",
    "value": "2018-07-31T23:34:35.00Z",
    "metadata": {}
  },
  "c_mode": {
    "type": "string",
    "value": " ",
    "metadata": {}
  },
  "external_camera_request_info": {
    "type": "commandResult",
    "value": " ",
    "metadata": {}
  },
  "external_camera_request_status": {
    "type": "commandStatus",
    "value": "PENDING",
    "metadata": {
      "TimeInstant": {
        "type": "ISO8601",
        "value": "2018-07-04T03:37:05.023Z"
      }
    }
  },
  "num_p": {
    "type": "int",
    "value": " ",
    "metadata": {}
  },
  "position": {
    "type": "string",
    "value": " ",
    "metadata": {}
  },
  "time": {
    "type": "string",
    "value": " ",
    "metadata": {}
  },
  "external_camera_request": {
    "type": "string",
    "value": "",
    "metadata": {}
  }
}
```
```bash
$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /external_camera/external_camera/cmdexe -u iotagent -P XXXXXXXX -m "external_camera_0000000000000011@external_camera_request|result,success/time,2018-08-01 08:34:32/c_cmd,Monitor"
Client mosqpub|81501-Nobuyukin sending CONNECT
Client mosqpub|81501-Nobuyukin received CONNACK
Client mosqpub|81501-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/external_camera/external_camera_0000000000000011/cmdexe', ... (110 bytes))
Client mosqpub|81501-Nobuyukin sending DISCONNECT
```
```bash
mac:$ mosquitto_sub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /# -u iotagent -P XXXXXXXX
...
Client mosqsub|6747-Nobuyukino received PUBLISH (d0, q0, r0, m0, '/external_camera/external_camera_0000000000000011/cmdexe', ... (110 bytes))
external_camera_0000000000000011@external_camera_request|result,success/time,2018-08-01 08:34:32/c_cmd,Monitor
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: camera" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/external_camera_0000000000000011/ | jq .
{
  "id": "external_camera_0000000000000011",
  "type": "external_camera",
  "TimeInstant": {
    "type": "ISO8601",
    "value": "2018-07-31T23:34:35.00Z",
    "metadata": {}
  },
  "c_mode": {
    "type": "string",
    "value": " ",
    "metadata": {}
  },
  "external_camera_request_info": {
    "type": "commandResult",
    "value": "result,success/time,2018-08-01 08:34:32/c_cmd,Monitor",
    "metadata": {
      "TimeInstant": {
        "type": "ISO8601",
        "value": "2018-07-31T23:34:35.231Z"
      }
    }
  },
  "external_camera_request_status": {
    "type": "commandStatus",
    "value": "OK",
    "metadata": {
      "TimeInstant": {
        "type": "ISO8601",
        "value": "2018-07-31T23:34:35.231Z"
      }
    }
  },
  "num_p": {
    "type": "int",
    "value": " ",
    "metadata": {}
  },
  "position": {
    "type": "string",
    "value": " ",
    "metadata": {}
  },
  "time": {
    "type": "string",
    "value": " ",
    "metadata": {}
  },
  "external_camera_request": {
    "type": "string",
    "value": "",
    "metadata": {}
  }
}
```

* test `external_camera_0000000000000012` and `external_camera_0000000000000021` by the same procedure.


## test CAMERA attribute
```bash
mac:$ mosquitto_sub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /# -u iotagent -P XXXXXXXX
```
```bash
$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /external_camera/external_camera_0000000000000011/attrs -u iotagent -P XXXXXXXX -m "$d|time|2018-01-02 03:04:05|c_mode|Monitor|num_p|1|position|x[0],1.12/y[0],-95.1"
Client mosqpub|82032-Nobuyukin sending CONNECT
Client mosqpub|82032-Nobuyukin received CONNACK
Client mosqpub|82032-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/external_camera/external_camera_0000000000000011/attrs', ... (109 bytes))
Client mosqpub|82032-Nobuyukin sending DISCONNECT
```
```bash
mac:$ mosquitto_sub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /# -u iotagent -P XXXXXXXX
...
Client mosqsub|7354-Nobuyukino received PUBLISH (d0, q0, r0, m0, '/external_camera/external_camera_0000000000000011/attrs', ... (109 bytes))
2018-08-01T09:07:17.010090+0900|time|2018-01-02 03:04:05|c_mode|Monitor|num_p|1|position|x[0],1.12/y[0],-95.1
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: camera" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/external_camera_0000000000000011/ | jq .
{
  "id": "external_camera_0000000000000011",
  "type": "external_camera",
  "TimeInstant": {
    "type": "ISO8601",
    "value": "2018-08-01T09:07:17.010090+0900",
    "metadata": {}
  },
  "c_mode": {
    "type": "string",
    "value": "Monitor",
    "metadata": {
      "TimeInstant": {
        "type": "ISO8601",
        "value": "2018-08-01T09:07:17.010090+0900"
      }
    }
  },
  "external_camera_request_info": {
    "type": "commandResult",
    "value": "result,success/time,2018-08-01 08:34:32/c_cmd,Monitor",
    "metadata": {
      "TimeInstant": {
        "type": "ISO8601",
        "value": "2018-07-31T23:34:35.231Z"
      }
    }
  },
  "external_camera_request_status": {
    "type": "commandStatus",
    "value": "OK",
    "metadata": {
      "TimeInstant": {
        "type": "ISO8601",
        "value": "2018-07-31T23:34:35.231Z"
      }
    }
  },
  "num_p": {
    "type": "int",
    "value": "1",
    "metadata": {
      "TimeInstant": {
        "type": "ISO8601",
        "value": "2018-08-01T09:07:17.010090+0900"
      }
    }
  },
  "position": {
    "type": "string",
    "value": "x[0],1.12/y[0],-95.1",
    "metadata": {
      "TimeInstant": {
        "type": "ISO8601",
        "value": "2018-08-01T09:07:17.010090+0900"
      }
    }
  },
  "time": {
    "type": "string",
    "value": "2018-01-02 03:04:05",
    "metadata": {
      "TimeInstant": {
        "type": "ISO8601",
        "value": "2018-08-01T09:07:17.010090+0900"
      }
    }
  },
  "external_camera_request": {
    "type": "string",
    "value": "",
    "metadata": {}
  }
}
```

* test `external_camera_0000000000000012` and `external_camera_0000000000000021` by the same procedure.

## register DEST-LED service
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: dest_led" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/idas/ul20/manage/iot/services/ -X POST -d @- <<__EOS__
{
  "services": [
    {
      "apikey": "dest_led",
      "cbroker": "http://orion:1026",
      "resource": "/iot/d",
      "entity_type": "dest_led"
    }
  ]
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: dest_led" -H "Fiware-Servicepath: /*" https://api.tech-sketch.jp/idas/ul20/manage/iot/services/ | jq .
{
  "count": 1,
  "services": [
    {
      "_id": "5b3c72acab13130001647100",
      "subservice": "/",
      "service": "dest_led",
      "apikey": "dest_led",
      "resource": "/iot/d",
      "__v": 0,
      "attributes": [],
      "lazy": [],
      "commands": [],
      "entity_type": "dest_led",
      "internal_attributes": [],
      "static_attributes": []
    }
  ]
}
```

## register DEST-LED device
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: dest_led" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/idas/ul20/manage/iot/devices/ -X POST -d @- <<__EOS__
{
  "devices": [
    {
      "device_id": "dest_led_0000000000000001",
      "entity_name": "dest_led_0000000000000001",
      "entity_type": "dest_led",
      "timezone": "Asia/Tokyo",
      "protocol": "UL20",
      "commands": [
        {
          "name": "action",
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
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: dest_led" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/idas/ul20/manage/iot/devices/ -X POST -d @- <<__EOS__
{
  "devices": [
    {
      "device_id": "dest_led_0000000000000002",
      "entity_name": "dest_led_0000000000000002",
      "entity_type": "dest_led",
      "timezone": "Asia/Tokyo",
      "protocol": "UL20",
      "commands": [
        {
          "name": "action",
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
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: dest_led" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/idas/ul20/manage/iot/devices/dest_led_0000000000000001/ | jq .
{
  "device_id": "dest_led_0000000000000001",
  "service": "dest_led",
  "service_path": "/",
  "entity_name": "dest_led_0000000000000001",
  "entity_type": "dest_led",
  "transport": "MQTT",
  "attributes": [],
  "lazy": [],
  "commands": [
    {
      "object_id": "action",
      "name": "action",
      "type": "string"
    }
  ],
  "static_attributes": [],
  "protocol": "UL20"
}
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: dest_led" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/dest_led_0000000000000001/ | jq .
{
  "id": "dest_led_0000000000000001",
  "type": "dest_led",
  "TimeInstant": {
    "type": "ISO8601",
    "value": "2018-07-04T07:35:09.00Z",
    "metadata": {}
  },
  "action_info": {
    "type": "commandResult",
    "value": " ",
    "metadata": {}
  },
  "action_status": {
    "type": "commandStatus",
    "value": "UNKNOWN",
    "metadata": {}
  },
  "action": {
    "type": "string",
    "value": "",
    "metadata": {}
  }
}
```

* check `dest_led_0000000000000002` by the same procedure.

## test DEST-LED command
```bash
mac:$ mosquitto_sub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /# -u iotagent -P XXXXXXXX
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: dest_led" -H "Fiware-Servicepath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v1/updateContext -d @-<<__EOS__ | jq .
{
  "contextElements": [
    {
      "id": "dest_led_0000000000000001",
      "isPattern": "false",
      "type": "dest_led",
      "attributes": [
        {
          "name": "action",
          "value": "on"
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
Client mosqsub|90898-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/dest_led/dest_led_0000000000000001/cmd', ... (35 bytes))
dest_led_0000000000000001@action|on
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: dest_led" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/dest_led_0000000000000001/ | jq .
{
  "id": "dest_led_0000000000000001",
  "type": "dest_led",
  "TimeInstant": {
    "type": "ISO8601",
    "value": "2018-07-04T07:38:06.00Z",
    "metadata": {}
  },
  "action_info": {
    "type": "commandResult",
    "value": " ",
    "metadata": {}
  },
  "action_status": {
    "type": "commandStatus",
    "value": "PENDING",
    "metadata": {
      "TimeInstant": {
        "type": "ISO8601",
        "value": "2018-07-04T07:38:06.470Z"
      }
    }
  },
  "action": {
    "type": "string",
    "value": "",
    "metadata": {}
  }
}
```
```bash
mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /dest_led/dest_led_0000000000000001/cmdexe -u iotagent -P XXXXXXXX -m "dest_led_0000000000000001@action|success"
Client mosqpub|43968-Nobuyukin sending CONNECT
Client mosqpub|43968-Nobuyukin received CONNACK
Client mosqpub|43968-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/dest_led/dest_led_0000000000000001/cmdexe', ... (40 bytes))
Client mosqpub|43968-Nobuyukin sending DISCONNECT
```
```bash
mac:$ mosquitto_sub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /# -u iotagent -P XXXXXXXX
...
Client mosqsub|90898-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/dest_led/dest_led_0000000000000001/cmdexe', ... (40 bytes))
dest_led_0000000000000001@action|success
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: dest_led" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/dest_led_0000000000000001/ | jq .
{
  "id": "dest_led_0000000000000001",
  "type": "dest_led",
  "TimeInstant": {
    "type": "ISO8601",
    "value": "2018-07-04T07:40:04.00Z",
    "metadata": {}
  },
  "action_info": {
    "type": "commandResult",
    "value": "success",
    "metadata": {
      "TimeInstant": {
        "type": "ISO8601",
        "value": "2018-07-04T07:40:04.779Z"
      }
    }
  },
  "action_status": {
    "type": "commandStatus",
    "value": "OK",
    "metadata": {
      "TimeInstant": {
        "type": "ISO8601",
        "value": "2018-07-04T07:40:04.779Z"
      }
    }
  },
  "action": {
    "type": "string",
    "value": "",
    "metadata": {}
  }
}
```

* test `dest_led_0000000000000002` by the same procedure.

## register DEST-HUMAN-SENSOR service
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: dest_human_sensor" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/idas/ul20/manage/iot/services/ -X POST -d @- <<__EOS__
{
  "services": [
    {
      "apikey": "dest_human_sensor",
      "cbroker": "http://orion:1026",
      "resource": "/iot/d",
      "entity_type": "dest_human_sensor"
    }
  ]
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: dest_human_sensor" -H "Fiware-Servicepath: /*" https://api.tech-sketch.jp/idas/ul20/manage/iot/services/ | jq .
{
  "count": 1,
  "services": [
    {
      "_id": "5b3d7595743a010001e250ad",
      "subservice": "/",
      "service": "dest_human_sensor",
      "apikey": "dest_human_sensor",
      "resource": "/iot/d",
      "__v": 0,
      "attributes": [],
      "lazy": [],
      "commands": [],
      "entity_type": "dest_human_sensor",
      "internal_attributes": [],
      "static_attributes": []
    }
  ]
}
```

## register DEST-HUMAN-SENSOR device
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: dest_human_sensor" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/idas/ul20/manage/iot/devices/ -X POST -d @- <<__EOS__
{
  "devices": [
    {
      "device_id": "dest_human_sensor_0000000000000001",
      "entity_name": "dest_human_sensor_0000000000000001",
      "entity_type": "dest_human_sensor",
      "timezone": "Asia/Tokyo",
      "protocol": "UL20",
      "attributes": [
        {
          "name": "arrival",
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
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: dest_human_sensor" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/idas/ul20/manage/iot/devices/ -X POST -d @- <<__EOS__
{
  "devices": [
    {
      "device_id": "dest_human_sensor_0000000000000002",
      "entity_name": "dest_human_sensor_0000000000000002",
      "entity_type": "dest_human_sensor",
      "timezone": "Asia/Tokyo",
      "protocol": "UL20",
      "attributes": [
        {
          "name": "arrival",
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
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: dest_human_sensor" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/idas/ul20/manage/iot/devices/dest_human_sensor_0000000000000001/ | jq .
{
  "device_id": "dest_human_sensor_0000000000000001",
  "service": "dest_human_sensor",
  "service_path": "/",
  "entity_name": "dest_human_sensor_0000000000000001",
  "entity_type": "dest_human_sensor",
  "transport": "MQTT",
  "attributes": [
    {
      "object_id": "arrival",
      "name": "arrival",
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
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: dest_human_sensor" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/dest_human_sensor_0000000000000001/ | jq .
{
  "id": "dest_human_sensor_0000000000000001",
  "type": "dest_human_sensor",
  "TimeInstant": {
    "type": "ISO8601",
    "value": " ",
    "metadata": {}
  },
  "arrival": {
    "type": "string",
    "value": " ",
    "metadata": {}
  }
}
```

* check `dest_human_sensor_0000000000000002` by the same procedure.

## test DEST-HUMAN-SENSOR attribute
```bash
mac:$ mosquitto_sub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /# -u iotagent -P XXXXXXXX
```
```bash
mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /dest_human_sensor/dest_human_sensor_0000000000000001/attrs -u iotagent -P XXXXXXXX -m "$d|arrival|$d"
Client mosqpub|59075-Nobuyukin sending CONNECT
Client mosqpub|59075-Nobuyukin received CONNACK
Client mosqpub|59075-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/dest_human_sensor/dest_human_sensor_0000000000000001/attrs', ... (79 bytes))
Client mosqpub|59075-Nobuyukin sending DISCONNECT
```
```bash
mac:$ mosquitto_sub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /# -u iotagent -P XXXXXXXX
...
lient mosqsub|58138-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/dest_human_sensor/dest_human_sensor_0000000000000001/attrs', ... (79 bytes))
2018-07-05T10:41:52.1530754912+0900|arrival|2018-07-05T10:41:52.1530754912+0900
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: dest_human_sensor" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/dest_human_sensor_0000000000000001/ | jq .
{
  "id": "dest_human_sensor_0000000000000001",
  "type": "dest_human_sensor",
  "TimeInstant": {
    "type": "ISO8601",
    "value": "2018-07-05T10:41:52.1530754912+0900",
    "metadata": {}
  },
  "arrival": {
    "type": "string",
    "value": "2018-07-05T10:41:52.1530754912+0900",
    "metadata": {
      "TimeInstant": {
        "type": "ISO8601",
        "value": "2018-07-05T10:41:52.1530754912+0900"
      }
    }
  }
}
```

* test `dest_human_sensor_0000000000000002` by the same procedure.
