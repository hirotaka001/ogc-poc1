# 4. simulate scenario

## preparation
* start roscore & rosbridge on robot and camera
* start `rostopic echo /Robot/request`

## reception
1. subscribe all topics

    ```bash
    mac:$ mosquitto_sub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /# -u iotagent -P XXXXXXXX
    ```
1. simulate to push button of `button_sensor`

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /button_sensor/button_sensor_0000000000000001/attrs -u iotagent -P XXXXXXXX -m "$d|state|on"
    Client mosqpub|52223-Nobuyukin sending CONNECT
    Client mosqpub|52223-Nobuyukin received CONNACK
    Client mosqpub|52223-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/button_sensor/button_sensor_0000000000000001/attrs', ... (44 bytes))
    Client mosqpub|52223-Nobuyukin sending DISCONNECT
    ```
    * send 'welcome' command to `pepper` automatically when receiving the `state|on` command from `button_sensor`

        ```bash
        mac:$ mosquitto_sub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /# -u iotagent -P XXXXXXXX
        ...
        Client mosqsub|52097-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/button_sensor/button_sensor_0000000000000001/attrs', ... (44 bytes))
        2018-06-26T13:43:18.1529988198+0900|state|on
        Client mosqsub|52097-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/cmd', ... (37 bytes))
        pepper_0000000000000001@welcome|start
        ```
1. simlate to be called `/destinations/` REST API by `pepper`

    ```bash
    mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" https://api.tech-sketch.jp/destinations/ | jq .
    [
      {
        "dest_human_sensor_id": "DEST-HUMAN-SENSOR-n8aL7MJuNQk0iJpY",
        "dest_led_id": "DEST-LED-CK2s264PqyndhUZ7",
        "dest_led_pos": "0.000000,0.000000",
        "dest_pos": "0.001151,0.000134",
        "floor": 1,
        "id": "dest-n4uRxmtdWv6jOHpI",
        "name": "管理センター"
      },
      {
        "dest_human_sensor_id": "DEST-HUMAN-SENSOR-oyVYENgHKHmQ6VJE",
        "dest_led_id": "DEST-LED-12Mz9QcPjoemgU39",
        "dest_led_pos": "122.001122,91.991122",
        "dest_pos": "125.12345,92.12345",
        "floor": 2,
        "id": "dest-vLBTZbPXc3Al0hMT",
        "name": "203号室"
      },
      {
        "dest_human_sensor_id": "DEST-HUMAN-SENSOR-9WfJoTmxczWrM4WZ",
        "dest_led_id": "DEST-LED-MV4isvEfDsLZ75R6",
        "dest_led_pos": "98.980808,0.881122",
        "dest_pos": "110.120101,0.993313",
        "floor": 2,
        "id": "dest-9QgohxohSmb3AECD",
        "name": "204号室"
      },
      {
        "dest_human_sensor_id": "DEST-HUMAN-SENSOR-6d8JoY1hR0wS8rqO",
        "dest_led_id": "DEST-LED-sDAyKhjhXKqJsbr9",
        "dest_led_pos": "122.001122,91.991122",
        "dest_pos": "125.12345,92.12345",
        "floor": 3,
        "id": "dest-Ymq1aoftEIViZjry",
        "name": "ProjectRoom 1",
        "slack_webhook": "https://hooks.slack.com/services/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
      }
    ]
    ```
1. simulate to be called `/storage/faces/` REST API by `pepper`

    ```bash
    mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Content-Type: multipart/form-data" https://api.tech-sketch.jp/storage/faces/ -X POST -F face=@face.jpg | jq .
    {
      "path": "/shared/faces/xBlzQGubIM5YYr1S.JPEG",
      "url": ""
    }
    ```
1. simulate to finish reception

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /pepper/pepper_0000000000000001/attrs -u iotagent -P XXXXXXXX -m "$d|face|/shared/faces/IoYu2c4sggdVLi49.JPEG|dest|ProjectRoom 1"
    Client mosqpub|22418-Nobuyukin sending CONNECT
    Client mosqpub|22418-Nobuyukin received CONNACK
    Client mosqpub|22418-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/attrs', ... (100 bytes))
    Client mosqpub|22418-Nobuyukin sending DISCONNECT
    ```
    * send 'handover' command to `pepper` automatically

        ```bash
        Client mosqsub|99494-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/attrs', ... (95 bytes))
        2018-06-28T10:44:07.1530150247+0900|face|/shared/faces/IoYu2c4sggdVLi49.JPEG|dest|ProjectRoom 1
        Client mosqsub|99494-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/cmd', ... (34 bytes))
        pepper_0000000000000001@handover|3
        ```
    * send ros message to ros topic '/Robot/request

        ```bash
        root@rosbridge:/opt/ros_ws# rostopic echo /Robot/request
        time: "2018-07-04 13:14:02"
        id: 1
        r_cmd: "Navi"
        pos:
          x: 125.12345
          y: 92.12345
          z: 3.0
        ---
        ```
1. simulate to send `welcome` cmd result

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /pepper/pepper_0000000000000001/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000001@welcome|success"
    Client mosqpub|22365-Nobuyukin sending CONNECT
    Client mosqpub|22365-Nobuyukin received CONNACK
    Client mosqpub|22365-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/cmdexe', ... (39 bytes))
    Client mosqpub|22365-Nobuyukin sending DISCONNECT
    ```
1. simulate to send `handover` cmd result

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /pepper/pepper_0000000000000001/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000001@handover|success"
    Client mosqpub|22763-Nobuyukin sending CONNECT
    Client mosqpub|22763-Nobuyukin received CONNACK
    Client mosqpub|22763-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/cmdexe', ... (40 bytes))
    Client mosqpub|22763-Nobuyukin sending DISCONNECT
    ```
1. simulate to receive robot state (Navi)
    * publish ros message to `/Robot/state`

    ```bash
    root@rosbridge:/opt/ros_ws# rostopic pub -1 /Robot/state rosbridge/r_state "
    time: '2018-01-02 03:04:05'
    id: 1
    r_mode: 'Navi'
    pos:
      x: 1.01
      y: -2.02
      z: 3.0
    "
    ```
    * receive MQTT message and send `action|on` message to `dest_led` authomatically

        ```bash
        Client mosqsub|77879-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot/attrs', ... (112 bytes))
        2018-07-04T13:24:20.259204+0900|time|2018-01-02 03:04:05|robot_id|1|r_mode|Navi|pos.x|1.01|pos.y|-2.02|pos.z|3.0
        Client mosqsub|58138-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/dest_led/dest_led_0000000000000001/cmd', ... (35 bytes))
        dest_led_0000000000000001@action|on
        ```
1. simulate to send `action` cmd result

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /dest_led/dest_led_0000000000000001/cmdexe -u iotagent -P XXXXXXXX -m "dest_led_0000000000000001@action|success"
    Client mosqpub|22763-Nobuyukin sending CONNECT
    Client mosqpub|22763-Nobuyukin received CONNACK
    Client mosqpub|22763-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/dest_led/dest_led_0000000000000001/cmdexe', ... (40 bytes))
    Client mosqpub|22763-Nobuyukin sending DISCONNECT
    ```
1. simulate to receive robot state (Standby)
    * publish ros message to `/Robot/state`

    ```bash
    root@rosbridge:/opt/ros_ws# rostopic pub -1 /Robot/state rosbridge/r_state "
    time: '2018-01-02 03:04:05'
    id: 1
    r_mode: 'Standby'
    pos:
      x: 1.01
      y: -2.02
      z: 3.0
    "
    ```
    * receive MQTT message, but don't send `action|on` message to `dest_led` authomatically

        ```bash
        Client mosqsub|49077-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot/attrs', ... (115 bytes))
        2018-07-05T08:41:12.547917+0900|time|2018-01-02 03:04:05|robot_id|1|r_mode|Standby|pos.x|1.01|pos.y|-2.02|pos.z|3.0
        ```
1. simuate visitor arriving at the destination

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /dest_human_sensor/dest_human_sensor_0000000000000001/attrs -u iotagent -P XXXXXXXX -m "$d|arrival|$d"
    Client mosqpub|65572-Nobuyukin sending CONNECT
    Client mosqpub|65572-Nobuyukin received CONNACK
    Client mosqpub|65572-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/dest_human_sensor/dest_human_sensor_0000000000000001/attrs', ... (79 bytes))
    Client mosqpub|65572-Nobuyukin sending DISCONNECT
    ```


1. simulate to receive camera state
    * publish ros message to `/ExternalCamera/state`

    ```bash
    root@rosbridge:/opt/ros_ws# rostopic pub -1 /ExternalCamera/state rosbridge/c_state "
    time: '2018-02-03 04:05:06'
    id: 2
    c_mode: 'Monitor'
    num_p: 2
    p_state:
    - i: 0
      pos: {x: 10.1, y: 20.2, z: 30.3}
      size: {width: 1.0, height: 2.0}
      feature: [0, 255, 0, 128, 128, 128]
    - i: 1
      pos: {x: 110.1, y: 120.2, z: 130.3}
      size: {width: 101.0, height: 102.0}
      feature: [255, 254, 253, 0, 1, 2]
    "
    ```
    * recieve MQTT message

        ```bash
        Client mosqsub|77879-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/external_camera/external_camera/attrs', ... (300 bytes))
        2018-07-04T13:31:03.853772+0900|time|2018-02-03 04:05:06|camera_id|2|c_mode|Monitor|num_p|2|p_state|pos[0].x,10.1/pos[0].y,20.2/pos[0].z,30.3/width[0],1.0/height[0],2.0/feature_hex[0],00ff00808080/pos[1].x,110.1/pos[1].y,120.2/pos[1].z,130.3/width[1],101.0/height[1],102.0/feature_hex[1],fffefd000102
        ```
1. the state of entities
    * `button_sensor_0000000000000001`

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: button_sensor" -H "Fiware-ServicePath: /" https://api.tech-sketch.jp/orion/v2/entities/button_sensor_0000000000000001/ | jq .
        {
          "id": "button_sensor_0000000000000001",
          "type": "button_sensor",
          "TimeInstant": {
            "type": "ISO8601",
            "value": "2018-07-04T13:10:53.1530677453+0900",
            "metadata": {}
          },
          "state": {
            "type": "string",
            "value": "on",
            "metadata": {
              "TimeInstant": {
                "type": "ISO8601",
                "value": "2018-07-04T13:10:53.1530677453+0900"
              }
            }
          }
        }
        ```
    * `pepper_0000000000000001`

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-ServicePath: /" https://api.tech-sketch.jp/orion/v2/entities/pepper_0000000000000001/ | jq .
        {
          "id": "pepper_0000000000000001",
          "type": "pepper",
          "TimeInstant": {
            "type": "ISO8601",
            "value": "2018-07-04T04:18:51.00Z",
            "metadata": {}
          },
          "dest": {
            "type": "string",
            "value": "ProjectRoom 1",
            "metadata": {
              "TimeInstant": {
                "type": "ISO8601",
                "value": "2018-07-04T13:14:05.1530677645+0900"
              }
            }
          },
          "face": {
            "type": "string",
            "value": "/shared/faces/IoYu2c4sggdVLi49.JPEG",
            "metadata": {
              "TimeInstant": {
                "type": "ISO8601",
                "value": "2018-07-04T13:14:05.1530677645+0900"
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
            "value": "success",
            "metadata": {
              "TimeInstant": {
                "type": "ISO8601",
                "value": "2018-07-04T04:18:51.420Z"
              }
            }
          },
          "handover_status": {
            "type": "commandStatus",
            "value": "OK",
            "metadata": {
              "TimeInstant": {
                "type": "ISO8601",
                "value": "2018-07-04T04:18:51.420Z"
              }
            }
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
            "value": "success",
            "metadata": {
              "TimeInstant": {
                "type": "ISO8601",
                "value": "2018-07-04T04:17:39.788Z"
              }
            }
          },
          "welcome_status": {
            "type": "commandStatus",
            "value": "OK",
            "metadata": {
              "TimeInstant": {
                "type": "ISO8601",
                "value": "2018-07-04T04:17:39.788Z"
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
    * `guide_robot`

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-ServicePath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot/ | jq .
        {
          "id": "guide_robot",
          "type": "guide_robot",
          "TimeInstant": {
            "type": "ISO8601",
            "value": "2018-07-04T13:24:20.259204+0900",
            "metadata": {}
          },
          "pos.x": {
            "type": "float",
            "value": "1.01",
            "metadata": {
              "TimeInstant": {
                "type": "ISO8601",
                "value": "2018-07-04T13:24:20.259204+0900"
              }
            }
          },
          "pos.y": {
            "type": "float",
            "value": "-2.02",
            "metadata": {
              "TimeInstant": {
                "type": "ISO8601",
                "value": "2018-07-04T13:24:20.259204+0900"
              }
            }
          },
          "pos.z": {
            "type": "float",
            "value": "3.0",
            "metadata": {
              "TimeInstant": {
                "type": "ISO8601",
                "value": "2018-07-04T13:24:20.259204+0900"
              }
            }
          },
          "r_mode": {
            "type": "string",
            "value": "Navi",
            "metadata": {
              "TimeInstant": {
                "type": "ISO8601",
                "value": "2018-07-04T13:24:20.259204+0900"
              }
            }
          },
          "robot_id": {
            "type": "int",
            "value": "1",
            "metadata": {
              "TimeInstant": {
                "type": "ISO8601",
                "value": "2018-07-04T13:24:20.259204+0900"
              }
            }
          },
          "robot_request_info": {
            "type": "commandResult",
            "value": "result,success/time,2018-07-04 13:14:02/id,1/r_cmd,Navi/pos.x,125.12345/pos.y,92.12345/pos.z,3.0",
            "metadata": {
              "TimeInstant": {
                "type": "ISO8601",
                "value": "2018-07-04T04:14:06.316Z"
              }
            }
          },
          "robot_request_status": {
            "type": "commandStatus",
            "value": "OK",
            "metadata": {
              "TimeInstant": {
                "type": "ISO8601",
                "value": "2018-07-04T04:14:06.316Z"
              }
            }
          },
          "time": {
            "type": "string",
            "value": "2018-01-02 03:04:05",
            "metadata": {
              "TimeInstant": {
                "type": "ISO8601",
                "value": "2018-07-04T13:24:20.259204+0900"
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
    * `external_camera`

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: camera" -H "Fiware-ServicePath: /" https://api.tech-sketch.jp/orion/v2/entities/external_camera/ | jq .
        {
          "id": "external_camera",
          "type": "external_camera",
          "TimeInstant": {
            "type": "ISO8601",
            "value": "2018-07-04T13:31:03.853772+0900",
            "metadata": {}
          },
          "c_mode": {
            "type": "string",
            "value": "Monitor",
            "metadata": {
              "TimeInstant": {
                "type": "ISO8601",
                "value": "2018-07-04T13:31:03.853772+0900"
              }
            }
          },
          "camera_id": {
            "type": "int",
            "value": "2",
            "metadata": {
              "TimeInstant": {
                "type": "ISO8601",
                "value": "2018-07-04T13:31:03.853772+0900"
              }
            }
          },
          "external_camera_request_info": {
            "type": "commandResult",
            "value": "result,success/camera_id,1/c_cmd,Monitor",
            "metadata": {
              "TimeInstant": {
                "type": "ISO8601",
                "value": "2018-07-04T03:39:38.731Z"
              }
            }
          },
          "external_camera_request_status": {
            "type": "commandStatus",
            "value": "OK",
            "metadata": {
              "TimeInstant": {
                "type": "ISO8601",
                "value": "2018-07-04T03:39:38.731Z"
              }
            }
          },
          "num_p": {
            "type": "int",
            "value": "2",
            "metadata": {
              "TimeInstant": {
                "type": "ISO8601",
                "value": "2018-07-04T13:31:03.853772+0900"
              }
            }
          },
          "p_state": {
            "type": "string",
            "value": "pos[0].x,10.1/pos[0].y,20.2/pos[0].z,30.3/width[0],1.0/height[0],2.0/feature_hex[0],00ff00808080/pos[1].x,110.1/pos[1].y,120.2/pos[1].z,130.3/width[1],101.0/height[1],102.0/feature_hex[1],fffefd000102",
            "metadata": {
              "TimeInstant": {
                "type": "ISO8601",
                "value": "2018-07-04T13:31:03.853772+0900"
              }
            }
          },
          "time": {
            "type": "string",
            "value": "2018-02-03 04:05:06",
            "metadata": {
              "TimeInstant": {
                "type": "ISO8601",
                "value": "2018-07-04T13:31:03.853772+0900"
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
