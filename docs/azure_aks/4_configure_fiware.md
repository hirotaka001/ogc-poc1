# 4. configure fiware on AKS

Configure fiware on AKS by following steps:

1. [register "BUTTON-SENSOR" to cygnus](#register-button-sensor-to-cygnus)
1. [register "PEPPER" to cygnus](#register-pepper-to-cygnus)
1. [register "ROBOT" to cygnus](#register-robot-to-cygnus)
1. [register "CAMERA" to cygnus](#register-camera-to-cygnus)
1. [register "DEST-LED" to cygnus](#register-dest-led-to-cygnus)
1. [register "DEST-HUMAN-SENSOR" to cygnus](#register-dest-human-sensor-to-cygnus)
1. [register `start-reception` of "reception" as a subscriber of "BUTTON-SENSOR"](#register-start-reception-of-reception-as-a-subscriber-of-button-sensor)
1. [register `finish-reception` of "reception" as a subscriber of "PEPPER"](#register-finish-reception-of-reception-as-a-subscriber-of-pepper)
1. [register `record-reception` of "ledger" as a subscriber of "PEPPER"](#register-record-reception-of-ledger-as-a-subscriber-of-pepper)
1. [register `detect-visitor` of "ledger" as a subscriber of "PEPPER"](#register-detect-visitor-of-ledger-as-a-subscriber-of-pepper)
1. [register `reask-destination` of "ledger" as a subscriber of "PEPPER"](#register-reask-destination-of-ledger-as-a-subscriber-of-pepper)
1. [register `start_movement` entity](#register-stert_movement-entity)
1. [register `start-movement` of "guidance" as a subscriber of `start_movement`](#register-start-movement-of-guidance-as-a-subscriber-of-start_movement)
1. [register cygnus as as subscriber of `start_movement`](#register-cygnus-as-a-subscriber-of-start_movement)
1. [register `check-destination` of "guidance" as a subscriber of "ROBOT"](#register-check-destination-of-guidance-as-a-subscriber-of-robot)
1. [register `stop-movement` of "guidance" as a subscriber of "ROBOT"](#register-stop-movement-of-guidance-as-a-subscriber-of-robot)
1. [register `record-arrival` of "ledger" as a subscriber of "DEST-HUMAN-SENSOR"](#register-record-arrival-of-ledger-as-a-subscriber-of-dest-human-sensor)
1. [register `arrival` of "guidance" as a subscriber of "DEST-HUMAN-SENSOR"](#register-arrival-of-guidance-as-a-subscriber-of-dest-human-sensor)
1. [register desinations](#register-destinations)

## register BUTTON-SENSOR to cygnus
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
    "id": "5b3c41f0d31a6404acc0ae2c",
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
      "lastNotification": "2018-07-04T03:41:36.00Z",
      "attrs": [
        "state"
      ],
      "attrsFormat": "legacy",
      "http": {
        "url": "http://cygnus:5050/notify"
      },
      "lastSuccess": "2018-07-04T03:41:36.00Z"
    }
  }
]
```
```bash
mac:$ kubectl exec mongodb-0 -c mongodb -- mongo sth_button_sensor --eval 'db.getCollection("sth_/_button_sensor_0000000000000001_button_sensor").find()'
MongoDB shell version v3.6.5
connecting to: mongodb://127.0.0.1:27017/sth_button_sensor
MongoDB server version: 3.6.5
{ "_id" : ObjectId("5b3c41f223b570000ae53ba3"), "recvTime" : ISODate("2018-07-04T03:41:36.668Z"), "attrName" : "state", "attrType" : "string", "attrValue" : "on" }
```

## register PEPPER to cygnus
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
    "id": "5b3c43d4f1bdbe368d81d4c1",
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
      "timesSent": 1,
      "lastNotification": "2018-07-04T03:49:40.00Z",
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
      "lastSuccess": "2018-07-04T03:49:40.00Z"
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

## register ROBOT to cygnus
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v2/subscriptions/ -X POST -d @- <<__EOS__
{
  "subject": {
    "entities": [{
      "idPattern": "guide_robot.*",
      "type": "guide_robot"
    }]
  },
  "notification": {
    "http": {
      "url": "http://cygnus:5050/notify"
    },
    "attrs": [
      "time",
      "r_mode",
      "x",
      "y",
      "theta",
      "robot_request_status",
      "robot_request_info"
    ],
    "attrsFormat": "legacy"
  }
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-ServicePath: /" https://api.tech-sketch.jp/orion/v2/subscriptions/ | jq .
[
  {
    "id": "5b611c4cbc0be89f5baac3d3",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "guide_robot.*",
          "type": "guide_robot"
        }
      ],
      "condition": {
        "attrs": []
      }
    },
    "notification": {
      "timesSent": 1,
      "lastNotification": "2018-08-01T02:34:52.00Z",
      "attrs": [
        "time",
        "r_mode",
        "x",
        "y",
        "theta",
        "robot_request_status",
        "robot_request_info"
      ],
      "attrsFormat": "legacy",
      "http": {
        "url": "http://cygnus:5050/notify"
      },
      "lastSuccess": "2018-08-01T02:34:52.00Z"
    }
  }
]
```
```bash
mac:$ kubectl exec mongodb-0 -c mongodb -- mongo sth_robot --eval 'db.getCollection("sth_/_guide_robot_0000000000000001_guide_robot").find()'
MongoDB shell version v3.6.5
connecting to: mongodb://127.0.0.1:27017/sth_robot
MongoDB server version: 3.6.5
{ "_id" : ObjectId("5b611c88c22929000a69fe9c"), "recvTime" : ISODate("2018-08-01T02:35:52.628Z"), "attrName" : "r_mode", "attrType" : "string", "attrValue" : "Navi" }
{ "_id" : ObjectId("5b611c88c22929000a69fe9d"), "recvTime" : ISODate("2018-08-01T02:21:08.148Z"), "attrName" : "robot_request_info", "attrType" : "commandResult", "attrValue" : "result,success/time,2018-08-01 11:21:07/r_cmd,Navi/pos.x,123.4/pos.y,-987.6" }
{ "_id" : ObjectId("5b611c88c22929000a69fe9e"), "recvTime" : ISODate("2018-08-01T02:21:08.148Z"), "attrName" : "robot_request_status", "attrType" : "commandStatus", "attrValue" : "OK" }
{ "_id" : ObjectId("5b611c88c22929000a69fe9f"), "recvTime" : ISODate("2018-08-01T02:35:52.628Z"), "attrName" : "theta", "attrType" : "float", "attrValue" : "0.3" }
{ "_id" : ObjectId("5b611c88c22929000a69fea0"), "recvTime" : ISODate("2018-08-01T02:35:52.628Z"), "attrName" : "time", "attrType" : "string", "attrValue" : "2018-09-08 07:06:05" }
{ "_id" : ObjectId("5b611c88c22929000a69fea1"), "recvTime" : ISODate("2018-08-01T02:35:52.628Z"), "attrName" : "x", "attrType" : "float", "attrValue" : "0.1" }
{ "_id" : ObjectId("5b611c88c22929000a69fea2"), "recvTime" : ISODate("2018-08-01T02:35:52.628Z"), "attrName" : "y", "attrType" : "float", "attrValue" : "0.2" }
```
```bash
mac:$ kubectl exec mongodb-0 -c mongodb -- mongo sth_robot --eval 'db.getCollection("sth_/_guide_robot_0000000000000002_guide_robot").find()'
MongoDB shell version v3.6.5
connecting to: mongodb://127.0.0.1:27017/sth_robot
MongoDB server version: 3.6.5
{ "_id" : ObjectId("5b611c8cc22929000a69fea3"), "recvTime" : ISODate("2018-08-01T02:35:56.153Z"), "attrName" : "r_mode", "attrType" : "string", "attrValue" : "Navi" }
{ "_id" : ObjectId("5b611d37f8a94e000a6eaeae"), "recvTime" : ISODate("2018-08-01T02:38:47.590Z"), "attrName" : "robot_request_info", "attrType" : "commandResult", "attrValue" : "result,success/time,2018-08-01 11:38:46/r_cmd,Navi/pos.x,-0.1/pos.y,0.2" }
{ "_id" : ObjectId("5b611d37f8a94e000a6eaeaf"), "recvTime" : ISODate("2018-08-01T02:38:47.590Z"), "attrName" : "robot_request_status", "attrType" : "commandStatus", "attrValue" : "OK" }
{ "_id" : ObjectId("5b611c8cc22929000a69fea5"), "recvTime" : ISODate("2018-08-01T02:35:56.153Z"), "attrName" : "theta", "attrType" : "float", "attrValue" : "-0.3" }
{ "_id" : ObjectId("5b611c8cc22929000a69fea6"), "recvTime" : ISODate("2018-08-01T02:35:56.153Z"), "attrName" : "time", "attrType" : "string", "attrValue" : "2018-09-08 17:16:15" }
{ "_id" : ObjectId("5b611c8cc22929000a69fea7"), "recvTime" : ISODate("2018-08-01T02:35:56.153Z"), "attrName" : "x", "attrType" : "float", "attrValue" : "-0.1" }
{ "_id" : ObjectId("5b611c8cc22929000a69fea8"), "recvTime" : ISODate("2018-08-01T02:35:56.153Z"), "attrName" : "y", "attrType" : "float", "attrValue" : "-0.2" }
```

## register CAMERA to cygnus

```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: camera" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v2/subscriptions/ -X POST -d @- <<__EOS__
{
  "subject": {
    "entities": [{
      "idPattern": "external_camera.*",
      "type": "external_camera"
    }]
  },
  "notification": {
    "http": {
      "url": "http://cygnus:5050/notify"
    },
    "attrs": [
      "time",
      "c_mode",
      "num_p",
      "position",
      "external_camera_request_status",
      "external_camera_request_info"
    ],
    "attrsFormat": "legacy"
  }
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: camera" -H "Fiware-ServicePath: /" https://api.tech-sketch.jp/orion/v2/subscriptions/ | jq .
[
  {
    "id": "5b60fbaabc0be89f5baac3d2",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "external_camera.*",
          "type": "external_camera"
        }
      ],
      "condition": {
        "attrs": []
      }
    },
    "notification": {
      "timesSent": 1,
      "lastNotification": "2018-08-01T00:15:38.00Z",
      "attrs": [
        "time",
        "c_mode",
        "num_p",
        "position",
        "external_camera_request_status",
        "external_camera_request_info"
      ],
      "attrsFormat": "legacy",
      "http": {
        "url": "http://cygnus:5050/notify"
      },
      "lastSuccess": "2018-08-01T00:15:38.00Z"
    }
  }
]
```
```bash
mac:$ kubectl exec mongodb-0 -c mongodb -- mongo sth_camera --eval 'db.getCollection("sth_/_external_camera_0000000000000011_external_camera").find()'
MongoDB shell version v3.6.5
connecting to: mongodb://127.0.0.1:27017/sth_camera
MongoDB server version: 3.6.5
{ "_id" : ObjectId("5b60fbfbf8a94e000a6eae83"), "recvTime" : ISODate("2018-08-01T00:16:58.930Z"), "attrName" : "c_mode", "attrType" : "string", "attrValue" : "Monitor" }
{ "_id" : ObjectId("5b60fbfbf8a94e000a6eae84"), "recvTime" : ISODate("2018-07-31T23:34:35.231Z"), "attrName" : "external_camera_request_info", "attrType" : "commandResult", "attrValue" : "result,success/time,2018-08-01 08:34:32/c_cmd,Monitor" }
{ "_id" : ObjectId("5b60fbfbf8a94e000a6eae85"), "recvTime" : ISODate("2018-07-31T23:34:35.231Z"), "attrName" : "external_camera_request_status", "attrType" : "commandStatus", "attrValue" : "OK" }
{ "_id" : ObjectId("5b60fbfbf8a94e000a6eae86"), "recvTime" : ISODate("2018-08-01T00:16:58.930Z"), "attrName" : "num_p", "attrType" : "int", "attrValue" : "1" }
{ "_id" : ObjectId("5b60fbfbf8a94e000a6eae87"), "recvTime" : ISODate("2018-08-01T00:16:58.930Z"), "attrName" : "position", "attrType" : "string", "attrValue" : "x[0],1.12/y[0],-95.1" }
{ "_id" : ObjectId("5b60fbfbf8a94e000a6eae88"), "recvTime" : ISODate("2018-08-01T00:16:58.930Z"), "attrName" : "time", "attrType" : "string", "attrValue" : "2018-01-02 03:04:05" }
```
```bash
mac:$ kubectl exec mongodb-0 -c mongodb -- mongo sth_camera --eval 'db.getCollection("sth_/_external_camera_0000000000000012_external_camera").find()'
MongoDB shell version v3.6.5
connecting to: mongodb://127.0.0.1:27017/sth_camera
MongoDB server version: 3.6.5
{ "_id" : ObjectId("5b60fc92c22929000a69fe7e"), "recvTime" : ISODate("2018-08-01T00:19:30.639Z"), "attrName" : "c_mode", "attrType" : "string", "attrValue" : "Monitor" }
{ "_id" : ObjectId("5b60fc92c22929000a69fe7f"), "recvTime" : ISODate("2018-07-31T23:44:31.386Z"), "attrName" : "external_camera_request_info", "attrType" : "commandResult", "attrValue" : "result,success/time,2018-08-01 08:44:28/c_cmd,Monitor" }
{ "_id" : ObjectId("5b60fc92c22929000a69fe80"), "recvTime" : ISODate("2018-07-31T23:44:31.386Z"), "attrName" : "external_camera_request_status", "attrType" : "commandStatus", "attrValue" : "OK" }
{ "_id" : ObjectId("5b60fc92c22929000a69fe81"), "recvTime" : ISODate("2018-08-01T00:19:30.639Z"), "attrName" : "num_p", "attrType" : "int", "attrValue" : "1" }
{ "_id" : ObjectId("5b60fc92c22929000a69fe82"), "recvTime" : ISODate("2018-08-01T00:19:30.639Z"), "attrName" : "position", "attrType" : "string", "attrValue" : "x[0],-0.1/y[0],-15.1" }
{ "_id" : ObjectId("5b60fc92c22929000a69fe83"), "recvTime" : ISODate("2018-08-01T00:19:30.639Z"), "attrName" : "time", "attrType" : "string", "attrValue" : "2018-01-02 03:04:05" }
```
```bash
mac:$ kubectl exec mongodb-0 -c mongodb -- mongo sth_camera --eval 'db.getCollection("sth_/_external_camera_0000000000000021_external_camera").find()'
MongoDB shell version v3.6.5
connecting to: mongodb://127.0.0.1:27017/sth_camera
MongoDB server version: 3.6.5
{ "_id" : ObjectId("5b60fca2c22929000a69fe84"), "recvTime" : ISODate("2018-08-01T00:19:46.793Z"), "attrName" : "c_mode", "attrType" : "string", "attrValue" : "Monitor" }
{ "_id" : ObjectId("5b60fca2c22929000a69fe85"), "recvTime" : ISODate("2018-07-31T23:44:55.554Z"), "attrName" : "external_camera_request_info", "attrType" : "commandResult", "attrValue" : "result,success/time,2018-08-01 08:44:53/c_cmd,Monitor" }
{ "_id" : ObjectId("5b60fca2c22929000a69fe86"), "recvTime" : ISODate("2018-07-31T23:44:55.554Z"), "attrName" : "external_camera_request_status", "attrType" : "commandStatus", "attrValue" : "OK" }
{ "_id" : ObjectId("5b60fca2c22929000a69fe87"), "recvTime" : ISODate("2018-08-01T00:19:46.793Z"), "attrName" : "num_p", "attrType" : "int", "attrValue" : "1" }
{ "_id" : ObjectId("5b60fca2c22929000a69fe88"), "recvTime" : ISODate("2018-08-01T00:19:46.793Z"), "attrName" : "position", "attrType" : "string", "attrValue" : "x[0],-0.111111/y[0],105.1" }
{ "_id" : ObjectId("5b60fca2c22929000a69fe89"), "recvTime" : ISODate("2018-08-01T00:19:46.793Z"), "attrName" : "time", "attrType" : "string", "attrValue" : "2018-01-02 03:04:05" }
```

## register DEST-LED to cygnus
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: dest_led" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v2/subscriptions/ -X POST -d @- <<__EOS__
{
  "subject": {
    "entities": [{
      "idPattern": "dest_led.*",
      "type": "dest_led"
    }]
  },
  "notification": {
    "http": {
      "url": "http://cygnus:5050/notify"
    },
    "attrs": ["action_status", "action_info"],
    "attrsFormat": "legacy"
  }
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: dest_led" -H "Fiware-ServicePath: /" https://api.tech-sketch.jp/orion/v2/subscriptions/ | jq .
[
  {
    "id": "5b3c83f2d31a6404acc0ae2f",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "dest_led.*",
          "type": "dest_led"
        }
      ],
      "condition": {
        "attrs": []
      }
    },
    "notification": {
      "timesSent": 1,
      "lastNotification": "2018-07-04T08:23:14.00Z",
      "attrs": [
        "action_status",
        "action_info"
      ],
      "attrsFormat": "legacy",
      "http": {
        "url": "http://cygnus:5050/notify"
      },
      "lastSuccess": "2018-07-04T08:23:14.00Z"
    }
  }
]
```
```bash
mac:$ kubectl exec mongodb-0 -c mongodb -- mongo sth_dest_led --eval 'db.getCollection("sth_/_dest_led_0000000000000001_dest_led").find()'
MongoDB shell version v3.6.5
connecting to: mongodb://127.0.0.1:27017/sth_dest_led
MongoDB server version: 3.6.5
{ "_id" : ObjectId("5b3c847ac22929000a69f8b5"), "recvTime" : ISODate("2018-07-04T07:40:04.779Z"), "attrName" : "action_info", "attrType" : "commandResult", "attrValue" : "success" }
{ "_id" : ObjectId("5b3c847ac22929000a69f8b6"), "recvTime" : ISODate("2018-07-04T08:25:30.289Z"), "attrName" : "action_status", "attrType" : "commandStatus", "attrValue" : "PENDING" }
{ "_id" : ObjectId("5b3c8499f8a94e000a6ea93a"), "recvTime" : ISODate("2018-07-04T08:25:57.960Z"), "attrName" : "action_info", "attrType" : "commandResult", "attrValue" : "success" }
{ "_id" : ObjectId("5b3c8499f8a94e000a6ea93b"), "recvTime" : ISODate("2018-07-04T08:25:57.960Z"), "attrName" : "action_status", "attrType" : "commandStatus", "attrValue" : "OK" }
```

## register DEST-HUMAN-SENSOR to cygnus
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: dest_human_sensor" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v2/subscriptions/ -X POST -d @- <<__EOS__
{
  "subject": {
    "entities": [{
      "idPattern": "dest_human_sensor.*",
      "type": "dest_human_sensor"
    }]
  },
  "notification": {
    "http": {
      "url": "http://cygnus:5050/notify"
    },
    "attrs": ["arrival"],
    "attrsFormat": "legacy"
  }
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: dest_human_sensor" -H "Fiware-ServicePath: /" https://api.tech-sketch.jp/orion/v2/subscriptions/ | jq .
[
  {
    "id": "5b3d786bd31a6404acc0ae31",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "dest_human_sensor.*",
          "type": "dest_human_sensor"
        }
      ],
      "condition": {
        "attrs": []
      }
    },
    "notification": {
      "timesSent": 1,
      "lastNotification": "2018-07-05T01:46:19.00Z",
      "attrs": [
        "arrival"
      ],
      "attrsFormat": "legacy",
      "http": {
        "url": "http://cygnus:5050/notify"
      },
      "lastSuccess": "2018-07-05T01:46:19.00Z"
    }
  }
]
```
```bash
mac:$ kubectl exec mongodb-0 -c mongodb -- mongo sth_dest_human_sensor --eval 'db.getCollection("sth_/_dest_human_sensor_0000000000000001_dest_human_sensor").find()'
MongoDB shell version v3.6.5
connecting to: mongodb://127.0.0.1:27017/sth_dest_human_sensor
MongoDB server version: 3.6.5
{ "_id" : ObjectId("5b3d786b23b570000ae53c6e"), "recvTime" : ISODate("2018-07-05T01:46:19.603Z"), "attrName" : "arrival", "attrType" : "string", "attrValue" : "2018-07-05T10:41:52.1530754912+0900" }
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
      "id": "pepper_0000000000000001",
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
          "id": "pepper_0000000000000001",
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
      "id": "pepper_0000000000000001",
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
          "id": "pepper_0000000000000001",
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
          "id": "pepper_0000000000000001",
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

## register `detect-visitor` of ledger as a subscriber of PEPPER
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v2/subscriptions/ -X POST -d @- <<__EOS__
{
  "subject": {
    "entities": [{
      "id": "pepper_0000000000000002",
      "type": "pepper"
    }],
    "condition": {
      "attrs": ["face"]
    }
  },
  "notification": {
    "http": {
      "url": "http://ledger:8888/notify/detect-visitor/"
    },
    "attrs": ["face"]
  }
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-ServicePath: /" https://api.tech-sketch.jp/orion/v2/subscriptions/ | jq .
[
  {
    "id": "5b397c2c01ed8ed56809d2c8",
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
      "timesSent": 36,
      "lastNotification": "2018-07-03T05:34:29.00Z",
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
      "lastSuccess": "2018-07-03T05:34:29.00Z"
    }
  },
  {
    "id": "5b397c967da87a300178826f",
    "status": "active",
    "subject": {
      "entities": [
        {
          "id": "pepper_0000000000000001",
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
      "timesSent": 14,
      "lastNotification": "2018-07-03T05:34:29.00Z",
      "attrs": [
        "face",
        "dest"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://reception:8888/notify/finish-reception/"
      },
      "lastSuccess": "2018-07-03T05:34:29.00Z"
    }
  },
  {
    "id": "5b397cac7da87a3001788270",
    "status": "active",
    "subject": {
      "entities": [
        {
          "id": "pepper_0000000000000001",
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
      "timesSent": 14,
      "lastNotification": "2018-07-03T05:34:29.00Z",
      "attrs": [
        "face",
        "dest"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://ledger:8888/notify/record-reception/"
      },
      "lastSuccess": "2018-07-03T05:34:29.00Z"
    }
  },
  {
    "id": "5b3ecfacd31a6404acc0ae36",
    "status": "active",
    "subject": {
      "entities": [
        {
          "id": "pepper_0000000000000002",
          "type": "pepper"
        }
      ],
      "condition": {
        "attrs": [
          "face"
        ]
      }
    },
    "notification": {
      "timesSent": 1,
      "lastNotification": "2018-07-06T02:10:52.00Z",
      "attrs": [
        "face"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://ledger:8888/notify/detect-visitor/"
      },
      "lastSuccess": "2018-07-06T02:10:52.00Z"
    }
  }
]
```

## register `reask-destination` of ledger as a subscriber of PEPPER
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v2/subscriptions/ -X POST -d @- <<__EOS__
{
  "subject": {
    "entities": [{
      "id": "pepper_0000000000000002",
      "type": "pepper"
    }],
    "condition": {
      "attrs": ["dest"]
    }
  },
  "notification": {
    "http": {
      "url": "http://ledger:8888/notify/reask-destination/"
    },
    "attrs": ["dest"]
  }
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-ServicePath: /" https://api.tech-sketch.jp/orion/v2/subscriptions/ | jq .
[
  {
    "id": "5b397c2c01ed8ed56809d2c8",
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
      "timesSent": 36,
      "lastNotification": "2018-07-03T05:34:29.00Z",
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
      "lastSuccess": "2018-07-03T05:34:29.00Z"
    }
  },
  {
    "id": "5b397c967da87a300178826f",
    "status": "active",
    "subject": {
      "entities": [
        {
          "id": "pepper_0000000000000001",
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
      "timesSent": 14,
      "lastNotification": "2018-07-03T05:34:29.00Z",
      "attrs": [
        "face",
        "dest"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://reception:8888/notify/finish-reception/"
      },
      "lastSuccess": "2018-07-03T05:34:29.00Z"
    }
  },
  {
    "id": "5b397cac7da87a3001788270",
    "status": "active",
    "subject": {
      "entities": [
        {
          "id": "pepper_0000000000000001",
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
      "timesSent": 14,
      "lastNotification": "2018-07-03T05:34:29.00Z",
      "attrs": [
        "face",
        "dest"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://ledger:8888/notify/record-reception/"
      },
      "lastSuccess": "2018-07-03T05:34:29.00Z"
    }
  },
  {
    "id": "5b3ecfacd31a6404acc0ae36",
    "status": "active",
    "subject": {
      "entities": [
        {
          "id": "pepper_0000000000000002",
          "type": "pepper"
        }
      ],
      "condition": {
        "attrs": [
          "face"
        ]
      }
    },
    "notification": {
      "timesSent": 1,
      "lastNotification": "2018-07-06T02:10:52.00Z",
      "attrs": [
        "face"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://ledger:8888/notify/detect-visitor/"
      },
      "lastSuccess": "2018-07-06T02:10:52.00Z"
    }
  },
  {
    "id": "5b3ed0b0f1bdbe368d81d4ce",
    "status": "active",
    "subject": {
      "entities": [
        {
          "id": "pepper_0000000000000002",
          "type": "pepper"
        }
      ],
      "condition": {
        "attrs": [
          "dest"
        ]
      }
    },
    "notification": {
      "timesSent": 1,
      "lastNotification": "2018-07-06T02:15:12.00Z",
      "attrs": [
        "dest"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://ledger:8888/notify/reask-destination/"
      }
    }
  }
]
```

## register `start_movement` entity
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: start_movement" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v2/entities/ -X POST -d @- <<__EOS__
{
  "id": "start_movement",
  "type": "start_movement",
  "destx": {
    "type": "float",
    "value": "",
    "metadata": {}
  },
  "desty": {
    "type": "float",
    "value": "",
    "metadata": {}
  },
  "floor": {
    "type": "int",
    "value": "",
    "metadata": {}
  },
  "timestamp": {
    "type": "string",
    "value": "",
    "metadata": {}
  }
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: start_movement" -H "Fiware-ServicePath: /" https://api.tech-sketch.jp/orion/v2/entities/start_movement/ | jq .
{
  "id": "start_movement",
  "type": "start_movement",
  "destx": {
    "type": "float",
    "value": "",
    "metadata": {}
  },
  "desty": {
    "type": "float",
    "value": "",
    "metadata": {}
  },
  "floor": {
    "type": "int",
    "value": "",
    "metadata": {}
  },
  "timestamp": {
    "type": "string",
    "value": "",
    "metadata": {}
  }
}
```

## register `start-movement` of guidance as a subscriber of `start_movement`
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: start_movement" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v2/subscriptions/ -X POST -d @- <<__EOS__
{
  "subject": {
    "entities": [{
      "id": "start_movement",
      "type": "start_movement"
    }],
    "condition": {
      "attrs": ["destx", "desty", "floor", "timestamp"]
    }
  },
  "notification": {
    "http": {
      "url": "http://guidance:8888/notify/start-movement/"
    },
    "attrs": ["destx", "desty", "floor", "timestamp"]
  }
}
__EOS__
```

## register cygnus as as subscriber of `start_movement`
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: start_movement" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v2/subscriptions/ -X POST -d @- <<__EOS__
{
  "subject": {
    "entities": [{
      "id": "start_movement",
      "type": "start_movement"
    }]
  },
  "notification": {
    "http": {
      "url": "http://cygnus:5050/notify"
    },
    "attrs": ["destx", "desty", "floor", "timestamp"],
    "attrsFormat": "legacy"
  }
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: start_movement" -H "Fiware-ServicePath: /" https://api.tech-sketch.jp/orion/v2/subscriptions/ | jq .
[
  {
    "id": "5b3efc85d31a6404acc0ae37",
    "status": "active",
    "subject": {
      "entities": [
        {
          "id": "start_movement",
          "type": "start_movement"
        }
      ],
      "condition": {
        "attrs": [
          "destx",
          "desty",
          "floor",
          "timestamp"
        ]
      }
    },
    "notification": {
      "attrs": [
        "destx",
        "desty",
        "floor",
        "timestamp"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://guidance:8888/notify/start-movement/"
      }
    }
  },
  {
    "id": "5b3efc8ed31a6404acc0ae38",
    "status": "active",
    "subject": {
      "entities": [
        {
          "id": "start_movement",
          "type": "start_movement"
        }
      ],
      "condition": {
        "attrs": []
      }
    },
    "notification": {
      "timesSent": 1,
      "lastNotification": "2018-07-06T05:22:22.00Z",
      "attrs": [
        "destx",
        "desty",
        "floor",
        "timestamp"
      ],
      "attrsFormat": "legacy",
      "http": {
        "url": "http://cygnus:5050/notify"
      },
      "lastSuccess": "2018-07-06T05:22:22.00Z"
    }
  }
]
```

## register `check-destination` of guidance as a subscriber of ROBOT
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v2/subscriptions/ -X POST -d @- <<__EOS__
{
  "subject": {
    "entities": [{
      "idPattern": "guide_robot.*",
      "type": "guide_robot"
    }],
    "condition": {
      "attrs": ["r_mode", "x", "y", "theta"],
      "expression": {
        "q": "r_mode==Navi"
      }
    }
  },
  "notification": {
    "http": {
      "url": "http://guidance:8888/notify/check-destination/"
    },
    "attrs": ["r_mode", "x", "y", "theta"]
  }
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-ServicePath: /" https://api.tech-sketch.jp/orion/v2/subscriptions/ | jq .
[
  {
    "id": "5b611c4cbc0be89f5baac3d3",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "guide_robot.*",
          "type": "guide_robot"
        }
      ],
      "condition": {
        "attrs": []
      }
    },
    "notification": {
      "timesSent": 5,
      "lastNotification": "2018-08-01T02:38:47.00Z",
      "attrs": [
        "time",
        "r_mode",
        "x",
        "y",
        "theta",
        "robot_request_status",
        "robot_request_info"
      ],
      "attrsFormat": "legacy",
      "http": {
        "url": "http://cygnus:5050/notify"
      },
      "lastSuccess": "2018-08-01T02:38:47.00Z"
    }
  },
  {
    "id": "5b611e8bd201a33a709aa74c",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "guide_robot.*",
          "type": "guide_robot"
        }
      ],
      "condition": {
        "attrs": [
          "r_mode",
          "x",
          "y",
          "theta"
        ],
        "expression": {
          "q": "r_mode==Navi"
        }
      }
    },
    "notification": {
      "timesSent": 1,
      "lastNotification": "2018-08-01T02:44:27.00Z",
      "attrs": [
        "r_mode",
        "x",
        "y",
        "theta"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://guidance:8888/notify/check-destination/"
      }
    }
  }
]
```

## register `stop-movement` of guidance as a subscriber of ROBOT
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v2/subscriptions/ -X POST -d @- <<__EOS__
{
  "subject": {
    "entities": [{
      "idPattern": "guide_robot.*",
      "type": "guide_robot"
    }],
    "condition": {
      "attrs": ["r_mode", "x", "y", "theta"],
      "expression": {
        "q": "r_mode==Standby"
      }
    }
  },
  "notification": {
    "http": {
      "url": "http://guidance:8888/notify/stop-movement/"
    },
    "attrs": ["r_mode", "x", "y", "theta"]
  }
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-ServicePath: /" https://api.tech-sketch.jp/orion/v2/subscriptions/ | jq .
[
  {
    "id": "5b611c4cbc0be89f5baac3d3",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "guide_robot.*",
          "type": "guide_robot"
        }
      ],
      "condition": {
        "attrs": []
      }
    },
    "notification": {
      "timesSent": 5,
      "lastNotification": "2018-08-01T02:38:47.00Z",
      "attrs": [
        "time",
        "r_mode",
        "x",
        "y",
        "theta",
        "robot_request_status",
        "robot_request_info"
      ],
      "attrsFormat": "legacy",
      "http": {
        "url": "http://cygnus:5050/notify"
      },
      "lastSuccess": "2018-08-01T02:38:47.00Z"
    }
  },
  {
    "id": "5b611e8bd201a33a709aa74c",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "guide_robot.*",
          "type": "guide_robot"
        }
      ],
      "condition": {
        "attrs": [
          "r_mode",
          "x",
          "y",
          "theta"
        ],
        "expression": {
          "q": "r_mode==Navi"
        }
      }
    },
    "notification": {
      "timesSent": 1,
      "lastNotification": "2018-08-01T02:44:27.00Z",
      "attrs": [
        "r_mode",
        "x",
        "y",
        "theta"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://guidance:8888/notify/check-destination/"
      },
      "lastSuccess": "2018-08-01T02:44:27.00Z"
    }
  },
  {
    "id": "5b611ecdd201a33a709aa74d",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "guide_robot.*",
          "type": "guide_robot"
        }
      ],
      "condition": {
        "attrs": [
          "r_mode",
          "x",
          "y",
          "theta"
        ],
        "expression": {
          "q": "r_mode==Standby"
        }
      }
    },
    "notification": {
      "attrs": [
        "r_mode",
        "x",
        "y",
        "theta"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://guidance:8888/notify/stop-movement/"
      }
    }
  }
]
```

## register `record-arrival` of ledger as a subscriber of DEST-HUMAN-SENSOR
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: dest_human_sensor" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v2/subscriptions/ -X POST -d @- <<__EOS__
{
  "subject": {
    "entities": [{
      "idPattern": "dest_human_sensor.*",
      "type": "dest_human_sensor"
    }],
    "condition": {
      "attrs": ["arrival"]
    }
  },
  "notification": {
    "http": {
      "url": "http://ledger:8888/notify/record-arrival/"
    },
    "attrs": ["arrival"]
  }
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: dest_human_sensor" -H "Fiware-ServicePath: /" https://api.tech-sketch.jp/orion/v2/subscriptions/ | jq .
[
  {
    "id": "5b3d786bd31a6404acc0ae31",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "dest_human_sensor.*",
          "type": "dest_human_sensor"
        }
      ],
      "condition": {
        "attrs": []
      }
    },
    "notification": {
      "timesSent": 3,
      "lastNotification": "2018-07-05T02:53:34.00Z",
      "attrs": [
        "arrival"
      ],
      "attrsFormat": "legacy",
      "http": {
        "url": "http://cygnus:5050/notify"
      },
      "lastSuccess": "2018-07-05T02:53:34.00Z"
    }
  },
  {
    "id": "5b3d8959d31a6404acc0ae32",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "dest_human_sensor.*",
          "type": "dest_human_sensor"
        }
      ],
      "condition": {
        "attrs": [
          "arrival"
        ]
      }
    },
    "notification": {
      "timesSent": 1,
      "lastNotification": "2018-07-05T02:58:33.00Z",
      "attrs": [
        "arrival"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://ledger:8888/notify/record-arrival/"
      },
      "lastSuccess": "2018-07-05T02:58:33.00Z"
    }
  }
]
```

## register `arrival` of guidance as a subscriber of DEST-HUMAN-SENSOR
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: dest_human_sensor" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v2/subscriptions/ -X POST -d @- <<__EOS__
{
  "subject": {
    "entities": [{
      "idPattern": "dest_human_sensor.*",
      "type": "dest_human_sensor"
    }],
    "condition": {
      "attrs": ["arrival"]
    }
  },
  "notification": {
    "http": {
      "url": "http://guidance:8888/notify/arrival/"
    },
    "attrs": ["arrival"]
  }
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: dest_human_sensor" -H "Fiware-ServicePath: /" https://api.tech-sketch.jp/orion/v2/subscriptions/ | jq .
[
  {
    "id": "5b3d786bd31a6404acc0ae31",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "dest_human_sensor.*",
          "type": "dest_human_sensor"
        }
      ],
      "condition": {
        "attrs": []
      }
    },
    "notification": {
      "timesSent": 5,
      "lastNotification": "2018-07-05T03:34:44.00Z",
      "attrs": [
        "arrival"
      ],
      "attrsFormat": "legacy",
      "http": {
        "url": "http://cygnus:5050/notify"
      },
      "lastSuccess": "2018-07-05T03:34:44.00Z"
    }
  },
  {
    "id": "5b3d8959d31a6404acc0ae32",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "dest_human_sensor.*",
          "type": "dest_human_sensor"
        }
      ],
      "condition": {
        "attrs": [
          "arrival"
        ]
      }
    },
    "notification": {
      "timesSent": 3,
      "lastNotification": "2018-07-05T03:34:44.00Z",
      "attrs": [
        "arrival"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://ledger:8888/notify/record-arrival/"
      },
      "lastSuccess": "2018-07-05T03:34:44.00Z"
    }
  },
  {
    "id": "5b3d921ad31a6404acc0ae33",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "dest_human_sensor.*",
          "type": "dest_human_sensor"
        }
      ],
      "condition": {
        "attrs": [
          "arrival"
        ]
      }
    },
    "notification": {
      "timesSent": 1,
      "lastNotification": "2018-07-05T03:35:54.00Z",
      "attrs": [
        "arrival"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://guidance:8888/notify/arrival/"
      },
      "lastSuccess": "2018-07-05T03:35:54.00Z"
    }
  }
]
```

## register destinations
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl https://api.tech-sketch.jp/destinations/ -H "Authorization: bearer ${TOKEN}" -H "Content-Type: application/json" -X POST -d @- <<__EOS__ | jq .
{
    "name":"initial-1",
    "floor": 1,
    "dest_pos_x": 0.0,
    "dest_pos_y": 0.0,
    "dest_led_id": null,
    "dest_led_pos_x": null,
    "dest_led_pos_y": null,
    "dest_human_sensor_id": null,
    "initial": true
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl https://api.tech-sketch.jp/destinations/ -H "Authorization: bearer ${TOKEN}" -H "Content-Type: application/json" -X POST -d @- <<__EOS__ | jq .
{
    "name":"initial-2",
    "floor": 2,
    "dest_pos_x": 0.0,
    "dest_pos_y": 0.0,
    "dest_led_id": null,
    "dest_led_pos_x": null,
    "dest_led_pos_y": null,
    "dest_human_sensor_id": null,
    "initial": true
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl https://api.tech-sketch.jp/destinations/ -H "Authorization: bearer ${TOKEN}" -H "Content-Type: application/json" -X POST -d @- <<__EOS__ | jq .
{
    "name":"管理センター",
    "floor": 1,
    "dest_pos_x": -10.0,
    "dest_pos_y": 10.0,
    "dest_led_id": "dest_led_0000000000000001",
    "dest_led_pos_x": -9.0,
    "dest_led_pos_y": 9.0,
    "dest_human_sensor_id": "dest_human_sensor_0000000000000001"
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl https://api.tech-sketch.jp/destinations/ -H "Authorization: bearer ${TOKEN}" -H "Content-Type: application/json" -X POST -d @- <<__EOS__ | jq .
{
    "name":"203号室",
    "floor": 2,
    "dest_pos_x": 20.0,
    "dest_pos_y": 20.0,
    "dest_led_id": "dest_led_0000000000000002",
    "dest_led_pos_x": 19.0,
    "dest_led_pos_y": 19.0,
    "dest_human_sensor_id": "dest_human_sensor_0000000000000002"
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl https://api.tech-sketch.jp/destinations/ -H "Authorization: bearer ${TOKEN}" -H "Content-Type: application/json" -X POST -d @- <<__EOS__ | jq .
{
    "name":"204号室",
    "floor": 2,
    "dest_pos_x": 20.0,
    "dest_pos_y": -10.0,
    "dest_led_id": "dest_led_0000000000000003",
    "dest_led_pos_x": 19.0,
    "dest_led_pos_y": -19.0,
    "dest_human_sensor_id": "dest_human_sensor_0000000000000003"
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl https://api.tech-sketch.jp/destinations/ -H "Authorization: bearer ${TOKEN}" -H "Content-Type: application/json" -X POST -d @- <<__EOS__ | jq .
{
    "name":"ProjectRoom 1",
    "floor": 3,
    "dest_pos_x": null,
    "dest_pos_y": null,
    "dest_led_id": null,
    "dest_led_pos_x": null,
    "dest_led_pos_y": null,
    "dest_human_sensor_id": null,
    "slack_webhook": "https://hooks.slack.com/services/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
}
__EOS__
```
