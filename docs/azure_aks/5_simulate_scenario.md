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
        Client mosqsub|15957-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/button_sensor/button_sensor_0000000000000001/attrs', ... (44 bytes))
        2018-08-01T13:47:06.1533098826+0900|state|on
        Client mosqsub|15957-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/cmd', ... (37 bytes))
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
1. simulate to be called `/storage/faces/` REST API by `pepper(floor 1)`

    ```bash
    mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Content-Type: multipart/form-data" https://api.tech-sketch.jp/storage/faces/ -X POST -F face=@face.jpg | jq .
    {
      "path": "/shared/faces/xBlzQGubIM5YYr1S.JPEG",
      "url": ""
    }
    ```

## guidance (floor 1)
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
        Client mosqsub|15957-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/attrs', ... (100 bytes))
        2018-08-01T13:51:35.1533099095+0900|face|/shared/faces/IoYu2c4sggdVLi49.JPEG|dest|管理センター
        Client mosqsub|15957-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/cmd', ... (34 bytes))
        pepper_0000000000000001@handover|1
        Client mosqsub|15957-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000001/cmd', ... (83 bytes))
        guide_robot_0000000000000001@robot_request|r_cmd|Navi|pos.x|0.001151|pos.y|0.000134
        Client mosqsub|15957-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000001/cmdexe', ... (123 bytes))
        guide_robot_0000000000000001@robot_request|result,success/time,2018-08-01 13:51:35/r_cmd,Navi/pos.x,0.001151/pos.y,0.000134
        ```
    * send ros message to ros topic `/Robot1F-1/request` automatically

        ```bash
        root@rosbridge:/opt/ros_ws# rostopic type /Robot1F-1/request
        office_guide_robot/r_req
        ```
        ```bash
        root@rosbridge:/opt/ros_ws# rostopic echo /Robot1F-1/request
        time: "2018-08-01 13:51:35"
        r_cmd: "Navi"
        pos:
          x: 0.001151
          y: 0.000134
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

## navigating (floor 1)
1. simulate to receive robot state (Navi)
    * publish ros message to `/Robot1F-1/state`

    ```bash
    root@rosbridge:/opt/ros_ws# rostopic pub -1 /Robot1F-1/state office_guide_robot/r_state "
    time: '2018-09-08 07:06:05'
    r_mode: 'Navi'
    pos:
      x: 1.1
      y: 1.2
      theta: 0.3
    "
    ```
    * receive MQTT message and send `action|on` message to `dest_led_0000000000000001` authomatically

        ```bash
        Client mosqsub|15957-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000001/attrs', ... (90 bytes))
        2018-08-01T13:57:40.484738+0900|time|2018-09-08 07:06:05|r_mode|Navi|x|1.1|y|1.2|theta|0.3
        Client mosqsub|15957-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/dest_led/dest_led_0000000000000001/cmd', ... (35 bytes))
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
    * publish ros message to `/Robot1F-1/state`

    ```bash
    root@rosbridge:/opt/ros_ws# rostopic pub -1 /Robot1F-1/state office_guide_robot/r_state "
    time: '2018-09-08 07:06:15'
    r_mode: 'Standby'
    pos:
      x: 15.1
      y: -11.2
      theta: 9.3
    "
    ```
    * receive MQTT message, but don't send `action|on` message to `dest_led` authomatically

        ```bash
        Client mosqsub|15957-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000001/attrs', ... (96 bytes))
        2018-08-01T14:00:28.335883+0900|time|2018-09-08 07:06:15|r_mode|Standby|x|15.1|y|-11.2|theta|9.3
        ```
    * nothing to do when stopping robot

        ```bash
        guidance-857987f97b-f86zj guidance 2018/08/01 05:00:28 [   INFO] src.views - nothing to do when called stop-movement
        ```

## arrival (floor 1)
1. simuate visitor arriving at the destination

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /dest_human_sensor/dest_human_sensor_0000000000000001/attrs -u iotagent -P XXXXXXXX -m "$d|arrival|$d"
    Client mosqpub|65572-Nobuyukin sending CONNECT
    Client mosqpub|65572-Nobuyukin received CONNACK
    Client mosqpub|65572-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/dest_human_sensor/dest_human_sensor_0000000000000001/attrs', ... (79 bytes))
    Client mosqpub|65572-Nobuyukin sending DISCONNECT
    ```
    * receive MQTT message and send `action|off` message to `dest_led_0000000000000001` and `robot_request` command to `guide_robot_0000000000000001` automatically

        ```bash
        Client mosqsub|15957-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/dest_human_sensor/dest_human_sensor_0000000000000001/attrs', ... (79 bytes))
        2018-08-01T14:03:09.1533099789+0900|arrival|2018-08-01T14:03:09.1533099789+0900
        Client mosqsub|15957-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/dest_led/dest_led_0000000000000001/cmd', ... (36 bytes))
        dest_led_0000000000000001@action|off
        Client mosqsub|15957-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000001/cmd', ... (73 bytes))
        guide_robot_0000000000000001@robot_request|r_cmd|Navi|pos.x|0.0|pos.y|0.0
        Client mosqsub|15957-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000001/cmdexe', ... (113 bytes))
        guide_robot_0000000000000001@robot_request|result,success/time,2018-08-01 14:03:10/r_cmd,Navi/pos.x,0.0/pos.y,0.0
        ```
    * send ros message to ros topic `/Robot1F-1/request` automatically

        ```bash
        root@rosbridge:/opt/ros_ws# rostopic echo /Robot1F-1/request
        time: "2018-08-01 14:03:10"
        r_cmd: "Navi"
        pos:
          x: 0.0
          y: 0.0
        ---
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
    * publish ros message to `/Robot1F-1/state`

    ```bash
    root@rosbridge:/opt/ros_ws# rostopic pub -1 /Robot1F-1/state office_guide_robot/r_state "
    time: '2018-09-08 07:06:15'
    r_mode: 'Standby'
    pos:
      x: 0.0
      y: 0.0
      theta: 0.0
    "
    ```
    * receive MQTT message, but don't send `action|on` message to `dest_led` authomatically

        ```bash
        Client mosqsub|15957-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000001/attrs', ... (93 bytes))
        2018-08-01T14:32:04.185008+0900|time|2018-09-08 07:06:25|r_mode|Standby|x|0.0|y|0.0|theta|0.0
        ```
    * nothing to do when stopping robot

        ```bash
        guidance-857987f97b-f86zj guidance 2018/08/01 05:32:04 [   INFO] src.views - nothing to do when called stop-movement
        ```

## guidance (floor 2)
1. simulate to finish reception (floor 2)

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /pepper/pepper_0000000000000001/attrs -u iotagent -P XXXXXXXX -m "$d|face|/shared/faces/IoYu2c4sggdVLi49.JPEG|dest|203号室"
    Client mosqpub|37447-Nobuyukin sending CONNECT
    Client mosqpub|37447-Nobuyukin received CONNACK
    Client mosqpub|37447-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/attrs', ... (91 bytes))
    Client mosqpub|37447-Nobuyukin sending DISCONNECT
    ```
    * send `handover` command to `pepper(floor 1)` and `facedetect` command to `pepper(floor 2)` automatically

        ```bash
        Client mosqsub|15957-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/attrs', ... (91 bytes))
        2018-08-01T14:34:12.1533101652+0900|face|/shared/faces/IoYu2c4sggdVLi49.JPEG|dest|203号室
        Client mosqsub|15957-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000002/cmd', ... (40 bytes))
        pepper_0000000000000002@facedetect|start
        Client mosqsub|15957-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/cmd', ... (34 bytes))
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


## face detection (floor 2)
1. simulate to be called `/storage/faces/` REST API by `pepper(floor 2)`

    ```bash
    mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Content-Type: multipart/form-data" https://api.tech-sketch.jp/storage/faces/ -X POST -F face=@face.jpg | jq .
    {
      "path": "/shared/faces/6Q72bJkxZ4Ct8wx0.JPEG",
      "url": ""
    }
    ```
1. simulate to detect visitor

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /pepper/pepper_0000000000000002/attrs -u iotagent -P XXXXXXXX -m "$d|face|/shared/faces/IoYu2c4sggdVLi49.JPEG"
    Client mosqpub|97057-Nobuyukin sending CONNECT
    Client mosqpub|97057-Nobuyukin received CONNACK
    Client mosqpub|97057-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000002/attrs', ... (76 bytes))
    Client mosqpub|97057-Nobuyukin sending DISCONNECT
    ```
    * send `handover` command to `pepper(floor 2)` and `robot_request` command to `guide_robot` automatically

        ```bash
        Client mosqsub|15957-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000002/attrs', ... (76 bytes))
        2018-08-01T14:38:09.1533101889+0900|face|/shared/faces/IoYu2c4sggdVLi49.JPEG
        Client mosqsub|15957-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000002/cmd', ... (41 bytes))
        pepper_0000000000000002@handover|continue
        Client mosqsub|15957-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000002/cmd', ... (84 bytes))
        guide_robot_0000000000000002@robot_request|r_cmd|Navi|pos.x|125.12345|pos.y|92.12345
        Client mosqsub|15957-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000002/cmdexe', ... (124 bytes))
        guide_robot_0000000000000002@robot_request|result,success/time,2018-08-01 14:38:10/r_cmd,Navi/pos.x,125.12345/pos.y,92.12345
        ```
    * send ros message to ros topic `/Robot2F-1/request` automatically

        ```bash
        root@rosbridge:/opt/ros_ws# rostopic type /Robot2F-1/request
        office_guide_robot/r_req
        ```
        ```bash
        root@rosbridge:/opt/ros_ws# rostopic echo /Robot2F-1/request
        time: "2018-08-01 14:38:10"
        r_cmd: "Navi"
        pos:
          x: 125.12345
          y: 92.12345
        ---
        ```
1. simulate to send `facedetect` cmd result from `pepper(floor 2)`

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /pepper/pepper_0000000000000002/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000002@facedetect|success"
    Client mosqpub|48535-Nobuyukin sending CONNECT
    Client mosqpub|48535-Nobuyukin received CONNACK
    Client mosqpub|48535-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000002/cmdexe', ... (42 bytes))
    Client mosqpub|48535-Nobuyukin sending DISCONNECT
    ```

1. simulate to send `handover` cmd result from `pepper(floor 2)`

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /pepper/pepper_0000000000000002/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000002@handover|success"
    Client mosqpub|48779-Nobuyukin sending CONNECT
    Client mosqpub|48779-Nobuyukin received CONNACK
    Client mosqpub|48779-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000002/cmdexe', ... (40 bytes))
    Client mosqpub|48779-Nobuyukin sending DISCONNECT
    ```

## navigating (floor 2)
1. simulate to receive robot state (Navi)
    * publish ros message to `/Robot2F-1/state`

    ```bash
    root@rosbridge:/opt/ros_ws# rostopic pub -1 /Robot2F-1/state office_guide_robot/r_state "
    time: '2018-10-09 08:07:06'
    r_mode: 'Navi'
    pos:
      x: 1.15
      y: 1.25
      theta: 1.35
    "
    ```
    * receive MQTT message and send `action|on` message to `dest_led_0000000000000002` authomatically

        ```bash
        Client mosqsub|78142-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000002/attrs', ... (93 bytes))
        2018-08-01T15:01:20.091336+0900|time|2018-10-09 08:07:06|r_mode|Navi|x|1.15|y|1.25|theta|1.35
        Client mosqsub|78142-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/dest_led/dest_led_0000000000000002/cmd', ... (35 bytes))
        dest_led_0000000000000002@action|on
        ```
1. simulate to send `action` cmd result

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /dest_led/dest_led_0000000000000002/cmdexe -u iotagent -P XXXXXXXX -m "dest_led_0000000000000002@action|success"
    Client mosqpub|22763-Nobuyukin sending CONNECT
    Client mosqpub|22763-Nobuyukin received CONNACK
    Client mosqpub|22763-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/dest_led/dest_led_0000000000000002/cmdexe', ... (40 bytes))
    Client mosqpub|22763-Nobuyukin sending DISCONNECT
    ```
1. simulate to receive robot state (Standby)
    * publish ros message to `/Robot2F-1/state`

    ```bash
    root@rosbridge:/opt/ros_ws# rostopic pub -1 /Robot2F-1/state office_guide_robot/r_state "
    time: '2018-10-09 08:07:16'
    r_mode: 'Standby'
    pos:
      x: -35.1
      y: 1.2
      theta: 19.5
    "
    ```
    * receive MQTT message, but don't send `action|on` message to `dest_led` authomatically

        ```bash
        Client mosqsub|78142-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000002/attrs', ... (96 bytes))
        2018-08-01T15:05:02.377134+0900|time|2018-10-09 08:07:16|r_mode|Standby|x|-35.1|y|1.2|theta|19.5
        ```
    * nothing to do when stopping robot

        ```bash
        guidance-857987f97b-7hdmt guidance 2018/08/01 06:05:02 [   INFO] src.views - nothing to do when called stop-movement
        ```

## arrival (floor 1)
1. simuate visitor arriving at the destination

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /dest_human_sensor/dest_human_sensor_0000000000000002/attrs -u iotagent -P XXXXXXXX -m "$d|arrival|$d"
    Client mosqpub|65572-Nobuyukin sending CONNECT
    Client mosqpub|65572-Nobuyukin received CONNACK
    Client mosqpub|65572-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/dest_human_sensor/dest_human_sensor_0000000000000002/attrs', ... (79 bytes))
    Client mosqpub|65572-Nobuyukin sending DISCONNECT
    ```
    * receive MQTT message and send `action|off` message to `dest_led_0000000000000002` and `robot_request` command to `guide_robot_0000000000000002` automatically

        ```bash
        Client mosqsub|78142-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/dest_human_sensor/dest_human_sensor_0000000000000002/attrs', ... (79 bytes))
        2018-08-01T15:08:28.1533103708+0900|arrival|2018-08-01T15:08:28.1533103708+0900
        Client mosqsub|78142-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/dest_led/dest_led_0000000000000002/cmd', ... (36 bytes))
        dest_led_0000000000000002@action|off
        Client mosqsub|78142-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000002/cmd', ... (73 bytes))
        guide_robot_0000000000000002@robot_request|r_cmd|Navi|pos.x|0.0|pos.y|0.0
        Client mosqsub|78142-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000002/cmdexe', ... (113 bytes))
        guide_robot_0000000000000002@robot_request|result,success/time,2018-08-01 15:08:28/r_cmd,Navi/pos.x,0.0/pos.y,0.0
        ```
    * send ros message to ros topic `/Robot2F-1/request` automatically

        ```bash
        root@rosbridge:/opt/ros_ws# rostopic echo /Robot2F-1/request
        time: "2018-08-01 15:08:28"
        r_cmd: "Navi"
        pos:
          x: 0.0
          y: 0.0
        ---
        ```
1. simulate to send `action` cmd result

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /dest_led/dest_led_0000000000000002/cmdexe -u iotagent -P XXXXXXXX -m "dest_led_0000000000000002@action|success"
    Client mosqpub|22763-Nobuyukin sending CONNECT
    Client mosqpub|22763-Nobuyukin received CONNACK
    Client mosqpub|22763-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/dest_led/dest_led_0000000000000002/cmdexe', ... (40 bytes))
    Client mosqpub|22763-Nobuyukin sending DISCONNECT
    ```
1. simulate to receive robot state (Standby)
    * publish ros message to `/Robot2F-1/state`

    ```bash
    root@rosbridge:/opt/ros_ws# rostopic pub -1 /Robot2F-1/state office_guide_robot/r_state "
    time: '2018-10-09 08:07:26'
    r_mode: 'Standby'
    pos:
      x: 0.0
      y: 0.0
      theta: 0.0
    "
    ```
    * receive MQTT message, but don't send `action|on` message to `dest_led` authomatically

        ```bash
        Client mosqsub|78142-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000002/attrs', ... (93 bytes))
        2018-08-01T15:12:28.186635+0900|time|2018-10-09 08:07:26|r_mode|Standby|x|0.0|y|0.0|theta|0.0
        ```
    * nothing to do when stopping robot

        ```bash
        guidance-857987f97b-7hdmt guidance 2018/08/01 06:12:28 [   INFO] src.views - nothing to do when called stop-movement
        ```

## guidance (floor 3)
1. simulate to finish reception (floor 3)

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /pepper/pepper_0000000000000001/attrs -u iotagent -P XXXXXXXX -m "$d|face|/shared/faces/IoYu2c4sggdVLi49.JPEG|dest|ProjectRoom 1"
    Client mosqpub|38060-Nobuyukin sending CONNECT
    Client mosqpub|38060-Nobuyukin received CONNACK
    Client mosqpub|38060-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/attrs', ... (95 bytes))
    Client mosqpub|38060-Nobuyukin sending DISCONNECT
    ```
    * send `handover` command to `pepper(floor 1)` automatically

        ```bash
        Client mosqsub|78142-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/attrs', ... (95 bytes))
        2018-08-01T15:15:12.1533104112+0900|face|/shared/faces/IoYu2c4sggdVLi49.JPEG|dest|ProjectRoom 1
        Client mosqsub|78142-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/cmd', ... (34 bytes))
        pepper_0000000000000001@handover|3
        ```
    * requres slack module

        ```bash
        reception-7895487b-rhc49 reception 2018/08/01 06:15:13 [   INFO] src.slack - 来客がいらっしゃいました。ProjectRoom 1までご案内いたしております
        reception-7895487b-rhc49 reception 2018/08/01 06:15:13 [   INFO] src.views - nothing to do, dest_name=ProjectRoom 1, floor=3
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

## request ofexternal camera
1. simulate to start monitoring of external camera 1F-1

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
    * send `external_camera_request` command to `external_camera_0000000000000011` automatically

        ```bash
        Client mosqsub|78142-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/external_camera/external_camera_0000000000000011/cmd', ... (70 bytes))
        external_camera_0000000000000011@external_camera_request|c_cmd|Monitor
        Client mosqsub|78142-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/external_camera/external_camera_0000000000000011/cmdexe', ... (110 bytes))
        external_camera_0000000000000011@external_camera_request|result,success/time,2018-08-01 15:26:20/c_cmd,Monitor
        ```
    * send ros message to ros topic `/ExternalCamera1F-1/request` automatically

        ```bash
        root@rosbridge:/opt/ros_ws# rostopic type /ExternalCamera1F-1/request
        external_camera/c_req
        ```
        ```bash
        root@rosbridge:/opt/ros_ws# rostopic echo /ExternalCamera1F-1/request
        time: "2018-08-01 15:26:20"
        c_cmd: "Monitor"
        ---
        ```
1. simulate to stop monitoring of external camera 1F-2

    ```bash
    mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: camera" -H "Fiware-Servicepath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v1/updateContext -d @-<<__EOS__ | jq .
    {
      "contextElements": [
        {
          "id": "external_camera_0000000000000012",
          "isPattern": "false",
          "type": "external_camera",
          "attributes": [
            {
              "name": "external_camera_request",
              "value": "c_cmd|Standby"
            }
          ]
        }
      ],
      "updateAction": "UPDATE"
    }
    __EOS__
    ```
    * send `external_camera_request` command to `external_camera_0000000000000012` automatically

        ```bash
        Client mosqsub|78142-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/external_camera/external_camera_0000000000000012/cmd', ... (70 bytes))
        external_camera_0000000000000012@external_camera_request|c_cmd|Standby
        Client mosqsub|78142-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/external_camera/external_camera_0000000000000012/cmdexe', ... (110 bytes))
        external_camera_0000000000000012@external_camera_request|result,success/time,2018-08-01 15:29:56/c_cmd,Standby
        ```
    * send ros message to ros topic `/ExternalCamera1F-2/request` automatically

        ```bash
        root@rosbridge:/opt/ros_ws# rostopic type /ExternalCamera1F-2/request
        external_camera/c_req
        ```
        ```bash
        root@rosbridge:/opt/ros_ws# rostopic echo /ExternalCamera1F-1/request
        time: "2018-08-01 15:29:56"
        c_cmd: "Standby"
        ---
        ```
1. simulate to start monitoring of external camera 2F-1

    ```bash
    mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: camera" -H "Fiware-Servicepath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v1/updateContext -d @-<<__EOS__ | jq .
    {
      "contextElements": [
        {
          "id": "external_camera_0000000000000021",
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
    * send `external_camera_request` command to `external_camera_0000000000000021` automatically

        ```bash
        Client mosqsub|78142-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/external_camera/external_camera_0000000000000021/cmd', ... (70 bytes))
        external_camera_0000000000000021@external_camera_request|c_cmd|Monitor
        Client mosqsub|78142-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/external_camera/external_camera_0000000000000021/cmdexe', ... (110 bytes))
        external_camera_0000000000000021@external_camera_request|result,success/time,2018-08-01 15:34:20/c_cmd,Monitor
        ```
    * send ros message to ros topic `/ExternalCamera2F-1/request` automatically

        ```bash
        root@rosbridge:/opt/ros_ws# rostopic type /ExternalCamera2F-1/request
        external_camera/c_req
        ```
        ```bash
        root@rosbridge:/opt/ros_ws# rostopic echo /ExternalCamera2F-1/request
        time: "2018-08-01 15:34:20"
        c_cmd: "Monitor"
        ---
        ```

## state of external camera
1. simulate to receive the state of external camera 1F-1
    * publish ros message to `/ExternalCamera1F-1/state`

    ```bash
    root@rosbridge:/opt/ros_ws# rostopic pub -1 /ExternalCamera1F-1/state external_camera/c_state "
    time: '2018-02-03 04:05:06'
    c_mode: 'Monitor'
    num_p: 0
    "
    ```
    * recieve MQTT message

        ```bash
        Client mosqsub|78142-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/external_camera/external_camera_0000000000000011/attrs', ... (90 bytes))
        2018-08-01T15:54:53.797550+0900|time|2018-02-03 04:05:06|c_mode|Monitor|num_p|0|position|-
        ```
    * confirm mogodb records registered within 3 minuntes

        ```bash
        mac:$ kubectl exec mongodb-0 -c mongodb -- mongo sth_camera --eval 'db.getCollection("sth_/_external_camera_0000000000000011_external_camera").find({recvTime: { "$gte": new Date(ISODate().getTime() - 1000 * 60 * 3)}})'
        MongoDB shell version v3.6.5
        connecting to: mongodb://127.0.0.1:27017/sth_camera
        MongoDB server version: 3.6.5
        { "_id" : ObjectId("5b615b39f8a94e000a6eaf84"), "recvTime" : ISODate("2018-08-01T07:03:19.074Z"), "attrName" : "c_mode", "attrType" : "string", "attrValue" : "Monitor" }
        { "_id" : ObjectId("5b615b39f8a94e000a6eaf87"), "recvTime" : ISODate("2018-08-01T07:03:19.074Z"), "attrName" : "num_p", "attrType" : "int", "attrValue" : "0" }
        { "_id" : ObjectId("5b615b39f8a94e000a6eaf88"), "recvTime" : ISODate("2018-08-01T07:03:19.074Z"), "attrName" : "position", "attrType" : "string", "attrValue" : "-" }
        { "_id" : ObjectId("5b615b39f8a94e000a6eaf89"), "recvTime" : ISODate("2018-08-01T07:03:19.074Z"), "attrName" : "time", "attrType" : "string", "attrValue" : "2018-02-03 04:05:06" }
        ```
1. simulate to receive the state of external camera 1F-2
    * publish ros message to `/ExternalCamera1F-2/state`

    ```bash
    root@rosbridge:/opt/ros_ws# rostopic pub -1 /ExternalCamera1F-2/state external_camera/c_state "
    time: '2018-02-03 04:15:16'
    c_mode: 'Standby'
    num_p: 1
    position:
      - x: 1.0
        y: 1.1
    "
    ```
    * recieve MQTT message

        ```bash
        Client mosqsub|78142-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/external_camera/external_camera_0000000000000012/attrs', ... (106 bytes))
        2018-08-01T16:15:19.717449+0900|time|2018-02-03 04:15:16|c_mode|Standby|num_p|1|position|x[0],1.0/y[0],1.1
        ```
    * confirm mogodb records registered within 3 minuntes

        ```bash
        mac:$ kubectl exec mongodb-0 -c mongodb -- mongo sth_camera --eval 'db.getCollection("sth_/_external_camera_0000000000000012_external_camera").find({recvTime: { "$gte": new Date(ISODate().getTime() - 1000 * 60 * 3)}})'
        MongoDB shell version v3.6.5
        connecting to: mongodb://127.0.0.1:27017/sth_camera
        MongoDB server version: 3.6.5
        { "_id" : ObjectId("5b615e07c22929000a69ffc5"), "recvTime" : ISODate("2018-08-01T07:15:19.847Z"), "attrName" : "c_mode", "attrType" : "string", "attrValue" : "Standby" }
        { "_id" : ObjectId("5b615e07c22929000a69ffc8"), "recvTime" : ISODate("2018-08-01T07:15:19.847Z"), "attrName" : "num_p", "attrType" : "int", "attrValue" : "1" }
        { "_id" : ObjectId("5b615e07c22929000a69ffc9"), "recvTime" : ISODate("2018-08-01T07:15:19.847Z"), "attrName" : "position", "attrType" : "string", "attrValue" : "x[0],1.0/y[0],1.1" }
        { "_id" : ObjectId("5b615e07c22929000a69ffca"), "recvTime" : ISODate("2018-08-01T07:15:19.847Z"), "attrName" : "time", "attrType" : "string", "attrValue" : "2018-02-03 04:15:16" }
        ```
1. simulate to receive the state of external camera 2F-1
    * publish ros message to `/ExternalCamera2F-1/state`

    ```bash
    root@rosbridge:/opt/ros_ws# rostopic pub -1 /ExternalCamera2F-1/state external_camera/c_state "
    time: '2018-02-03 04:25:26'
    c_mode: 'Error'
    num_p: 2
    position:
      - x: 1.0
        y: 1.1
      - x: 2.0
        y: 2.1
    "
    ```
    * recieve MQTT message

        ```bash
        Client mosqsub|78142-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/external_camera/external_camera_0000000000000021/attrs', ... (122 bytes))
        2018-08-01T16:17:45.661304+0900|time|2018-02-03 04:25:26|c_mode|Error|num_p|2|position|x[0],1.0/y[0],1.1/x[1],2.0/y[1],2.1
        ```
    * confirm mogodb records registered within 3 minuntes

        ```bash
        mac:$ kubectl exec mongodb-0 -c mongodb -- mongo sth_camera --eval 'db.getCollection("sth_/_external_camera_0000000000000021_external_camera").find({recvTime: { "$gte": new Date(ISODate().getTime() - 1000 * 60 * 3)}})'
        MongoDB shell version v3.6.5
        connecting to: mongodb://127.0.0.1:27017/sth_camera
        MongoDB server version: 3.6.5
        { "_id" : ObjectId("5b615e9dc22929000a69ffcb"), "recvTime" : ISODate("2018-08-01T07:17:45.788Z"), "attrName" : "c_mode", "attrType" : "string", "attrValue" : "Error" }
        { "_id" : ObjectId("5b615e9dc22929000a69ffce"), "recvTime" : ISODate("2018-08-01T07:17:45.788Z"), "attrName" : "num_p", "attrType" : "int", "attrValue" : "2" }
        { "_id" : ObjectId("5b615e9dc22929000a69ffcf"), "recvTime" : ISODate("2018-08-01T07:17:45.788Z"), "attrName" : "position", "attrType" : "string", "attrValue" : "x[0],1.0/y[0],1.1/x[1],2.0/y[1],2.1" }
        { "_id" : ObjectId("5b615e9dc22929000a69ffd0"), "recvTime" : ISODate("2018-08-01T07:17:45.788Z"), "attrName" : "time", "attrType" : "string", "attrValue" : "2018-02-03 04:25:26" }
        ```
