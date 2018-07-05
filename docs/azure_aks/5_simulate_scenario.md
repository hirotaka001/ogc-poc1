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
1. simulate to finish reception (floor 1)

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /pepper/pepper_0000000000000001/attrs -u iotagent -P XXXXXXXX -m "$d|face|/shared/faces/IoYu2c4sggdVLi49.JPEG|dest|管理センター"
    Client mosqpub|37117-Nobuyukin sending CONNECT
    Client mosqpub|37117-Nobuyukin received CONNACK
    Client mosqpub|37117-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/attrs', ... (100 bytes))
    Client mosqpub|37117-Nobuyukin sending DISCONNECT
    ```
    * send `handover` command to `pepper(floor 1)` and `robot_request` command to `guide_robot` automatically

        ```bash
        Client mosqsub|22564-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/attrs', ... (100 bytes))
        2018-07-05T17:40:57.1530780057+0900|face|/shared/faces/IoYu2c4sggdVLi49.JPEG|dest|管理センター
        Client mosqsub|22564-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot/cmd', ... (85 bytes))
        guide_robot@robot_request|robot_id|1|r_cmd|Navi|pos.x|0.001151|pos.y|0.000134|pos.z|1
        Client mosqsub|22564-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot/cmdexe', ... (121 bytes))
        guide_robot@robot_request|result,success/time,2018-07-05 17:41:27/id,1/r_cmd,Navi/pos.x,0.001151/pos.y,0.000134/pos.z,1.0
        Client mosqsub|22564-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/cmd', ... (34 bytes))
        pepper_0000000000000001@handover|1
        ```
    * send ros message to ros topic '/Robot/request

        ```bash
        root@rosbridge:/opt/ros_ws# rostopic echo /Robot/request
        time: "2018-07-05 17:41:27"
        id: 1
        r_cmd: "Navi"
        pos:
          x: 0.001151
          y: 0.000134
          z: 1.0
        ---
        ```
1. simulate to send `welcome` cmd result from `pepper(floor 1)`

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /pepper/pepper_0000000000000001/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000001@welcome|success"
    Client mosqpub|22365-Nobuyukin sending CONNECT
    Client mosqpub|22365-Nobuyukin received CONNACK
    Client mosqpub|22365-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/cmdexe', ... (39 bytes))
    Client mosqpub|22365-Nobuyukin sending DISCONNECT
    ```
1. simulate to send `handover` cmd result from `pepper(floor 1)`

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
      z: 1.0
    "
    ```
    * receive MQTT message and send `action|on` message to `dest_led` authomatically

        ```bash
        Client mosqsub|77879-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot/attrs', ... (112 bytes))
        2018-07-04T13:24:20.259204+0900|time|2018-01-02 03:04:05|robot_id|1|r_mode|Navi|pos.x|1.01|pos.y|-2.02|pos.z|1.0
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
      x: 10.01
      y: -20.02
      z: 1.0
    "
    ```
    * receive MQTT message, but don't send `action|on` message to `dest_led` authomatically

        ```bash
        Client mosqsub|49077-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot/attrs', ... (115 bytes))
        2018-07-05T08:41:12.547917+0900|time|2018-01-02 03:04:05|robot_id|1|r_mode|Standby|pos.x|10.01|pos.y|-20.02|pos.z|1.0
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
1. simulate to finish reception (floor 2)

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /pepper/pepper_0000000000000001/attrs -u iotagent -P iotagent_0GC -m "$d|face|/shared/faces/IoYu2c4sggdVLi49.JPEG|dest|203号室"
    Client mosqpub|37447-Nobuyukin sending CONNECT
    Client mosqpub|37447-Nobuyukin received CONNACK
    Client mosqpub|37447-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/attrs', ... (91 bytes))
    Client mosqpub|37447-Nobuyukin sending DISCONNECT
    ```
    * send `handover` command to `pepper(floor 1)` and `facedetect` command to `pepper(floor 2)` automatically

        ```bash
        Client mosqsub|22564-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/attrs', ... (91 bytes))
        2018-07-05T17:46:14.1530780374+0900|face|/shared/faces/IoYu2c4sggdVLi49.JPEG|dest|203号室
        Client mosqsub|22564-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000002/cmd', ... (40 bytes))
        pepper_0000000000000002@facedetect|start
        Client mosqsub|22564-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/cmd', ... (34 bytes))
        pepper_0000000000000001@handover|2
        ```
1. simulate to send `welcome` cmd result from `pepper(floor 1)`

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /pepper/pepper_0000000000000001/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000001@welcome|success"
    Client mosqpub|22365-Nobuyukin sending CONNECT
    Client mosqpub|22365-Nobuyukin received CONNACK
    Client mosqpub|22365-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/cmdexe', ... (39 bytes))
    Client mosqpub|22365-Nobuyukin sending DISCONNECT
    ```
1. simulate to send `handover` cmd result from `pepper(floor 1)`

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /pepper/pepper_0000000000000001/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000001@handover|success"
    Client mosqpub|22763-Nobuyukin sending CONNECT
    Client mosqpub|22763-Nobuyukin received CONNACK
    Client mosqpub|22763-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/cmdexe', ... (40 bytes))
    Client mosqpub|22763-Nobuyukin sending DISCONNECT
    ```
1. simulate to finish reception (floor 3)

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /pepper/pepper_0000000000000001/attrs -u iotagent -P iotagent_0GC -m "$d|face|/shared/faces/IoYu2c4sggdVLi49.JPEG|dest|ProjectRoom 1"
    Client mosqpub|38060-Nobuyukin sending CONNECT
    Client mosqpub|38060-Nobuyukin received CONNACK
    Client mosqpub|38060-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/attrs', ... (95 bytes))
    Client mosqpub|38060-Nobuyukin sending DISCONNECT
    ```
    * send `handover` command to `pepper(floor 1)` automatically

        ```bash
        Client mosqsub|22564-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/attrs', ... (95 bytes))
        2018-07-05T17:53:39.1530780819+0900|face|/shared/faces/IoYu2c4sggdVLi49.JPEG|dest|ProjectRoom 1
        Client mosqsub|22564-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/cmd', ... (34 bytes))
        pepper_0000000000000001@handover|3
        ```
1. simulate to send `welcome` cmd result from `pepper(floor 1)`

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /pepper/pepper_0000000000000001/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000001@welcome|success"
    Client mosqpub|22365-Nobuyukin sending CONNECT
    Client mosqpub|22365-Nobuyukin received CONNACK
    Client mosqpub|22365-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/cmdexe', ... (39 bytes))
    Client mosqpub|22365-Nobuyukin sending DISCONNECT
    ```
1. simulate to send `handover` cmd result from `pepper(floor 1)`

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /pepper/pepper_0000000000000001/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000001@handover|success"
    Client mosqpub|22763-Nobuyukin sending CONNECT
    Client mosqpub|22763-Nobuyukin received CONNACK
    Client mosqpub|22763-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/cmdexe', ... (40 bytes))
    Client mosqpub|22763-Nobuyukin sending DISCONNECT
    ```
