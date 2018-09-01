# 5. simulate scenario

## preparation
* start roscore & rosbridge on guide robot and external camera
* echo request topic of guide robot and external camera like below:
    * `rostopic echo /robot_1f_1/request`
    * `rostopic echo /robot_2f_1/request`
    * `rostopic echo /external_camera_1f_1/request`
    * `rostopic echo /external_camera_1f_2/request`
    * `rostopic echo /external_camera_2f_1/request`


## initialize
1. set `r_state` of guide robot as `Waiting`

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v1/updateContext -d @-<<__EOS__ | jq .
    {
      "contextElements": [
        {
          "id": "guide_robot_0000000000000001",
          "isPattern": "false",
          "type": "guide_robot",
          "attributes": [
            {
              "name": "r_state",
              "value": "Waiting",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }, {
              "name": "destx",
              "value": "",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }, {
              "name": "desty",
              "value": "",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }, {
              "name": "visitor",
              "value": "",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }
          ]
        }
      ],
      "updateAction": "UPDATE"
    }
    __EOS__
    ```
    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v1/updateContext -d @-<<__EOS__ | jq .
    {
      "contextElements": [
        {
          "id": "guide_robot_0000000000000002",
          "isPattern": "false",
          "type": "guide_robot",
          "attributes": [
            {
              "name": "r_state",
              "value": "Waiting",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }, {
              "name": "destx",
              "value": "",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }, {
              "name": "desty",
              "value": "",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }, {
              "name": "visitor",
              "value": "",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }
          ]
        }
      ],
      "updateAction": "UPDATE"
    }
    __EOS__
    ```
    ```bash
    mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000001/attrs/r_state | jq .
    {
      "type": "string",
      "value": "Waiting",
      "metadata": {
        "TimeInstant": {
          "type": "ISO8601",
          "value": "2018-08-08T19:00:18.1533722418+0900"
        }
      }
    }
    ```
    ```bash
    mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000002/attrs/r_state | jq .
    {
      "type": "string",
      "value": "Waiting",
      "metadata": {
        "TimeInstant": {
          "type": "ISO8601",
          "value": "2018-08-08T19:00:25.1533722425+0900"
        }
      }
    }
    ```

## reception
1. subscribe all topics

    ```bash
    mac:$ mosquitto_sub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /# -u iotagent -P XXXXXXXX
    ```
1. simulate to push button of `button_sensor`

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /button_sensor/button_sensor_0000000000000001/attrs -u iotagent -P XXXXXXXX -m "$d|state|on"
    Client mosqpub|52223-Nobuyukin sending CONNECT
    Client mosqpub|52223-Nobuyukin received CONNACK
    Client mosqpub|52223-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/button_sensor/button_sensor_0000000000000001/attrs', ... (44 bytes))
    Client mosqpub|52223-Nobuyukin sending DISCONNECT
    ```
    * send 'welcome' command to `pepper` automatically when receiving the `state|on` command from `button_sensor`

        ```bash
        mac:$ mosquitto_sub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /# -u iotagent -P XXXXXXXX
        ...
        Client mosqsub|86059-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/button_sensor/button_sensor_0000000000000001/attrs', ... (44 bytes))
        2018-08-08T19:01:28.1533722488+0900|state|on
        Client mosqsub|86059-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/cmd', ... (37 bytes))
        pepper_0000000000000001@welcome|start
        ```
1. simlate to be called `/destinations/` REST API by `pepper`

    ```bash
    mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" https://api.tech-sketch.jp/destinations/ | jq .
    [
      {
        "dest_human_sensor_id": "dest_human_sensor_0000000000000001",
        "dest_led_id": "dest_led_0000000000000001",
        "dest_led_pos_x": -9,
        "dest_led_pos_y": 9,
        "dest_pos_x": -10,
        "dest_pos_y": 10,
        "floor": 1,
        "id": "5b63d66d7597100013d0b2a7",
        "name": "管理センター"
      },
      {
        "dest_human_sensor_id": "dest_human_sensor_0000000000000002",
        "dest_led_id": "dest_led_0000000000000002",
        "dest_led_pos_x": 19,
        "dest_led_pos_y": 19,
        "dest_pos_x": 20,
        "dest_pos_y": 20,
        "floor": 2,
        "id": "5b63d672f6f8a80013b85abf",
        "name": "203号室"
      },
      {
        "dest_human_sensor_id": "dest_human_sensor_0000000000000003",
        "dest_led_id": "dest_led_0000000000000003",
        "dest_led_pos_x": 19,
        "dest_led_pos_y": -19,
        "dest_pos_x": 20,
        "dest_pos_y": -10,
        "floor": 2,
        "id": "5b63d6787597100013d0b2a9",
        "name": "204号室"
      },
      {
        "dest_human_sensor_id": null,
        "dest_led_id": null,
        "dest_led_pos_x": null,
        "dest_led_pos_y": null,
        "dest_pos_x": null,
        "dest_pos_y": null,
        "floor": 3,
        "id": "5b63d67c7597100013d0b2ab",
        "name": "ProjectRoom 1",
        "slack_webhook": "https://hooks.slack.com/services/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
      }
    ]
    ```

## guidance (floor 1)
1. simulate to finish reception (floor 1)

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000001/attrs -u iotagent -P XXXXXXXX -m "$d|face|null|dest|管理センター"
    Client mosqpub|37117-Nobuyukin sending CONNECT
    Client mosqpub|37117-Nobuyukin received CONNACK
    Client mosqpub|37117-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/attrs', ... (100 bytes))
    Client mosqpub|37117-Nobuyukin sending DISCONNECT
    ```
    * send `handover` command to `pepper(floor 1)` and `robot_request` command to `guide_robot` automatically

        ```bash
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/attrs', ... (69 bytes))
        2018-08-08T19:02:34.1533722554+0900|face|null|dest|管理センター
        Client mosqsub|86059-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/cmd', ... (34 bytes))
        pepper_0000000000000001@handover|1
        Client mosqsub|86059-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000001/cmd', ... (68 bytes))
        guide_robot_0000000000000001@robot_request|r_cmd|Navi|x|-10.0|y|10.0
        Client mosqsub|86059-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000001/cmdexe', ... (108 bytes))
        guide_robot_0000000000000001@robot_request|result,success/time,2018-08-08 19:02:35/r_cmd,Navi/x,-10.0/y,10.0
        ```
    * send ros message to ros topic `/robot_1f_1/request` automatically

        ```bash
        root@rosbridge:/opt/ros_ws# rostopic type /robot_1f_1/request
        office_guide_robot/r_req
        ```
        ```bash
        root@rosbridge:/opt/ros_ws# rostopic echo /robot_1f_1/request
        time: "2018-08-08 19:02:35"
        r_cmd: "Navi"
        pos:
          x: -10.0
          y: 10.0
        --- 
        ```
    * update `r_state` to `Guiding` automatically

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000001/attrs/r_state/ | jq .
        {
          "type": "string",
          "value": "Guiding",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-08T19:02:35.179639+0900"
            }
          }
        }
        ```
    * set `visitor` automatically

        ```bash
        $ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000001/attrs/visitor/ | jq .
        {
          "type": "string",
          "value": "5b6abfbb393f5f00136ecea0",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-08T19:02:35.179639+0900"
            }
          }
        }
        ```
    * record ledger automatically

        ```bash
        mac:$ kubectl exec mongodb-0 -c mongodb -- mongo ledger --eval 'db.visitors.find().sort({"receptionDatetime":-1}).limit(1).pretty()'
        MongoDB shell version v3.6.5
        connecting to: mongodb://127.0.0.1:27017/ledger
        MongoDB server version: 3.6.5
        {
          "_id" : ObjectId("5b6abfbb393f5f00136ecea0"),
          "status" : "reception",
          "face" : null,
          "faceIds" : [ ],
          "dest" : {
            "dest_human_sensor_id" : "dest_human_sensor_0000000000000001",
            "dest_led_id" : "dest_led_0000000000000001",
            "dest_led_pos_x" : -9,
            "dest_led_pos_y" : 9,
            "dest_pos_x" : -10,
            "dest_pos_y" : 10,
            "floor" : 1,
            "id" : "5b63d66d7597100013d0b2a7",
            "name" : "管理センター"
          },
          "receptionDatetime" : ISODate("2018-08-08T10:02:35.092Z")
        }
        ```
1. simulate to send `welcome` cmd result from `pepper(floor 1)`

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000001/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000001@welcome|success"
    Client mosqpub|22365-Nobuyukin sending CONNECT
    Client mosqpub|22365-Nobuyukin received CONNACK
    Client mosqpub|22365-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/cmdexe', ... (39 bytes))
    Client mosqpub|22365-Nobuyukin sending DISCONNECT
    ```
1. simulate to send `handover` cmd result from `pepper(floor 1)`

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000001/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000001@handover|success"
    Client mosqpub|22763-Nobuyukin sending CONNECT
    Client mosqpub|22763-Nobuyukin received CONNACK
    Client mosqpub|22763-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/cmdexe', ... (40 bytes))
    Client mosqpub|22763-Nobuyukin sending DISCONNECT
    ```

## navigating (floor 1)
1. simulate to receive robot state (Navi)
    * publish ros message to `/robot_1f_1/state` near the start position

    ```bash
    root@rosbridge:/opt/ros_ws# rostopic pub -1 /robot_1f_1/state office_guide_robot/r_state "
    time: '2018-09-08 07:06:01'
    r_mode: 'Navi'
    pos:
      x: -1.1
      y: 1.2
      theta: 0.3
    "
    ```
    * receive MQTT message but no action occured

        ```bash
        Client mosqsub|86059-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000001/attrs', ... (91 bytes))
        2018-08-08T19:08:26.322076+0900|time|2018-09-08 07:06:01|r_mode|Navi|x|-1.1|y|1.2|theta|0.3
        ```
    * publish ros message to `/robot_1f_1/state` near the `dest_led_pos`

    ```bash
    root@rosbridge:/opt/ros_ws# rostopic pub -1 /robot_1f_1/state office_guide_robot/r_state "
    time: '2018-09-08 07:06:05'
    r_mode: 'Navi'
    pos:
      x: -9.05
      y: 9.1
      theta: 0.3
    "
    ```
    * receive MQTT message and send `action|on` message to `dest_led_0000000000000001` authomatically

        ```bash
        Client mosqsub|86059-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000001/attrs', ... (92 bytes))
        2018-08-08T19:08:54.428282+0900|time|2018-09-08 07:06:05|r_mode|Navi|x|-9.05|y|9.1|theta|0.3
        Client mosqsub|86059-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/dest_led/dest_led_0000000000000001/cmd', ... (35 bytes))
        dest_led_0000000000000001@action|on
        ```
1. simulate to send `action` cmd result

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /dest_led/dest_led_0000000000000001/cmdexe -u iotagent -P XXXXXXXX -m "dest_led_0000000000000001@action|success"
    Client mosqpub|22763-Nobuyukin sending CONNECT
    Client mosqpub|22763-Nobuyukin received CONNACK
    Client mosqpub|22763-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/dest_led/dest_led_0000000000000001/cmdexe', ... (40 bytes))
    Client mosqpub|22763-Nobuyukin sending DISCONNECT
    ```
1. simulate to receive robot state (Standby)
    * publish ros message to `/robot_1f_1/state`

    ```bash
    root@rosbridge:/opt/ros_ws# rostopic pub -1 /robot_1f_1/state office_guide_robot/r_state "
    time: '2018-09-08 07:06:15'
    r_mode: 'Standby'
    pos:
      x: -10.01
      y: 10.02
      theta: 9.1
    "
    ```
    * receive MQTT message, but don't send `action|on` message to `dest_led` authomatically

        ```bash
        Client mosqsub|86059-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000001/attrs', ... (98 bytes))
        2018-08-08T19:10:40.602383+0900|time|2018-09-08 07:06:15|r_mode|Standby|x|-10.01|y|10.02|theta|9.1
        ```
    * update `r_state` to `Suspending` automatically

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000001/attrs/r_state/ | jq .
        {
          "type": "string",
          "value": "Suspending",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-08T19:10:40.684193+0900"
            }
          }
        }
        ```

## arrival (floor 1)
1. simuate visitor arriving at the destination

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /dest_human_sensor/dest_human_sensor_0000000000000001/attrs -u iotagent -P XXXXXXXX -m "$d|arrival|$d"
    Client mosqpub|65572-Nobuyukin sending CONNECT
    Client mosqpub|65572-Nobuyukin received CONNACK
    Client mosqpub|65572-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/dest_human_sensor/dest_human_sensor_0000000000000001/attrs', ... (79 bytes))
    Client mosqpub|65572-Nobuyukin sending DISCONNECT
    ```
    * receive MQTT message and send `action|off` message to `dest_led_0000000000000001` and `robot_request` command to `guide_robot_0000000000000001` automatically

        ```bash
        Client mosqsub|86059-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/dest_human_sensor/dest_human_sensor_0000000000000001/attrs', ... (79 bytes))
        2018-08-08T19:28:01.1533724081+0900|arrival|2018-08-08T19:28:01.1533724081+0900
        Client mosqsub|86059-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/dest_led/dest_led_0000000000000001/cmd', ... (36 bytes))
        dest_led_0000000000000001@action|off
        Client mosqsub|86059-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000001/cmd', ... (65 bytes))
        guide_robot_0000000000000001@robot_request|r_cmd|Navi|x|0.0|y|0.0
        Client mosqsub|86059-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000001/cmdexe', ... (105 bytes))
        guide_robot_0000000000000001@robot_request|result,success/time,2018-08-08 19:28:02/r_cmd,Navi/x,0.0/y,0.0
        ```
    * send ros message to ros topic `/robot_1f_1/request` automatically

        ```bash
        root@rosbridge:/opt/ros_ws# rostopic echo /robot_1f_1/request
        time: "2018-08-08 19:28:02"
        r_cmd: "Navi"
        pos:
          x: 0.0
          y: 0.0
        ---
        ```
    * update `r_state` to `Returning` automatically

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000001/attrs/r_state/ | jq .
        {
          "type": "string",
          "value": "Returning",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-08T19:28:02.283736+0900"
            }
          }
        }
        ```
    * reset `visitor` automatically

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000001/attrs/visitor/ | jq .
        {
          "type": "string",
          "value": "",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-08T19:28:02.191985+0900"
            }
          }
        }
        ```
    * record ledger automatically

        ```bash
        mac:$ kubectl exec mongodb-0 -c mongodb -- mongo ledger --eval 'db.visitors.find().sort({"receptionDatetime":-1}).limit(1).pretty()'
        MongoDB shell version v3.6.5
        connecting to: mongodb://127.0.0.1:27017/ledger
        MongoDB server version: 3.6.5
        {
          "_id" : ObjectId("5b6ac3c46a77d600136cbcb7"),
          "status" : "arrival",
          "face" : null,
          "faceIds" : [ ],
          "dest" : {
            "dest_human_sensor_id" : "dest_human_sensor_0000000000000001",
            "dest_led_id" : "dest_led_0000000000000001",
            "dest_led_pos_x" : -9,
            "dest_led_pos_y" : 9,
            "dest_pos_x" : -10,
            "dest_pos_y" : 10,
            "floor" : 1,
            "id" : "5b63d66d7597100013d0b2a7",
            "name" : "管理センター"
          },
          "receptionDatetime" : ISODate("2018-08-08T10:19:48.533Z"),
          "arrivalDatetime" : ISODate("2018-08-08T10:28:02.181Z")
        }
        ```
1. simulate to send `action` cmd result

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /dest_led/dest_led_0000000000000001/cmdexe -u iotagent -P XXXXXXXX -m "dest_led_0000000000000001@action|success"
    Client mosqpub|22763-Nobuyukin sending CONNECT
    Client mosqpub|22763-Nobuyukin received CONNACK
    Client mosqpub|22763-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/dest_led/dest_led_0000000000000001/cmdexe', ... (40 bytes))
    Client mosqpub|22763-Nobuyukin sending DISCONNECT
    ```
1. simulate to receive robot state (Navi)
    * publish ros message to `/robot_1f_1/state` near the dest position

    ```bash
    root@rosbridge:/opt/ros_ws# rostopic pub -1 /robot_1f_1/state office_guide_robot/r_state "
    time: '2018-09-08 07:06:21'
    r_mode: 'Navi'
    pos:
      x: -9.99
      y: 10.01
      theta: 3.3
    "
    ```
    * receive MQTT message, but no action occured

        ```bash
        Client mosqsub|86059-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000001/attrs', ... (94 bytes))
        2018-08-08T19:31:27.929171+0900|time|2018-09-08 07:06:21|r_mode|Navi|x|-9.99|y|10.01|theta|3.3
        ```
    * publish ros message to `/robot_1f_1/state` near the `dest_led_pos`

    ```bash
    root@rosbridge:/opt/ros_ws# rostopic pub -1 /robot_1f_1/state office_guide_robot/r_state "
    time: '2018-09-08 07:06:22'
    r_mode: 'Navi'
    pos:
      x: -9.05
      y: 9.1
      theta: 3.3
    "
    ```
    * receive MQTT message but no action occured

        ```bash
        Client mosqsub|86059-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000001/attrs', ... (92 bytes))
        2018-08-08T19:33:38.920621+0900|time|2018-09-08 07:06:22|r_mode|Navi|x|-9.05|y|9.1|theta|3.3
        ```
1. simulate to receive robot state (Standby)
    * publish ros message to `/robot_1f_1/state`

    ```bash
    root@rosbridge:/opt/ros_ws# rostopic pub -1 /robot_1f_1/state office_guide_robot/r_state "
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
        Client mosqsub|86059-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000001/attrs', ... (93 bytes))
        2018-08-08T19:35:42.490765+0900|time|2018-09-08 07:06:15|r_mode|Standby|x|0.0|y|0.0|theta|0.0
        ```
    * update `r_state` to `Waiting` automatically

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000001/attrs/r_state/ | jq .
        {
          "type": "string",
          "value": "Waiting",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-08T19:35:42.601126+0900"
            }
          }
        }
        ```

## guidance (floor 2)
1. simulate to be called `/storage/faces/` REST API by pepper(floor 1)

    ```bash
    mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);export FACEPATH=$(curl -sS -H "Authorization: bearer ${TOKEN}" -H "Content-Type: multipart/form-data" https://api.tech-sketch.jp/storage/faces/ -X POST -F face=@face.jpg | jq .path -r);echo ${FACEPATH}
    /shared/faces/tZGqEzEEvuc8jhw0.JPEG
    ```
1. simulate to finish reception (floor 2)

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000001/attrs -u iotagent -P XXXXXXXX -m "$d|face|${FACEPATH}|dest|203号室"
    Client mosqpub|37447-Nobuyukin sending CONNECT
    Client mosqpub|37447-Nobuyukin received CONNACK
    Client mosqpub|37447-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/attrs', ... (91 bytes))
    Client mosqpub|37447-Nobuyukin sending DISCONNECT
    ```
    * send `handover` command to `pepper(floor 1)` and `facedetect` command to `pepper(floor 2)` automatically

        ```bash
        Client mosqsub|86059-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/attrs', ... (91 bytes))
        2018-08-08T19:44:26.1533725066+0900|face|/shared/faces/tZGqEzEEvuc8jhw0.JPEG|dest|203号室
        Client mosqsub|86059-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000002/cmd', ... (40 bytes))
        pepper_0000000000000002@facedetect|start
        Client mosqsub|86059-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/cmd', ... (34 bytes))
        pepper_0000000000000001@handover|2
        ```
    * record ledger automatically

        ```bash
        mac:$ kubectl exec mongodb-0 -c mongodb -- mongo ledger --eval 'db.visitors.find().sort({"receptionDatetime":-1}).limit(1).pretty()'
        MongoDB shell version v3.6.5
        connecting to: mongodb://127.0.0.1:27017/ledger
        MongoDB server version: 3.6.5
        {
          "_id" : ObjectId("5b6ac98b393f5f00136ecea3"),
          "status" : "reception",
          "face" : "/shared/faces/tZGqEzEEvuc8jhw0.JPEG",
          "faceIds" : [
            "a74b8913-ccf7-44b9-af17-953ddd1bedae",
            "991e9292-5e75-4fa7-b0be-67e001007cef"
          ],
          "dest" : {
            "dest_human_sensor_id" : "dest_human_sensor_0000000000000002",
            "dest_led_id" : "dest_led_0000000000000002",
            "dest_led_pos_x" : 19,
            "dest_led_pos_y" : 19,
            "dest_pos_x" : 20,
            "dest_pos_y" : 20,
            "floor" : 2,
            "id" : "5b63d672f6f8a80013b85abf",
            "name" : "203号室"
          },
          "receptionDatetime" : ISODate("2018-08-08T10:44:26.530Z")
        }
        ```
1. simulate to send `welcome` cmd result from `pepper(floor 1)`

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000001/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000001@welcome|success"
    Client mosqpub|22365-Nobuyukin sending CONNECT
    Client mosqpub|22365-Nobuyukin received CONNACK
    Client mosqpub|22365-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/cmdexe', ... (39 bytes))
    Client mosqpub|22365-Nobuyukin sending DISCONNECT
    ```
1. simulate to send `handover` cmd result from `pepper(floor 1)`

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000001/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000001@handover|success"
    Client mosqpub|22763-Nobuyukin sending CONNECT
    Client mosqpub|22763-Nobuyukin received CONNACK
    Client mosqpub|22763-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/cmdexe', ... (40 bytes))
    Client mosqpub|22763-Nobuyukin sending DISCONNECT
    ```

## face detection (floor 2)
1. simulate to be called `/storage/faces/` REST API by pepper(floor 2)

    ```bash
    mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);export FACEPATH=$(curl -sS -H "Authorization: bearer ${TOKEN}" -H "Content-Type: multipart/form-data" https://api.tech-sketch.jp/storage/faces/ -X POST -F face=@another_face.jpg | jq .path -r);echo ${FACEPATH}
    /shared/faces/JFbVvPd1MW0hvWhP.JPEG
    ```
1. simulate to detect visitor

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000002/attrs -u iotagent -P XXXXXXXX -m "$d|face|${FACEPATH}"
    Client mosqpub|97057-Nobuyukin sending CONNECT
    Client mosqpub|97057-Nobuyukin received CONNACK
    Client mosqpub|97057-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000002/attrs', ... (76 bytes))
    Client mosqpub|97057-Nobuyukin sending DISCONNECT
    ```
    * send `handover` command to `pepper(floor 2)` and `robot_request` command to `guide_robot` automatically

        ```bash
        Client mosqsub|86059-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000002/attrs', ... (76 bytes))
        2018-08-08T19:49:52.1533725392+0900|face|/shared/faces/JFbVvPd1MW0hvWhP.JPEG
        Client mosqsub|86059-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000002/cmd', ... (41 bytes))
        pepper_0000000000000002@handover|continue
        Client mosqsub|86059-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000002/cmd', ... (67 bytes))
        guide_robot_0000000000000002@robot_request|r_cmd|Navi|x|20.0|y|20.0
        Client mosqsub|86059-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000002/cmdexe', ... (107 bytes))
        guide_robot_0000000000000002@robot_request|result,success/time,2018-08-08 19:49:53/r_cmd,Navi/x,20.0/y,20.0
        ```
    * send ros message to ros topic `/robot_2f_1/request` automatically

        ```bash
        root@rosbridge:/opt/ros_ws# rostopic type /robot_2f_1/request
        office_guide_robot/r_req
        ```
        ```bash
        root@rosbridge:/opt/ros_ws# rostopic echo /robot_2f_1/request
        time: "2018-08-08 19:49:53"
        r_cmd: "Navi"
        pos:
          x: 20.0
          y: 20.0
        ---
        ```
    * update `r_state` to `Guiding` automatically

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000002/attrs/r_state/ | jq .
        {
          "type": "string",
          "value": "Guiding",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-08T19:49:53.370281+0900"
            }
          }
        }
        ```
    * set `visitor` automatically

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000002/attrs/visitor/ | jq .
        {
          "type": "string",
          "value": "5b6ac98b393f5f00136ecea3",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-08T19:49:53.370281+0900"
            }
          }
        }
        ```
1. simulate to send `facedetect` cmd result from `pepper(floor 2)`

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000002/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000002@facedetect|success"
    Client mosqpub|48535-Nobuyukin sending CONNECT
    Client mosqpub|48535-Nobuyukin received CONNACK
    Client mosqpub|48535-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000002/cmdexe', ... (42 bytes))
    Client mosqpub|48535-Nobuyukin sending DISCONNECT
    ```
1. simulate to send `handover` cmd result from `pepper(floor 2)`

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000002/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000002@handover|success"
    Client mosqpub|48779-Nobuyukin sending CONNECT
    Client mosqpub|48779-Nobuyukin received CONNACK
    Client mosqpub|48779-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000002/cmdexe', ... (40 bytes))
    Client mosqpub|48779-Nobuyukin sending DISCONNECT
    ```

## navigating (floor 2)
1. simulate to receive robot state (Navi)
    * publish ros message to `/robot_1f_1/state` near the start position

    ```bash
    root@rosbridge:/opt/ros_ws# rostopic pub -1 /robot_2f_1/state office_guide_robot/r_state "
    time: '2018-10-09 08:07:01'
    r_mode: 'Navi'
    pos:
      x: 1.1
      y: 1.2
      theta: 0.3
    "
    ```
    * receive MQTT message but no action occured

        ```bash
        Client mosqsub|86059-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000002/attrs', ... (90 bytes))
        2018-08-08T19:52:51.816335+0900|time|2018-10-09 08:07:01|r_mode|Navi|x|1.1|y|1.2|theta|0.3
        ```
    * publish ros message to `/robot_2f_1/state` near the `dest_led_pos`

    ```bash
    root@rosbridge:/opt/ros_ws# rostopic pub -1 /robot_2f_1/state office_guide_robot/r_state "
    time: '2018-10-09 08:07:06'
    r_mode: 'Navi'
    pos:
      x: 19.05
      y: 18.98
      theta: 1.35
    "
    ```
    * receive MQTT message and send `action|on` message to `dest_led_0000000000000002` authomatically

        ```bash
        Client mosqsub|86059-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000002/attrs', ... (95 bytes))
        2018-08-08T19:53:24.329222+0900|time|2018-10-09 08:07:06|r_mode|Navi|x|19.05|y|18.98|theta|1.35
        Client mosqsub|86059-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/dest_led/dest_led_0000000000000002/cmd', ... (35 bytes))
        dest_led_0000000000000002@action|on
        ```
1. simulate to send `action` cmd result

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /dest_led/dest_led_0000000000000002/cmdexe -u iotagent -P XXXXXXXX -m "dest_led_0000000000000002@action|success"
    Client mosqpub|22763-Nobuyukin sending CONNECT
    Client mosqpub|22763-Nobuyukin received CONNACK
    Client mosqpub|22763-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/dest_led/dest_led_0000000000000002/cmdexe', ... (40 bytes))
    Client mosqpub|22763-Nobuyukin sending DISCONNECT
    ```
1. simulate to receive robot state (Standby)
    * publish ros message to `/robot_2f_1/state`

    ```bash
    root@rosbridge:/opt/ros_ws# rostopic pub -1 /robot_2f_1/state office_guide_robot/r_state "
    time: '2018-10-09 08:07:16'
    r_mode: 'Standby'
    pos:
      x: 20.0
      y: 20.2
      theta: 19.5
    "
    ```
    * receive MQTT message, but don't send `action|on` message to `dest_led` authomatically

        ```bash
        Client mosqsub|86059-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000002/attrs', ... (96 bytes))
        2018-08-08T19:54:22.826260+0900|time|2018-10-09 08:07:16|r_mode|Standby|x|20.0|y|20.2|theta|19.5
        ```
    * update `r_state` to `Suspending` automatically

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000002/attrs/r_state/ | jq .
        {
          "type": "string",
          "value": "Suspending",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-08T19:54:22.924134+0900"
            }
          }
        }
        ```

## arrival (floor 2)
1. simuate visitor arriving at the destination

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /dest_human_sensor/dest_human_sensor_0000000000000002/attrs -u iotagent -P XXXXXXXX -m "$d|arrival|$d"
    Client mosqpub|65572-Nobuyukin sending CONNECT
    Client mosqpub|65572-Nobuyukin received CONNACK
    Client mosqpub|65572-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/dest_human_sensor/dest_human_sensor_0000000000000002/attrs', ... (79 bytes))
    Client mosqpub|65572-Nobuyukin sending DISCONNECT
    ```
    * receive MQTT message and send `action|off` message to `dest_led_0000000000000002` and `robot_request` command to `guide_robot_0000000000000002` automatically

        ```bash
        Client mosqsub|86059-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/dest_human_sensor/dest_human_sensor_0000000000000002/attrs', ... (79 bytes))
        2018-08-08T19:55:35.1533725735+0900|arrival|2018-08-08T19:55:35.1533725735+0900
        Client mosqsub|86059-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/dest_led/dest_led_0000000000000002/cmd', ... (36 bytes))
        dest_led_0000000000000002@action|off
        Client mosqsub|86059-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000002/cmd', ... (65 bytes))
        guide_robot_0000000000000002@robot_request|r_cmd|Navi|x|0.0|y|0.0
        Client mosqsub|86059-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000002/cmdexe', ... (105 bytes))
        guide_robot_0000000000000002@robot_request|result,success/time,2018-08-08 19:55:36/r_cmd,Navi/x,0.0/y,0.0
        ```
    * send ros message to ros topic `/robot_2f_1/request` automatically

        ```bash
        root@rosbridge:/opt/ros_ws# rostopic echo /robot_2f_1/request
        time: "2018-08-08 19:55:36"
        r_cmd: "Navi"
        pos:
          x: 0.0
          y: 0.0
        ---
        ```
    * update `r_state` to `Returning` automatically

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000002/attrs/r_state/ | jq .
        {
          "type": "string",
          "value": "Returning",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-08T19:55:35.996884+0900"
            }
          }
        }
        ```
    * reset `visitor` automatically

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000002/attrs/visitor/ | jq .
        {
          "type": "string",
          "value": "",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-08T19:55:35.942273+0900"
            }
          }
        }
        ```
    * record ledger automatically

        ```bash
        mac:$ kubectl exec mongodb-0 -c mongodb -- mongo ledger --eval 'db.visitors.find().sort({"receptionDatetime":-1}).limit(1).pretty()'
        MongoDB shell version v3.6.5
        connecting to: mongodb://127.0.0.1:27017/ledger
        MongoDB server version: 3.6.5
        {
          "_id" : ObjectId("5b6ac98b393f5f00136ecea3"),
          "status" : "arrival",
          "face" : "/shared/faces/tZGqEzEEvuc8jhw0.JPEG",
          "faceIds" : [
            "a74b8913-ccf7-44b9-af17-953ddd1bedae",
            "991e9292-5e75-4fa7-b0be-67e001007cef"
          ],
          "dest" : {
            "dest_human_sensor_id" : "dest_human_sensor_0000000000000002",
            "dest_led_id" : "dest_led_0000000000000002",
            "dest_led_pos_x" : 19,
            "dest_led_pos_y" : 19,
            "dest_pos_x" : 20,
            "dest_pos_y" : 20,
            "floor" : 2,
            "id" : "5b63d672f6f8a80013b85abf",
            "name" : "203号室"
          },
          "receptionDatetime" : ISODate("2018-08-08T10:44:26.530Z"),
          "arrivalDatetime" : ISODate("2018-08-08T10:55:35.934Z")
        }
        ```
1. simulate to send `action` cmd result

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /dest_led/dest_led_0000000000000002/cmdexe -u iotagent -P XXXXXXXX -m "dest_led_0000000000000002@action|success"
    Client mosqpub|22763-Nobuyukin sending CONNECT
    Client mosqpub|22763-Nobuyukin received CONNACK
    Client mosqpub|22763-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/dest_led/dest_led_0000000000000002/cmdexe', ... (40 bytes))
    Client mosqpub|22763-Nobuyukin sending DISCONNECT
    ```
1. simulate to receive robot state (Navi)
    * publish ros message to `/robot_2f_1/state` near the dest position

    ```bash
    root@rosbridge:/opt/ros_ws# rostopic pub -1 /robot_2f_1/state office_guide_robot/r_state "
    time: '2018-10-09 08:07:26'
    r_mode: 'Navi'
    pos:
      x: 19.99
      y: 20
      theta: 2.5
    "
    ```
    * receive MQTT message, but no action occured

        ```bash
        Client mosqsub|86059-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000002/attrs', ... (96 bytes))
        2018-08-08T19:58:06.833283+0900|time|2018-10-09 08:07:26|r_mode|Navi|x|19.99|y|20.0|theta|2.5
        ```
    * publish ros message to `/robot_2f_1/state` near the `dest_led_pos`

        ```bash
        root@rosbridge:/opt/ros_ws# rostopic pub -1 /robot_2f_1/state office_guide_robot/r_state "
        time: '2018-10-09 08:07:28'
        r_mode: 'Navi'
        pos:
          x: 19.05
          y: 18.98
          theta: 4.35
        "
        ```
    * receive MQTT message but no action occured

        ```bash
        Client mosqsub|86059-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000002/attrs', ... (95 bytes))
        2018-08-08T19:58:38.153901+0900|time|2018-10-09 08:07:28|r_mode|Navi|x|19.05|y|18.98|theta|4.35
        ```
1. simulate to receive robot state (Standby)
    * publish ros message to `/robot_2f_1/state`

    ```bash
    root@rosbridge:/opt/ros_ws# rostopic pub -1 /robot_2f_1/state office_guide_robot/r_state "
    time: '2018-10-09 08:07:35'
    r_mode: 'Standby'
    pos:
      x: 0.0
      y: 0.0
      theta: 0.0
    "
    ```
    * receive MQTT message, but don't send `action|on` message to `dest_led` authomatically

        ```bash
        Client mosqsub|86059-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000002/attrs', ... (93 bytes))
        2018-08-08T19:59:04.933828+0900|time|2018-10-09 08:07:35|r_mode|Standby|x|0.0|y|0.0|theta|0.0
        ```
    * update `r_state` to `Waiting` automatically

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000002/attrs/r_state/ | jq .
        {
          "type": "string",
          "value": "Waiting",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-08T19:58:06.956661+0900"
            }
          }
        }
        ```

## guidance (floor 3)
1. simulate to finish reception (floor 3)

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000001/attrs -u iotagent -P XXXXXXXX -m "$d|face|null|dest|ProjectRoom 1"
    Client mosqpub|38060-Nobuyukin sending CONNECT
    Client mosqpub|38060-Nobuyukin received CONNACK
    Client mosqpub|38060-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/attrs', ... (95 bytes))
    Client mosqpub|38060-Nobuyukin sending DISCONNECT
    ```
    * send `handover` command to `pepper(floor 1)` automatically

        ```bash
        Client mosqsub|86059-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/attrs', ... (64 bytes))
        2018-08-08T20:00:30.1533726030+0900|face|null|dest|ProjectRoom 1
        Client mosqsub|86059-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/cmd', ... (34 bytes))
        pepper_0000000000000001@handover|3
        ```
    * requres slack module

        ```bash
        reception-7895487b-98m2c reception 2018/08/08 11:00:30 [   INFO] src.slack - 来客がいらっしゃいました。ProjectRoom 1までご案内いたしております
        ```
    * `r_state` of guide robots does not change

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000001/attrs/r_state/ | jq .
        {
          "type": "string",
          "value": "Waiting",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-08T19:35:42.601126+0900"
            }
          }
        }
        ```
        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000002/attrs/r_state/ | jq .
        {
          "type": "string",
          "value": "Waiting",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-08T19:58:06.956661+0900"
            }
          }
        }
        ```
    * record ledger automatically

        ```bash
        mac:$ kubectl exec mongodb-0 -c mongodb -- mongo ledger --eval 'db.visitors.find().sort({"receptionDatetime":-1}).limit(1).pretty()'
        MongoDB shell version v3.6.5
        connecting to: mongodb://127.0.0.1:27017/ledger
        MongoDB server version: 3.6.5
        {
          "_id" : ObjectId("5b6acd4e6a77d600136cbcba"),
          "status" : "reception",
          "face" : null,
          "faceIds" : [ ],
          "dest" : {
            "dest_human_sensor_id" : null,
            "dest_led_id" : null,
            "dest_led_pos_x" : null,
            "dest_led_pos_y" : null,
            "dest_pos_x" : null,
            "dest_pos_y" : null,
            "floor" : 3,
            "id" : "5b63d67c7597100013d0b2ab",
            "name" : "ProjectRoom 1",
            "slack_webhook" : "https://hooks.slack.com/services/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
          },
          "receptionDatetime" : ISODate("2018-08-08T11:00:30.595Z")
        }
        ```
1. simulate to send `welcome` cmd result from `pepper(floor 1)`

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000001/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000001@welcome|success"
    Client mosqpub|22365-Nobuyukin sending CONNECT
    Client mosqpub|22365-Nobuyukin received CONNACK
    Client mosqpub|22365-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/cmdexe', ... (39 bytes))
    Client mosqpub|22365-Nobuyukin sending DISCONNECT
    ```
1. simulate to send `handover` cmd result from `pepper(floor 1)`

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000001/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000001@handover|success"
    Client mosqpub|22763-Nobuyukin sending CONNECT
    Client mosqpub|22763-Nobuyukin received CONNACK
    Client mosqpub|22763-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/cmdexe', ... (40 bytes))
    Client mosqpub|22763-Nobuyukin sending DISCONNECT
    ```

## request to external camera
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
        Client mosqsub|17444-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/external_camera/external_camera_0000000000000011/cmd', ... (70 bytes))
        external_camera_0000000000000011@external_camera_request|c_cmd|Monitor
        Client mosqsub|17444-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/external_camera/external_camera_0000000000000011/cmdexe', ... (110 bytes))
        external_camera_0000000000000011@external_camera_request|result,success/time,2018-08-03 14:32:00/c_cmd,Monitor
        ```
    * send ros message to ros topic `/external_camera_1f_1/request` automatically

        ```bash
        root@rosbridge:/opt/ros_ws# rostopic type /external_camera_1f_1/request
        external_camera/c_req
        ```
        ```bash
        root@rosbridge:/opt/ros_ws# rostopic echo /external_camera_1f_1/request
        time: "2018-08-03 14:32:00"
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
        Client mosqsub|17444-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/external_camera/external_camera_0000000000000012/cmd', ... (70 bytes))
        external_camera_0000000000000012@external_camera_request|c_cmd|Standby
        Client mosqsub|17444-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/external_camera/external_camera_0000000000000012/cmdexe', ... (110 bytes))
        external_camera_0000000000000012@external_camera_request|result,success/time,2018-08-03 14:32:50/c_cmd,Standby
        ```
    * send ros message to ros topic `/external_camera_1f_2/request` automatically

        ```bash
        root@rosbridge:/opt/ros_ws# rostopic type /external_camera_1f_2/request
        external_camera/c_req
        ```
        ```bash
        root@rosbridge:/opt/ros_ws# rostopic echo /external_camera_1f_2/request
        time: "2018-08-03 14:32:50"
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
        Client mosqsub|17444-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/external_camera/external_camera_0000000000000021/cmd', ... (70 bytes))
        external_camera_0000000000000021@external_camera_request|c_cmd|Monitor
        Client mosqsub|17444-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/external_camera/external_camera_0000000000000021/cmdexe', ... (110 bytes))
        external_camera_0000000000000021@external_camera_request|result,success/time,2018-08-03 14:33:34/c_cmd,Monitor
        ```
    * send ros message to ros topic `/external_camera_2f_1/request` automatically

        ```bash
        root@rosbridge:/opt/ros_ws# rostopic type /external_camera_2f_1/request
        external_camera/c_req
        ```
        ```bash
        root@rosbridge:/opt/ros_ws# rostopic echo /external_camera_2f_1/request
        time: "2018-08-03 14:33:34"
        c_cmd: "Monitor"
        ---
        ```

## state of external camera
1. simulate to receive the state of external camera 1F-1
    * publish ros message to `/external_camera_1f_1/state`

    ```bash
    root@rosbridge:/opt/ros_ws# rostopic pub -1 /external_camera_1f_1/state external_camera/c_state "
    time: '2018-02-03 04:05:06'
    c_mode: 'Monitor'
    num_p: 0
    "
    ```
    * recieve MQTT message

        ```bash
        Client mosqsub|17444-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/external_camera/external_camera_0000000000000011/attrs', ... (90 bytes))
        2018-08-03T14:34:15.745794+0900|time|2018-02-03 04:05:06|c_mode|Monitor|num_p|0|position|-
        ```
    * confirm mogodb records registered within a minunte

        ```bash
        mac:$ kubectl exec mongodb-0 -c mongodb -- mongo sth_camera --eval 'db.getCollection("sth_/_external_camera_0000000000000011_external_camera").find({recvTime: { "$gte": new Date(ISODate().getTime() - 1000 * 60 * 1)}})'
        MongoDB shell version v3.6.5
        connecting to: mongodb://127.0.0.1:27017/sth_camera
        MongoDB server version: 3.6.5
        { "_id" : ObjectId("5b63e95723b570000ae5452c"), "recvTime" : ISODate("2018-08-03T05:34:15.846Z"), "attrName" : "c_mode", "attrType" : "string", "attrValue" : "Monitor" }
        { "_id" : ObjectId("5b63e95723b570000ae5452f"), "recvTime" : ISODate("2018-08-03T05:34:15.846Z"), "attrName" : "num_p", "attrType" : "int", "attrValue" : "0" }
        { "_id" : ObjectId("5b63e95723b570000ae54530"), "recvTime" : ISODate("2018-08-03T05:34:15.846Z"), "attrName" : "position", "attrType" : "string", "attrValue" : "-" }
        { "_id" : ObjectId("5b63e95723b570000ae54531"), "recvTime" : ISODate("2018-08-03T05:34:15.846Z"), "attrName" : "time", "attrType" : "string", "attrValue" : "2018-02-03 04:05:06" }
        ```
1. simulate to receive the state of external camera 1F-2
    * publish ros message to `/external_camera_1f_2/state`

    ```bash
    root@rosbridge:/opt/ros_ws# rostopic pub -1 /external_camera_1f_2/state external_camera/c_state "
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
        Client mosqsub|17444-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/external_camera/external_camera_0000000000000012/attrs', ... (106 bytes))
        2018-08-03T14:35:21.728598+0900|time|2018-02-03 04:15:16|c_mode|Standby|num_p|1|position|x[0],1.0/y[0],1.1
        ```
    * confirm mogodb records registered within a minunte

        ```bash
        mac:$ kubectl exec mongodb-0 -c mongodb -- mongo sth_camera --eval 'db.getCollection("sth_/_external_camera_0000000000000012_external_camera").find({recvTime: { "$gte": new Date(ISODate().getTime() - 1000 * 60 * 1)}})'
        MongoDB shell version v3.6.5
        connecting to: mongodb://127.0.0.1:27017/sth_camera
        MongoDB server version: 3.6.5
        { "_id" : ObjectId("5b63e99923b570000ae54532"), "recvTime" : ISODate("2018-08-03T05:35:21.805Z"), "attrName" : "c_mode", "attrType" : "string", "attrValue" : "Standby" }
        { "_id" : ObjectId("5b63e99923b570000ae54535"), "recvTime" : ISODate("2018-08-03T05:35:21.805Z"), "attrName" : "num_p", "attrType" : "int", "attrValue" : "1" }
        { "_id" : ObjectId("5b63e99923b570000ae54536"), "recvTime" : ISODate("2018-08-03T05:35:21.805Z"), "attrName" : "position", "attrType" : "string", "attrValue" : "x[0],1.0/y[0],1.1" }
        { "_id" : ObjectId("5b63e99923b570000ae54537"), "recvTime" : ISODate("2018-08-03T05:35:21.805Z"), "attrName" : "time", "attrType" : "string", "attrValue" : "2018-02-03 04:15:16" }
        ```
1. simulate to receive the state of external camera 2F-1
    * publish ros message to `/external_camera_2f_1/state`

    ```bash
    root@rosbridge:/opt/ros_ws# rostopic pub -1 /external_camera_2f_1/state external_camera/c_state "
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
        Client mosqsub|17444-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/external_camera/external_camera_0000000000000021/attrs', ... (122 bytes))
        2018-08-03T14:36:48.812620+0900|time|2018-02-03 04:25:26|c_mode|Error|num_p|2|position|x[0],1.0/y[0],1.1/x[1],2.0/y[1],2.1
        ```
    * confirm mogodb records registered within a minunte

        ```bash
        mac:$ kubectl exec mongodb-0 -c mongodb -- mongo sth_camera --eval 'db.getCollection("sth_/_external_camera_0000000000000021_external_camera").find({recvTime: { "$gte": new Date(ISODate().getTime() - 1000 * 60 * 1)}})'
        MongoDB shell version v3.6.5
        connecting to: mongodb://127.0.0.1:27017/sth_camera
        MongoDB server version: 3.6.5
        { "_id" : ObjectId("5b63e9f2f8a94e000a6eb160"), "recvTime" : ISODate("2018-08-03T05:36:48.863Z"), "attrName" : "c_mode", "attrType" : "string", "attrValue" : "Error" }
        { "_id" : ObjectId("5b63e9f2f8a94e000a6eb163"), "recvTime" : ISODate("2018-08-03T05:36:48.863Z"), "attrName" : "num_p", "attrType" : "int", "attrValue" : "2" }
        { "_id" : ObjectId("5b63e9f2f8a94e000a6eb164"), "recvTime" : ISODate("2018-08-03T05:36:48.863Z"), "attrName" : "position", "attrType" : "string", "attrValue" : "x[0],1.0/y[0],1.1/x[1],2.0/y[1],2.1" }
        { "_id" : ObjectId("5b63e9f2f8a94e000a6eb165"), "recvTime" : ISODate("2018-08-03T05:36:48.863Z"), "attrName" : "time", "attrType" : "string", "attrValue" : "2018-02-03 04:25:26" }
        ```

## face verify failure: initialize robot
1. set `r_state` of guide robot as `Waiting`
    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v1/updateContext -d @-<<__EOS__ | jq .
    {
      "contextElements": [
        {
          "id": "guide_robot_0000000000000002",
          "isPattern": "false",
          "type": "guide_robot",
          "attributes": [
            {
              "name": "r_state",
              "value": "Waiting",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }, {
              "name": "destx",
              "value": "",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }, {
              "name": "desty",
              "value": "",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }, {
              "name": "visitor",
              "value": "",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }
          ]
        }
      ],
      "updateAction": "UPDATE"
    }
    __EOS__
    ```

## face verify failure: guidance (floor 2)
1. simulate to be called `/storage/faces/` REST API by pepper(floor 1)

    ```bash
    mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);export FACEPATH=$(curl -sS -H "Authorization: bearer ${TOKEN}" -H "Content-Type: multipart/form-data" https://api.tech-sketch.jp/storage/faces/ -X POST -F face=@face.jpg | jq .path -r);echo ${FACEPATH}
    /shared/faces/AmYx4FqPsiSTi7s5.JPEG
    ```
1. simulate to finish reception (floor 2)

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000001/attrs -u iotagent -P XXXXXXXX -m "$d|face|${FACEPATH}|dest|203号室"
    Client mosqpub|37447-Nobuyukin sending CONNECT
    Client mosqpub|37447-Nobuyukin received CONNACK
    Client mosqpub|37447-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/attrs', ... (91 bytes))
    Client mosqpub|37447-Nobuyukin sending DISCONNECT
    ```
    * send `handover` command to `pepper(floor 1)` and `facedetect` command to `pepper(floor 2)` automatically

        ```bash
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/attrs', ... (91 bytes))
        2018-08-09T15:11:34.1533795094+0900|face|/shared/faces/AmYx4FqPsiSTi7s5.JPEG|dest|203号室
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000002/cmd', ... (40 bytes))
        pepper_0000000000000002@facedetect|start
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/cmd', ... (34 bytes))
        pepper_0000000000000001@handover|2
        ```
    * record ledger automatically

        ```bash
        mac:$ kubectl exec mongodb-0 -c mongodb -- mongo ledger --eval 'db.visitors.find().sort({"receptionDatetime":-1}).limit(1).pretty()'
        MongoDB shell version v3.6.5
        connecting to: mongodb://127.0.0.1:27017/ledger
        MongoDB server version: 3.6.5
        {
          "_id" : ObjectId("5b6bdb16b7326200135945d2"),
          "status" : "reception",
          "face" : "/shared/faces/AmYx4FqPsiSTi7s5.JPEG",
          "faceIds" : [
            "0225ca9f-91d5-4c23-898d-465dede3faaf"
          ],
          "dest" : {
            "dest_human_sensor_id" : "dest_human_sensor_0000000000000002",
            "dest_led_id" : "dest_led_0000000000000002",
            "dest_led_pos_x" : 19,
            "dest_led_pos_y" : 19,
            "dest_pos_x" : 20,
            "dest_pos_y" : 20,
            "floor" : 2,
            "id" : "5b63d672f6f8a80013b85abf",
            "name" : "203号室"
          },
          "receptionDatetime" : ISODate("2018-08-09T06:11:34.338Z")
        }
        ```
1. simulate to send `welcome` cmd result from `pepper(floor 1)`

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000001/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000001@welcome|success"
    Client mosqpub|22365-Nobuyukin sending CONNECT
    Client mosqpub|22365-Nobuyukin received CONNACK
    Client mosqpub|22365-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/cmdexe', ... (39 bytes))
    Client mosqpub|22365-Nobuyukin sending DISCONNECT
    ```
1. simulate to send `handover` cmd result from `pepper(floor 1)`

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000001/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000001@handover|success"
    Client mosqpub|22763-Nobuyukin sending CONNECT
    Client mosqpub|22763-Nobuyukin received CONNACK
    Client mosqpub|22763-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/cmdexe', ... (40 bytes))
    Client mosqpub|22763-Nobuyukin sending DISCONNECT
    ```

## face verify failure: face detection (floor 2)
1. simulate to be called `/storage/faces/` REST API by pepper(floor 2)

    ```bash
    mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);export FACEPATH=$(curl -sS -H "Authorization: bearer ${TOKEN}" -H "Content-Type: multipart/form-data" https://api.tech-sketch.jp/storage/faces/ -X POST -F face=@other_persons_face.jpg | jq .path -r);echo ${FACEPATH}
    /shared/faces/Gx45wxQtb07V0IBc.JPEG
    ```
1. simulate to detect visitor

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000002/attrs -u iotagent -P XXXXXXXX -m "$d|face|${FACEPATH}"
    Client mosqpub|97057-Nobuyukin sending CONNECT
    Client mosqpub|97057-Nobuyukin received CONNACK
    Client mosqpub|97057-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000002/attrs', ... (76 bytes))
    Client mosqpub|97057-Nobuyukin sending DISCONNECT
    ```
    * send `reask` command to `pepper(floor 2)`

        ```bash
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000002/attrs', ... (76 bytes))
        2018-08-09T15:14:50.1533795290+0900|face|/shared/faces/Gx45wxQtb07V0IBc.JPEG
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000002/cmd', ... (34 bytes))
        pepper_0000000000000002@reask|true
        ```
    * do not send ros message to ros topic `/robot_2f_1/request`
    * do not update `r_state` to `Guiding`

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000002/attrs/r_state/ | jq .
        {
          "type": "string",
          "value": "Waiting",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-09T15:10:27.1533795027+0900"
            }
          }
        }
        ```
    * do not set `visitor`

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000002/attrs/visitor/ | jq .
        {
          "type": "string",
          "value": "",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-09T15:10:27.1533795027+0900"
            }
          }
        }
        ```
1. simulate to send `facedetect` cmd result from `pepper(floor 2)`

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000002/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000002@facedetect|success"
    Client mosqpub|48535-Nobuyukin sending CONNECT
    Client mosqpub|48535-Nobuyukin received CONNACK
    Client mosqpub|48535-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000002/cmdexe', ... (42 bytes))
    Client mosqpub|48535-Nobuyukin sending DISCONNECT
    ```

## face verify failure: reask destination (floor 2)
1. simlate to be called `/destinations/?filter=floor|2` REST API by `pepper (floor 2)`

    ```bash
    mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" https://api.tech-sketch.jp/destinations/ -G --data-urlencode filter="floor|2" | jq .
    [
      {
        "dest_human_sensor_id": "dest_human_sensor_0000000000000002",
        "dest_led_id": "dest_led_0000000000000002",
        "dest_led_pos_x": 19,
        "dest_led_pos_y": 19,
        "dest_pos_x": 20,
        "dest_pos_y": 20,
        "floor": 2,
        "id": "5b63d672f6f8a80013b85abf",
        "name": "203号室"
      },
      {
        "dest_human_sensor_id": "dest_human_sensor_0000000000000003",
        "dest_led_id": "dest_led_0000000000000003",
        "dest_led_pos_x": 19,
        "dest_led_pos_y": -19,
        "dest_pos_x": 20,
        "dest_pos_y": -10,
        "floor": 2,
        "id": "5b63d6787597100013d0b2a9",
        "name": "204号室"
      }
    ]
    ```
1. simulate to finish reasking destination

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000002/attrs -u iotagent -P XXXXXXXX -m "$d|dest|203号室"
    Client mosqpub|21252-Nobuyukin sending CONNECT
    Client mosqpub|21252-Nobuyukin received CONNACK
    Client mosqpub|21252-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000002/attrs', ... (50 bytes))
    Client mosqpub|21252-Nobuyukin sending DISCONNECT
    ```
    * send `handover` command to `pepper(floor 2)` and `robot_request` command to `guide_robot` automatically

        ```bash
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000002/attrs', ... (50 bytes))
        2018-08-09T15:16:38.1533795398+0900|dest|203号室
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000002/cmd', ... (41 bytes))
        pepper_0000000000000002@handover|continue
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000002/cmd', ... (67 bytes))
        guide_robot_0000000000000002@robot_request|r_cmd|Navi|x|20.0|y|20.0
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000002/cmdexe', ... (107 bytes))
        guide_robot_0000000000000002@robot_request|result,success/time,2018-08-09 15:16:39/r_cmd,Navi/x,20.0/y,20.0
        ```
    * send ros message to ros topic `/robot_2f_1/request` automatically

        ```bash
        root@rosbridge:/opt/ros_ws# rostopic echo /robot_2f_1/request
        time: "2018-08-09 15:16:39"
        r_cmd: "Navi"
        pos:
          x: 20.0
          y: 20.0
        ---
        ```
    * update `r_state` to `Guiding` automatically

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000002/attrs/r_state/ | jq .
        {
          "type": "string",
          "value": "Guiding",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-09T15:16:39.128319+0900"
            }
          }
        }
        ```
    * set `visitor` automatically

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000002/attrs/visitor/ | jq .
        {
          "type": "string",
          "value": "5b6bdc472cc3eb0013ab7838",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-09T15:16:39.128319+0900"
            }
          }
        }
        ```
    * record ledger automatically

        ```bash
        mac:$ kubectl exec mongodb-0 -c mongodb -- mongo ledger --eval 'db.visitors.find().sort({"reaskDatetime":-1}).limit(1).pretty()'
        MongoDB shell version v3.6.5
        connecting to: mongodb://127.0.0.1:27017/ledger
        MongoDB server version: 3.6.5
        {
          "_id" : ObjectId("5b6bdc472cc3eb0013ab7838"),
          "status" : "reask",
          "face" : null,
          "faceIds" : [ ],
          "dest" : {
            "dest_human_sensor_id" : "dest_human_sensor_0000000000000002",
            "dest_led_id" : "dest_led_0000000000000002",
            "dest_led_pos_x" : 19,
            "dest_led_pos_y" : 19,
            "dest_pos_x" : 20,
            "dest_pos_y" : 20,
            "floor" : 2,
            "id" : "5b63d672f6f8a80013b85abf",
            "name" : "203号室"
          },
          "reaskDatetime" : ISODate("2018-08-09T06:16:39.063Z")
        }
        ```
1. simulate to send `reask` cmd result from `pepper(floor 2)`

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000002/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000002@reask|success"
    Client mosqpub|21833-Nobuyukin sending CONNECT
    Client mosqpub|21833-Nobuyukin received CONNACK
    Client mosqpub|21833-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000002/cmdexe', ... (37 bytes))
    Client mosqpub|21833-Nobuyukin sending DISCONNECT
    ```
1. simulate to send `handover` cmd result from `pepper(floor 2)`

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000002/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000002@handover|success"
    Client mosqpub|48779-Nobuyukin sending CONNECT
    Client mosqpub|48779-Nobuyukin received CONNACK
    Client mosqpub|48779-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000002/cmdexe', ... (40 bytes))
    Client mosqpub|48779-Nobuyukin sending DISCONNECT
    ```

## face verify failure: clean robot
1. set `r_state` of guide robot as `Waiting`
    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v1/updateContext -d @-<<__EOS__ | jq .
    {
      "contextElements": [
        {
          "id": "guide_robot_0000000000000002",
          "isPattern": "false",
          "type": "guide_robot",
          "attributes": [
            {
              "name": "r_state",
              "value": "Waiting",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }, {
              "name": "destx",
              "value": "",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }, {
              "name": "desty",
              "value": "",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }, {
              "name": "visitor",
              "value": "",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }
          ]
        }
      ],
      "updateAction": "UPDATE"
    }
    __EOS__
    ```

## robot busy (floor 1): initialize robot
1. set `r_state` of guide robot as `Waiting`

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v1/updateContext -d @-<<__EOS__ | jq .
    {
      "contextElements": [
        {
          "id": "guide_robot_0000000000000001",
          "isPattern": "false",
          "type": "guide_robot",
          "attributes": [
            {
              "name": "r_state",
              "value": "Waiting",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }, {
              "name": "destx",
              "value": "",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }, {
              "name": "desty",
              "value": "",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }, {
              "name": "visitor",
              "value": "",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }
          ]
        }
      ],
      "updateAction": "UPDATE"
    }
    __EOS__
    ```

## robot busy (floor 1): guidance a visitor
1. simulate to finish reception (floor 1)

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000001/attrs -u iotagent -P XXXXXXXX -m "$d|face|null|dest|管理センター"
    Client mosqpub|37117-Nobuyukin sending CONNECT
    Client mosqpub|37117-Nobuyukin received CONNACK
    Client mosqpub|37117-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/attrs', ... (100 bytes))
    Client mosqpub|37117-Nobuyukin sending DISCONNECT
    ```
    * send `handover` command to `pepper(floor 1)` and `robot_request` command to `guide_robot` automatically

        ```bash
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/attrs', ... (69 bytes))
        2018-08-09T17:36:39.1533803799+0900|face|null|dest|管理センター
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/cmd', ... (34 bytes))
        pepper_0000000000000001@handover|1
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000001/cmd', ... (68 bytes))
        guide_robot_0000000000000001@robot_request|r_cmd|Navi|x|-10.0|y|10.0
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000001/cmdexe', ... (108 bytes))
        guide_robot_0000000000000001@robot_request|result,success/time,2018-08-09 17:36:40/r_cmd,Navi/x,-10.0/y,10.0
        ```
    * update `r_state` to `Guiding` automatically

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000001/attrs/r_state/ | jq .
        {
          "type": "string",
          "value": "Guiding",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-09T17:36:39.984954+0900"
            }
          }
        }
        ```
    * set `visitor` automatically

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000001/attrs/visitor/ | jq .
        {
          "type": "string",
          "value": "5b6bfd1733d92500132faa80",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-09T17:36:39.984954+0900"
            }
          }
        }
        ```
    * record ledger automatically

        ```bash
        mac:$ kubectl exec mongodb-0 -c mongodb -- mongo ledger --eval 'db.visitors.find().sort({"receptionDatetime":-1}).limit(1).pretty()'
        MongoDB shell version v3.6.5
        connecting to: mongodb://127.0.0.1:27017/ledger
        MongoDB server version: 3.6.5
        {
          "_id" : ObjectId("5b6bfd1733d92500132faa80"),
          "status" : "reception",
          "face" : null,
          "faceIds" : [ ],
          "dest" : {
            "dest_human_sensor_id" : "dest_human_sensor_0000000000000001",
            "dest_led_id" : "dest_led_0000000000000001",
            "dest_led_pos_x" : -9,
            "dest_led_pos_y" : 9,
            "dest_pos_x" : -10,
            "dest_pos_y" : 10,
            "floor" : 1,
            "id" : "5b63d66d7597100013d0b2a7",
            "name" : "管理センター"
          },
          "receptionDatetime" : ISODate("2018-08-09T08:36:39.864Z")
        }
        ```
1. simulate to send `welcome` cmd result from `pepper(floor 1)`

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000001/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000001@welcome|success"
    Client mosqpub|22365-Nobuyukin sending CONNECT
    Client mosqpub|22365-Nobuyukin received CONNACK
    Client mosqpub|22365-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/cmdexe', ... (39 bytes))
    Client mosqpub|22365-Nobuyukin sending DISCONNECT
    ```
1. simulate to send `handover` cmd result from `pepper(floor 1)`

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000001/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000001@handover|success"
    Client mosqpub|22763-Nobuyukin sending CONNECT
    Client mosqpub|22763-Nobuyukin received CONNACK
    Client mosqpub|22763-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/cmdexe', ... (40 bytes))
    Client mosqpub|22763-Nobuyukin sending DISCONNECT
    ```

## robot busy (floor 1): guidance another visitor while guiding previous visitor
1. simulate to finish reception (floor 1)

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000001/attrs -u iotagent -P XXXXXXXX -m "$d|face|null|dest|管理センター"
    Client mosqpub|37117-Nobuyukin sending CONNECT
    Client mosqpub|37117-Nobuyukin received CONNACK
    Client mosqpub|37117-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/attrs', ... (100 bytes))
    Client mosqpub|37117-Nobuyukin sending DISCONNECT
    ```
    * send `handover|busy` command to `pepper(floor 1)` and do not send `robot_request` command

        ```bash
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/attrs', ... (69 bytes))
        2018-08-09T17:41:06.1533804066+0900|face|null|dest|管理センター
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/cmd', ... (37 bytes))
        pepper_0000000000000001@handover|busy
        ```
    * do not send ros message to ros topic `/robot_1f_1/request`
    * do not update `r_state`

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000001/attrs/r_state/ | jq .
        {
          "type": "string",
          "value": "Guiding",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-09T17:36:39.984954+0900"
            }
          }
        }
        ```
    * do not update `visitor`

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000001/attrs/visitor/ | jq .
        {
          "type": "string",
          "value": "5b6bfd1733d92500132faa80",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-09T17:36:39.984954+0900"
            }
          }
        }
        ```
    * record ledger automatically as busy state

        ```bash
        mac:$ kubectl exec mongodb-0 -c mongodb -- mongo ledger --eval 'db.visitors.find().sort({"receptionDatetime":-1}).limit(2).pretty()'
        MongoDB shell version v3.6.5
        connecting to: mongodb://127.0.0.1:27017/ledger
        MongoDB server version: 3.6.5
        {
          "_id" : ObjectId("5b6bfe2355d7fb0013c57183"),
          "status" : "busy",
          "face" : null,
          "faceIds" : [ ],
          "dest" : {
            "dest_human_sensor_id" : "dest_human_sensor_0000000000000001",
            "dest_led_id" : "dest_led_0000000000000001",
            "dest_led_pos_x" : -9,
            "dest_led_pos_y" : 9,
            "dest_pos_x" : -10,
            "dest_pos_y" : 10,
            "floor" : 1,
            "id" : "5b63d66d7597100013d0b2a7",
            "name" : "管理センター"
          },
          "receptionDatetime" : ISODate("2018-08-09T08:41:07.169Z"),
          "busyDatetime" : ISODate("2018-08-09T08:41:07.243Z")
        }
        {
          "_id" : ObjectId("5b6bfd1733d92500132faa80"),
          "status" : "reception",
          "face" : null,
          "faceIds" : [ ],
          "dest" : {
            "dest_human_sensor_id" : "dest_human_sensor_0000000000000001",
            "dest_led_id" : "dest_led_0000000000000001",
            "dest_led_pos_x" : -9,
            "dest_led_pos_y" : 9,
            "dest_pos_x" : -10,
            "dest_pos_y" : 10,
            "floor" : 1,
            "id" : "5b63d66d7597100013d0b2a7",
            "name" : "管理センター"
          },
          "receptionDatetime" : ISODate("2018-08-09T08:36:39.864Z")
        }
        ```

## robot busy (floor 1): arrival previous visitor
1. simulate to receive robot state (Standby)
    * publish ros message to `/robot_1f_1/state`

    ```bash
    root@rosbridge:/opt/ros_ws# rostopic pub -1 /robot_1f_1/state office_guide_robot/r_state "
    time: '2018-09-08 07:06:15'
    r_mode: 'Standby'
    pos:
      x: -10.01
      y: 10.02
      theta: 9.1
    "
    ```
    * update `r_state` to `Suspending` automatically

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000001/attrs/r_state/ | jq .
        {
          "type": "string",
          "value": "Suspending",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-09T17:47:42.636688+0900"
            }
          }
        }
        ```
1. simuate visitor arriving at the destination

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /dest_human_sensor/dest_human_sensor_0000000000000001/attrs -u iotagent -P XXXXXXXX -m "$d|arrival|$d"
    Client mosqpub|65572-Nobuyukin sending CONNECT
    Client mosqpub|65572-Nobuyukin received CONNACK
    Client mosqpub|65572-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/dest_human_sensor/dest_human_sensor_0000000000000001/attrs', ... (79 bytes))
    Client mosqpub|65572-Nobuyukin sending DISCONNECT
    ```
    * receive MQTT message and send `action|off` message to `dest_led_0000000000000001` and `robot_request` command to `guide_robot_0000000000000001` automatically

        ```bash
        mac:Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/dest_human_sensor/dest_human_sensor_0000000000000001/attrs', ... (79 bytes))
        2018-08-09T17:48:55.1533804535+0900|arrival|2018-08-09T17:48:55.1533804535+0900
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/dest_led/dest_led_0000000000000001/cmd', ... (36 bytes))
        dest_led_0000000000000001@action|off
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000001/cmd', ... (65 bytes))
        guide_robot_0000000000000001@robot_request|r_cmd|Navi|x|0.0|y|0.0
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000001/cmdexe', ... (105 bytes))
        guide_robot_0000000000000001@robot_request|result,success/time,2018-08-09 17:48:56/r_cmd,Navi/x,0.0/y,0.0
        ```
    * send ros message to ros topic `/robot_1f_1/request` automatically

        ```bash
        root@rosbridge:/opt/ros_ws# rostopic echo /robot_1f_1/request
        time: "2018-08-09 17:48:56"
        r_cmd: "Navi"
        pos:
          x: 0.0
          y: 0.0
        ---
        ```
    * update `r_state` to `Returning` automatically

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000001/attrs/r_state/ | jq .
        {
          "type": "string",
          "value": "Returning",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-09T17:48:56.292958+0900"
            }
          }
        }
        ```
    * record ledger automatically

        ```bash
        mac:$ kubectl exec mongodb-0 -c mongodb -- mongo ledger --eval 'db.visitors.find().sort({"receptionDatetime":-1}).limit(2).pretty()'
        MongoDB shell version v3.6.5
        connecting to: mongodb://127.0.0.1:27017/ledger
        MongoDB server version: 3.6.5
        {
          "_id" : ObjectId("5b6bfe2355d7fb0013c57183"),
          "status" : "busy",
          "face" : null,
          "faceIds" : [ ],
          "dest" : {
            "dest_human_sensor_id" : "dest_human_sensor_0000000000000001",
            "dest_led_id" : "dest_led_0000000000000001",
            "dest_led_pos_x" : -9,
            "dest_led_pos_y" : 9,
            "dest_pos_x" : -10,
            "dest_pos_y" : 10,
            "floor" : 1,
            "id" : "5b63d66d7597100013d0b2a7",
            "name" : "管理センター"
          },
          "receptionDatetime" : ISODate("2018-08-09T08:41:07.169Z"),
          "busyDatetime" : ISODate("2018-08-09T08:41:07.243Z")
        }
        {
          "_id" : ObjectId("5b6bfd1733d92500132faa80"),
          "status" : "arrival",
          "face" : null,
          "faceIds" : [ ],
          "dest" : {
            "dest_human_sensor_id" : "dest_human_sensor_0000000000000001",
            "dest_led_id" : "dest_led_0000000000000001",
            "dest_led_pos_x" : -9,
            "dest_led_pos_y" : 9,
            "dest_pos_x" : -10,
            "dest_pos_y" : 10,
            "floor" : 1,
            "id" : "5b63d66d7597100013d0b2a7",
            "name" : "管理センター"
          },
          "receptionDatetime" : ISODate("2018-08-09T08:36:39.864Z"),
          "arrivalDatetime" : ISODate("2018-08-09T08:48:56.202Z")
        }
        ```

## robot busy (floor 1): clean robot
1. set `r_state` of guide robot as `Waiting`

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v1/updateContext -d @-<<__EOS__ | jq .
    {
      "contextElements": [
        {
          "id": "guide_robot_0000000000000001",
          "isPattern": "false",
          "type": "guide_robot",
          "attributes": [
            {
              "name": "r_state",
              "value": "Waiting",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }, {
              "name": "destx",
              "value": "",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }, {
              "name": "desty",
              "value": "",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }, {
              "name": "visitor",
              "value": "",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }
          ]
        }
      ],
      "updateAction": "UPDATE"
    }
    __EOS__
    ```

## robot busy (floor 2) face detect: initialize robot
1. set `r_state` of guide robot as `Waiting`

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v1/updateContext -d @-<<__EOS__ | jq .
    {
      "contextElements": [
        {
          "id": "guide_robot_0000000000000002",
          "isPattern": "false",
          "type": "guide_robot",
          "attributes": [
            {
              "name": "r_state",
              "value": "Waiting",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }, {
              "name": "destx",
              "value": "",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }, {
              "name": "desty",
              "value": "",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }, {
              "name": "visitor",
              "value": "",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }
          ]
        }
      ],
      "updateAction": "UPDATE"
    }
    __EOS__
    ```

## robot busy (floor 2) face detect: guidance a visitor
1. simulate to be called `/storage/faces/` REST API by pepper(floor 1)

    ```bash
    mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);export FACEPATH=$(curl -sS -H "Authorization: bearer ${TOKEN}" -H "Content-Type: multipart/form-data" https://api.tech-sketch.jp/storage/faces/ -X POST -F face=@face.jpg | jq .path -r);echo ${FACEPATH}
    /shared/faces/5eOMQwLJSuQ0SVHb.JPEG
    ```
1. simulate to finish reception (floor 2)

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000001/attrs -u iotagent -P XXXXXXXX -m "$d|face|${FACEPATH}|dest|203号室"
    Client mosqpub|37447-Nobuyukin sending CONNECT
    Client mosqpub|37447-Nobuyukin received CONNACK
    Client mosqpub|37447-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/attrs', ... (91 bytes))
    Client mosqpub|37447-Nobuyukin sending DISCONNECT
    ```
    * send `handover` command to `pepper(floor 1)` and `facedetect` command to `pepper(floor 2)` automatically

        ```bash
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/attrs', ... (91 bytes))
        2018-08-09T17:57:17.1533805037+0900|face|/shared/faces/5eOMQwLJSuQ0SVHb.JPEG|dest|203号室
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000002/cmd', ... (40 bytes))
        pepper_0000000000000002@facedetect|start
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/cmd', ... (34 bytes))
        pepper_0000000000000001@handover|2
        ```
    * record ledger automatically

        ```bash
        mac:$ kubectl exec mongodb-0 -c mongodb -- mongo ledger --eval 'db.visitors.find().sort({"receptionDatetime":-1}).limit(1).pretty()'
        MongoDB shell version v3.6.5
        connecting to: mongodb://127.0.0.1:27017/ledger
        MongoDB server version: 3.6.5
        {
          "_id" : ObjectId("5b6c01ed55d7fb0013c57185"),
          "status" : "reception",
          "face" : "/shared/faces/5eOMQwLJSuQ0SVHb.JPEG",
          "faceIds" : [
            "4bf9d5b1-08be-46ec-8c0c-e52c09987d81"
          ],
          "dest" : {
            "dest_human_sensor_id" : "dest_human_sensor_0000000000000002",
            "dest_led_id" : "dest_led_0000000000000002",
            "dest_led_pos_x" : 19,
            "dest_led_pos_y" : 19,
            "dest_pos_x" : 20,
            "dest_pos_y" : 20,
            "floor" : 2,
            "id" : "5b63d672f6f8a80013b85abf",
            "name" : "203号室"
          },
          "receptionDatetime" : ISODate("2018-08-09T08:57:17.305Z")
        }
        ```
1. simulate to send `welcome` cmd result from `pepper(floor 1)`

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000001/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000001@welcome|success"
    Client mosqpub|22365-Nobuyukin sending CONNECT
    Client mosqpub|22365-Nobuyukin received CONNACK
    Client mosqpub|22365-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/cmdexe', ... (39 bytes))
    Client mosqpub|22365-Nobuyukin sending DISCONNECT
    ```
1. simulate to send `handover` cmd result from `pepper(floor 1)`

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000001/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000001@handover|success"
    Client mosqpub|22763-Nobuyukin sending CONNECT
    Client mosqpub|22763-Nobuyukin received CONNACK
    Client mosqpub|22763-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/cmdexe', ... (40 bytes))
    Client mosqpub|22763-Nobuyukin sending DISCONNECT
    ```

## robot busy (floor 2) face detect: detect a visitor
1. simulate to be called `/storage/faces/` REST API by pepper(floor 2)

    ```bash
    mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);export FACEPATH=$(curl -sS -H "Authorization: bearer ${TOKEN}" -H "Content-Type: multipart/form-data" https://api.tech-sketch.jp/storage/faces/ -X POST -F face=@another_face.jpg | jq .path -r);echo ${FACEPATH}
    /shared/faces/VNDKcDCEUhFR7P7T.JPEG
    ```
1. simulate to detect visitor

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000002/attrs -u iotagent -P XXXXXXXX -m "$d|face|${FACEPATH}"
    Client mosqpub|97057-Nobuyukin sending CONNECT
    Client mosqpub|97057-Nobuyukin received CONNACK
    Client mosqpub|97057-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000002/attrs', ... (76 bytes))
    Client mosqpub|97057-Nobuyukin sending DISCONNECT
    ```
    * send `handover` command to `pepper(floor 2)` and `robot_request` command to `guide_robot` automatically

        ```bash
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000002/attrs', ... (76 bytes))
        2018-08-09T18:01:31.1533805291+0900|face|/shared/faces/VNDKcDCEUhFR7P7T.JPEG
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000002/cmd', ... (41 bytes))
        pepper_0000000000000002@handover|continue
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000002/cmd', ... (67 bytes))
        guide_robot_0000000000000002@robot_request|r_cmd|Navi|x|20.0|y|20.0
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000002/cmdexe', ... (107 bytes))
        guide_robot_0000000000000002@robot_request|result,success/time,2018-08-09 18:01:32/r_cmd,Navi/x,20.0/y,20.0
        ```
    * send ros message to ros topic `/robot_2f_1/request` automatically

        ```bash
        root@rosbridge:/opt/ros_ws# rostopic echo /robot_2f_1/request
        time: "2018-08-09 18:01:32"
        r_cmd: "Navi"
        pos:
          x: 20.0
          y: 20.0
        ---
        ```
    * update `r_state` to `Guiding` automatically

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000002/attrs/r_state/ | jq .
        {
          "type": "string",
          "value": "Guiding",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-09T18:01:31.981792+0900"
            }
          }
        }
        ```
    * set `visitor` automatically

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000002/attrs/visitor/ | jq .
        {
          "type": "string",
          "value": "5b6c01ed55d7fb0013c57185",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-09T18:01:31.981792+0900"
            }
          }
        }
        ```
1. simulate to send `facedetect` cmd result from `pepper(floor 2)`

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000002/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000002@facedetect|success"
    Client mosqpub|48535-Nobuyukin sending CONNECT
    Client mosqpub|48535-Nobuyukin received CONNACK
    Client mosqpub|48535-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000002/cmdexe', ... (42 bytes))
    Client mosqpub|48535-Nobuyukin sending DISCONNECT
    ```
1. simulate to send `handover` cmd result from `pepper(floor 2)`

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000002/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000002@handover|success"
    Client mosqpub|48779-Nobuyukin sending CONNECT
    Client mosqpub|48779-Nobuyukin received CONNACK
    Client mosqpub|48779-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000002/cmdexe', ... (40 bytes))
    Client mosqpub|48779-Nobuyukin sending DISCONNECT
    ```

## robot busy (floor 2) face detect: guidance another visitor while guiding previous visitor
1. simulate to be called `/storage/faces/` REST API by pepper(floor 1)

    ```bash
    mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);export FACEPATH=$(curl -sS -H "Authorization: bearer ${TOKEN}" -H "Content-Type: multipart/form-data" https://api.tech-sketch.jp/storage/faces/ -X POST -F face=@other_persons_face.jpg | jq .path -r);echo ${FACEPATH}
    /shared/faces/ppRBgMmkcMXdhw36.JPEG
    ```
1. simulate to finish reception (floor 2)

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000001/attrs -u iotagent -P XXXXXXXX -m "$d|face|${FACEPATH}|dest|204号室"
    Client mosqpub|37447-Nobuyukin sending CONNECT
    Client mosqpub|37447-Nobuyukin received CONNACK
    Client mosqpub|37447-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/attrs', ... (91 bytes))
    Client mosqpub|37447-Nobuyukin sending DISCONNECT
    ```
    * send `handover` command to `pepper(floor 1)` and `facedetect` command to `pepper(floor 2)` automatically

        ```bash
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/attrs', ... (91 bytes))
        2018-08-09T18:08:23.1533805703+0900|face|/shared/faces/ppRBgMmkcMXdhw36.JPEG|dest|204号室
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000002/cmd', ... (40 bytes))
        pepper_0000000000000002@facedetect|start
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/cmd', ... (34 bytes))
        pepper_0000000000000001@handover|2
        ```
    * record ledger automatically

        ```bash
        mac:$ kubectl exec mongodb-0 -c mongodb -- mongo ledger --eval 'db.visitors.find().sort({"receptionDatetime":-1}).limit(2).pretty()'
        MongoDB shell version v3.6.5
        connecting to: mongodb://127.0.0.1:27017/ledger
        MongoDB server version: 3.6.5
        {
          "_id" : ObjectId("5b6c0488caee090013dcbf44"),
          "status" : "reception",
          "face" : "/shared/faces/ppRBgMmkcMXdhw36.JPEG",
          "faceIds" : [
            "9f071ce8-d5f9-4790-968e-a25a25d8ef1a"
          ],
          "dest" : {
            "dest_human_sensor_id" : "dest_human_sensor_0000000000000003",
            "dest_led_id" : "dest_led_0000000000000003",
            "dest_led_pos_x" : 19,
            "dest_led_pos_y" : -19,
            "dest_pos_x" : 20,
            "dest_pos_y" : -10,
            "floor" : 2,
            "id" : "5b63d6787597100013d0b2a9",
            "name" : "204号室"
          },
          "receptionDatetime" : ISODate("2018-08-09T09:08:23.938Z")
        }
        {
          "_id" : ObjectId("5b6c01ed55d7fb0013c57185"),
          "status" : "reception",
          "face" : "/shared/faces/5eOMQwLJSuQ0SVHb.JPEG",
          "faceIds" : [
            "4bf9d5b1-08be-46ec-8c0c-e52c09987d81"
          ],
          "dest" : {
            "dest_human_sensor_id" : "dest_human_sensor_0000000000000002",
            "dest_led_id" : "dest_led_0000000000000002",
            "dest_led_pos_x" : 19,
            "dest_led_pos_y" : 19,
            "dest_pos_x" : 20,
            "dest_pos_y" : 20,
            "floor" : 2,
            "id" : "5b63d672f6f8a80013b85abf",
            "name" : "203号室"
          },
          "receptionDatetime" : ISODate("2018-08-09T08:57:17.305Z")
        }
        ```
1. simulate to send `welcome` cmd result from `pepper(floor 1)`

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000001/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000001@welcome|success"
    Client mosqpub|22365-Nobuyukin sending CONNECT
    Client mosqpub|22365-Nobuyukin received CONNACK
    Client mosqpub|22365-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/cmdexe', ... (39 bytes))
    Client mosqpub|22365-Nobuyukin sending DISCONNECT
    ```
1. simulate to send `handover` cmd result from `pepper(floor 1)`

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000001/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000001@handover|success"
    Client mosqpub|22763-Nobuyukin sending CONNECT
    Client mosqpub|22763-Nobuyukin received CONNACK
    Client mosqpub|22763-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/cmdexe', ... (40 bytes))
    Client mosqpub|22763-Nobuyukin sending DISCONNECT
    ```

## robot busy (floor 2) face detect: detect another visitor while guiding previous visitor
1. simulate to be called `/storage/faces/` REST API by pepper(floor 2)

    ```bash
    mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);export FACEPATH=$(curl -sS -H "Authorization: bearer ${TOKEN}" -H "Content-Type: multipart/form-data" https://api.tech-sketch.jp/storage/faces/ -X POST -F face=@other_persons_face2.jpg | jq .path -r);echo ${FACEPATH}
    /shared/faces/7Xhz8TdQLr7aphFI.JPEG
    ```
1. simulate to detect visitor

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000002/attrs -u iotagent -P XXXXXXXX -m "$d|face|${FACEPATH}"
    Client mosqpub|97057-Nobuyukin sending CONNECT
    Client mosqpub|97057-Nobuyukin received CONNACK
    Client mosqpub|97057-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000002/attrs', ... (76 bytes))
    Client mosqpub|97057-Nobuyukin sending DISCONNECT
    ```
    * send `handover|busy` command to `pepper(floor 2)` and do not send `robot_request` command to `guide_robot`

        ```bash
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000002/attrs', ... (76 bytes))
        2018-08-09T18:12:27.1533805947+0900|face|/shared/faces/7Xhz8TdQLr7aphFI.JPEG
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000002/cmd', ... (37 bytes))
        pepper_0000000000000002@handover|busy
        ```
    * do not send ros message to ros topic `/robot_2f_1/request`
    * do not update `r_state`

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000002/attrs/r_state/ | jq .
        {
          "type": "string",
          "value": "Guiding",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-09T18:01:31.981792+0900"
            }
          }
        }
        ```
    * do not update `visitor`

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000002/attrs/visitor/ | jq .
        {
          "type": "string",
          "value": "5b6c01ed55d7fb0013c57185",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-09T18:01:31.981792+0900"
            }
          }
        }
        ```
    * record ledger automatically as busy state

        ```bash
        mac:$ kubectl exec mongodb-0 -c mongodb -- mongo ledger --eval 'db.visitors.find().sort({"receptionDatetime":-1}).limit(2).pretty()'
        MongoDB shell version v3.6.5
        connecting to: mongodb://127.0.0.1:27017/ledger
        MongoDB server version: 3.6.5
        {
          "_id" : ObjectId("5b6c0488caee090013dcbf44"),
          "status" : "busy",
          "face" : "/shared/faces/ppRBgMmkcMXdhw36.JPEG",
          "faceIds" : [
            "9f071ce8-d5f9-4790-968e-a25a25d8ef1a"
          ],
          "dest" : {
            "dest_human_sensor_id" : "dest_human_sensor_0000000000000003",
            "dest_led_id" : "dest_led_0000000000000003",
            "dest_led_pos_x" : 19,
            "dest_led_pos_y" : -19,
            "dest_pos_x" : 20,
            "dest_pos_y" : -10,
            "floor" : 2,
            "id" : "5b63d6787597100013d0b2a9",
            "name" : "204号室"
          },
          "receptionDatetime" : ISODate("2018-08-09T09:08:23.938Z"),
          "busyDatetime" : ISODate("2018-08-09T09:12:28.015Z")
        }
        {
          "_id" : ObjectId("5b6c01ed55d7fb0013c57185"),
          "status" : "reception",
          "face" : "/shared/faces/5eOMQwLJSuQ0SVHb.JPEG",
          "faceIds" : [
            "4bf9d5b1-08be-46ec-8c0c-e52c09987d81"
          ],
          "dest" : {
            "dest_human_sensor_id" : "dest_human_sensor_0000000000000002",
            "dest_led_id" : "dest_led_0000000000000002",
            "dest_led_pos_x" : 19,
            "dest_led_pos_y" : 19,
            "dest_pos_x" : 20,
            "dest_pos_y" : 20,
            "floor" : 2,
            "id" : "5b63d672f6f8a80013b85abf",
            "name" : "203号室"
          },
          "receptionDatetime" : ISODate("2018-08-09T08:57:17.305Z")
        }
        ```

## robot busy (floor 2) face detect: arrival previous visitor
1. simulate to receive robot state (Standby)
    * publish ros message to `/robot_2f_1/state`

    ```bash
    root@rosbridge:/opt/ros_ws# rostopic pub -1 /robot_2f_1/state office_guide_robot/r_state "
    time: '2018-10-09 08:07:16'
    r_mode: 'Standby'
    pos:
      x: 20.0
      y: 20.2
      theta: 19.5
    "
    ```
    * update `r_state` to `Suspending` automatically

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000002/attrs/r_state/ | jq .
        {
          "type": "string",
          "value": "Suspending",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-09T18:18:00.608256+0900"
            }
          }
        }
        ```
1. simuate visitor arriving at the destination

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /dest_human_sensor/dest_human_sensor_0000000000000002/attrs -u iotagent -P XXXXXXXX -m "$d|arrival|$d"
    Client mosqpub|65572-Nobuyukin sending CONNECT
    Client mosqpub|65572-Nobuyukin received CONNACK
    Client mosqpub|65572-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/dest_human_sensor/dest_human_sensor_0000000000000002/attrs', ... (79 bytes))
    Client mosqpub|65572-Nobuyukin sending DISCONNECT
    ```
    * receive MQTT message and send `action|off` message to `dest_led_0000000000000002` and `robot_request` command to `guide_robot_0000000000000002` automatically

        ```bash
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/dest_human_sensor/dest_human_sensor_0000000000000002/attrs', ... (79 bytes))
        2018-08-09T18:19:10.1533806350+0900|arrival|2018-08-09T18:19:10.1533806350+0900
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/dest_led/dest_led_0000000000000002/cmd', ... (36 bytes))
        dest_led_0000000000000002@action|off
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000002/cmd', ... (65 bytes))
        guide_robot_0000000000000002@robot_request|r_cmd|Navi|x|0.0|y|0.0
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000002/cmdexe', ... (105 bytes))
        guide_robot_0000000000000002@robot_request|result,success/time,2018-08-09 18:19:11/r_cmd,Navi/x,0.0/y,0.0
        ```
    * send ros message to ros topic `/robot_2f_1/request` automatically

        ```bash
        root@rosbridge:/opt/ros_ws# rostopic echo /robot_2f_1/request
        time: "2018-08-09 18:19:11"
        r_cmd: "Navi"
        pos:
          x: 0.0
          y: 0.0
        ---
        ```
    * update `r_state` to `Returning` automatically

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000002/attrs/r_state/ | jq .
        {
          "type": "string",
          "value": "Returning",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-09T18:19:11.166233+0900"
            }
          }
        }
        ```
    * record ledger automatically

        ```bash
        mac:$ kubectl exec mongodb-0 -c mongodb -- mongo ledger --eval 'db.visitors.find().sort({"receptionDatetime":-1}).limit(2).pretty()'
        MongoDB shell version v3.6.5
        connecting to: mongodb://127.0.0.1:27017/ledger
        MongoDB server version: 3.6.5
        {
          "_id" : ObjectId("5b6c0488caee090013dcbf44"),
          "status" : "busy",
          "face" : "/shared/faces/ppRBgMmkcMXdhw36.JPEG",
          "faceIds" : [
            "9f071ce8-d5f9-4790-968e-a25a25d8ef1a"
          ],
          "dest" : {
            "dest_human_sensor_id" : "dest_human_sensor_0000000000000003",
            "dest_led_id" : "dest_led_0000000000000003",
            "dest_led_pos_x" : 19,
            "dest_led_pos_y" : -19,
            "dest_pos_x" : 20,
            "dest_pos_y" : -10,
            "floor" : 2,
            "id" : "5b63d6787597100013d0b2a9",
            "name" : "204号室"
          },
          "receptionDatetime" : ISODate("2018-08-09T09:08:23.938Z"),
          "busyDatetime" : ISODate("2018-08-09T09:12:28.015Z")
        }
        {
          "_id" : ObjectId("5b6c01ed55d7fb0013c57185"),
          "status" : "arrival",
          "face" : "/shared/faces/5eOMQwLJSuQ0SVHb.JPEG",
          "faceIds" : [
            "4bf9d5b1-08be-46ec-8c0c-e52c09987d81"
          ],
          "dest" : {
            "dest_human_sensor_id" : "dest_human_sensor_0000000000000002",
            "dest_led_id" : "dest_led_0000000000000002",
            "dest_led_pos_x" : 19,
            "dest_led_pos_y" : 19,
            "dest_pos_x" : 20,
            "dest_pos_y" : 20,
            "floor" : 2,
            "id" : "5b63d672f6f8a80013b85abf",
            "name" : "203号室"
          },
          "receptionDatetime" : ISODate("2018-08-09T08:57:17.305Z"),
          "arrivalDatetime" : ISODate("2018-08-09T09:19:11.133Z")
        }
        ```

## robot busy (floor 2) face detect: clean robot
1. set `r_state` of guide robot as `Waiting`

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v1/updateContext -d @-<<__EOS__ | jq .
    {
      "contextElements": [
        {
          "id": "guide_robot_0000000000000002",
          "isPattern": "false",
          "type": "guide_robot",
          "attributes": [
            {
              "name": "r_state",
              "value": "Waiting",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }, {
              "name": "destx",
              "value": "",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }, {
              "name": "desty",
              "value": "",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }, {
              "name": "visitor",
              "value": "",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }
          ]
        }
      ],
      "updateAction": "UPDATE"
    }
    __EOS__
    ```

## robot busy (floor 2) face verify failure: initialize robot
1. set `r_state` of guide robot as `Waiting`

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v1/updateContext -d @-<<__EOS__ | jq .
    {
      "contextElements": [
        {
          "id": "guide_robot_0000000000000002",
          "isPattern": "false",
          "type": "guide_robot",
          "attributes": [
            {
              "name": "r_state",
              "value": "Waiting",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }, {
              "name": "destx",
              "value": "",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }, {
              "name": "desty",
              "value": "",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }, {
              "name": "visitor",
              "value": "",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }
          ]
        }
      ],
      "updateAction": "UPDATE"
    }
    __EOS__
    ```

## robot busy (floor 2) face verify failure: guidance a visitor
1. simulate to be called `/storage/faces/` REST API by pepper(floor 1)

    ```bash
    mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);export FACEPATH=$(curl -sS -H "Authorization: bearer ${TOKEN}" -H "Content-Type: multipart/form-data" https://api.tech-sketch.jp/storage/faces/ -X POST -F face=@face.jpg | jq .path -r);echo ${FACEPATH}
    /shared/faces/Kib1LCqLG2MLryFm.JPEG
    ```
1. simulate to finish reception (floor 2)

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000001/attrs -u iotagent -P XXXXXXXX -m "$d|face|${FACEPATH}|dest|203号室"
    Client mosqpub|37447-Nobuyukin sending CONNECT
    Client mosqpub|37447-Nobuyukin received CONNACK
    Client mosqpub|37447-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/attrs', ... (91 bytes))
    Client mosqpub|37447-Nobuyukin sending DISCONNECT
    ```
    * send `handover` command to `pepper(floor 1)` and `facedetect` command to `pepper(floor 2)` automatically

        ```bash
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/attrs', ... (91 bytes))
        2018-08-09T18:27:11.1533806831+0900|face|/shared/faces/Kib1LCqLG2MLryFm.JPEG|dest|203号室
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000002/cmd', ... (40 bytes))
        pepper_0000000000000002@facedetect|start
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/cmd', ... (34 bytes))
        pepper_0000000000000001@handover|2
        ```
    * record ledger automatically

        ```bash
        mac:$ kubectl exec mongodb-0 -c mongodb -- mongo ledger --eval 'db.visitors.find().sort({"receptionDatetime":-1}).limit(1).pretty()'
        MongoDB shell version v3.6.5
        connecting to: mongodb://127.0.0.1:27017/ledger
        MongoDB server version: 3.6.5
        {
          "_id" : ObjectId("5b6c08f0caee090013dcbf47"),
          "status" : "reception",
          "face" : "/shared/faces/Kib1LCqLG2MLryFm.JPEG",
          "faceIds" : [
            "5858e177-93a3-4aa6-9a0d-7d1b56ab9b0d"
          ],
          "dest" : {
            "dest_human_sensor_id" : "dest_human_sensor_0000000000000002",
            "dest_led_id" : "dest_led_0000000000000002",
            "dest_led_pos_x" : 19,
            "dest_led_pos_y" : 19,
            "dest_pos_x" : 20,
            "dest_pos_y" : 20,
            "floor" : 2,
            "id" : "5b63d672f6f8a80013b85abf",
            "name" : "203号室"
          },
          "receptionDatetime" : ISODate("2018-08-09T09:27:12.176Z")
        }
        ```
1. simulate to send `welcome` cmd result from `pepper(floor 1)`

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000001/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000001@welcome|success"
    Client mosqpub|22365-Nobuyukin sending CONNECT
    Client mosqpub|22365-Nobuyukin received CONNACK
    Client mosqpub|22365-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/cmdexe', ... (39 bytes))
    Client mosqpub|22365-Nobuyukin sending DISCONNECT
    ```
1. simulate to send `handover` cmd result from `pepper(floor 1)`

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000001/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000001@handover|success"
    Client mosqpub|22763-Nobuyukin sending CONNECT
    Client mosqpub|22763-Nobuyukin received CONNACK
    Client mosqpub|22763-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/cmdexe', ... (40 bytes))
    Client mosqpub|22763-Nobuyukin sending DISCONNECT
    ```

## robot busy (floor 2) face verify failure: detect a visitor
1. simulate to be called `/storage/faces/` REST API by pepper(floor 2)

    ```bash
    mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);export FACEPATH=$(curl -sS -H "Authorization: bearer ${TOKEN}" -H "Content-Type: multipart/form-data" https://api.tech-sketch.jp/storage/faces/ -X POST -F face=@another_face.jpg | jq .path -r);echo ${FACEPATH}
    /shared/faces/FVD2pA2SxSni0pum.JPEG
    ```
1. simulate to detect visitor

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000002/attrs -u iotagent -P XXXXXXXX -m "$d|face|${FACEPATH}"
    Client mosqpub|97057-Nobuyukin sending CONNECT
    Client mosqpub|97057-Nobuyukin received CONNACK
    Client mosqpub|97057-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000002/attrs', ... (76 bytes))
    Client mosqpub|97057-Nobuyukin sending DISCONNECT
    ```
    * send `handover` command to `pepper(floor 2)` and `robot_request` command to `guide_robot` automatically

        ```bash
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000002/attrs', ... (76 bytes))
        2018-08-09T18:29:59.1533806999+0900|face|/shared/faces/FVD2pA2SxSni0pum.JPEG
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000002/cmd', ... (41 bytes))
        pepper_0000000000000002@handover|continue
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000002/cmd', ... (67 bytes))
        guide_robot_0000000000000002@robot_request|r_cmd|Navi|x|20.0|y|20.0
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000002/cmdexe', ... (107 bytes))
        guide_robot_0000000000000002@robot_request|result,success/time,2018-08-09 18:30:00/r_cmd,Navi/x,20.0/y,20.0
        ```
    * send ros message to ros topic `/robot_2f_1/request` automatically

        ```bash
        root@rosbridge:/opt/ros_ws# rostopic echo /robot_2f_1/request
        time: "2018-08-09 18:30:00"
        r_cmd: "Navi"
        pos:
          x: 20.0
          y: 20.0
        ---
        ```
    * update `r_state` to `Guiding` automatically

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000002/attrs/r_state/ | jq .
        {
          "type": "string",
          "value": "Guiding",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-09T18:30:00.493667+0900"
            }
          }
        }
        ```
    * set `visitor` automatically

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000002/attrs/visitor/ | jq .
        {
          "type": "string",
          "value": "5b6c08f0caee090013dcbf47",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-09T18:30:00.493667+0900"
            }
          }
        }
        ```
1. simulate to send `facedetect` cmd result from `pepper(floor 2)`

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000002/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000002@facedetect|success"
    Client mosqpub|48535-Nobuyukin sending CONNECT
    Client mosqpub|48535-Nobuyukin received CONNACK
    Client mosqpub|48535-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000002/cmdexe', ... (42 bytes))
    Client mosqpub|48535-Nobuyukin sending DISCONNECT
    ```
1. simulate to send `handover` cmd result from `pepper(floor 2)`

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000002/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000002@handover|success"
    Client mosqpub|48779-Nobuyukin sending CONNECT
    Client mosqpub|48779-Nobuyukin received CONNACK
    Client mosqpub|48779-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000002/cmdexe', ... (40 bytes))
    Client mosqpub|48779-Nobuyukin sending DISCONNECT
    ```

## robot busy (floor 2) face verify failure: guidance another visitor while guiding previous visitor
1. simulate to be called `/storage/faces/` REST API by pepper(floor 1)

    ```bash
    mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);export FACEPATH=$(curl -sS -H "Authorization: bearer ${TOKEN}" -H "Content-Type: multipart/form-data" https://api.tech-sketch.jp/storage/faces/ -X POST -F face=@other_persons_face.jpg | jq .path -r);echo ${FACEPATH}
    /shared/faces/hYuXCIssiVrsYsCy.JPEG
    ```
1. simulate to finish reception (floor 2)

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000001/attrs -u iotagent -P XXXXXXXX -m "$d|face|${FACEPATH}|dest|204号室"
    Client mosqpub|37447-Nobuyukin sending CONNECT
    Client mosqpub|37447-Nobuyukin received CONNACK
    Client mosqpub|37447-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/attrs', ... (91 bytes))
    Client mosqpub|37447-Nobuyukin sending DISCONNECT
    ```
    * send `handover` command to `pepper(floor 1)` and `facedetect` command to `pepper(floor 2)` automatically

        ```bash
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/attrs', ... (91 bytes))
        2018-08-09T18:33:30.1533807210+0900|face|/shared/faces/hYuXCIssiVrsYsCy.JPEG|dest|204号室
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000002/cmd', ... (40 bytes))
        pepper_0000000000000002@facedetect|start
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/cmd', ... (34 bytes))
        pepper_0000000000000001@handover|2
        ```
    * record ledger automatically

        ```bash
        mac:$ kubectl exec mongodb-0 -c mongodb -- mongo ledger --eval 'db.visitors.find().sort({"receptionDatetime":-1}).limit(2).pretty()'
        MongoDB shell version v3.6.5
        connecting to: mongodb://127.0.0.1:27017/ledger
        MongoDB server version: 3.6.5
        {
          "_id" : ObjectId("5b6c0a6a55d7fb0013c57187"),
          "status" : "reception",
          "face" : "/shared/faces/hYuXCIssiVrsYsCy.JPEG",
          "faceIds" : [
            "e7f044c7-7fad-43ef-aee5-844f29f13e82"
          ],
          "dest" : {
            "dest_human_sensor_id" : "dest_human_sensor_0000000000000003",
            "dest_led_id" : "dest_led_0000000000000003",
            "dest_led_pos_x" : 19,
            "dest_led_pos_y" : -19,
            "dest_pos_x" : 20,
            "dest_pos_y" : -10,
            "floor" : 2,
            "id" : "5b63d6787597100013d0b2a9",
            "name" : "204号室"
          },
          "receptionDatetime" : ISODate("2018-08-09T09:33:30.323Z")
        }
        {
          "_id" : ObjectId("5b6c08f0caee090013dcbf47"),
          "status" : "reception",
          "face" : "/shared/faces/Kib1LCqLG2MLryFm.JPEG",
          "faceIds" : [
            "5858e177-93a3-4aa6-9a0d-7d1b56ab9b0d"
          ],
          "dest" : {
            "dest_human_sensor_id" : "dest_human_sensor_0000000000000002",
            "dest_led_id" : "dest_led_0000000000000002",
            "dest_led_pos_x" : 19,
            "dest_led_pos_y" : 19,
            "dest_pos_x" : 20,
            "dest_pos_y" : 20,
            "floor" : 2,
            "id" : "5b63d672f6f8a80013b85abf",
            "name" : "203号室"
          },
          "receptionDatetime" : ISODate("2018-08-09T09:27:12.176Z")
        }
        ```
1. simulate to send `welcome` cmd result from `pepper(floor 1)`

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000001/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000001@welcome|success"
    Client mosqpub|22365-Nobuyukin sending CONNECT
    Client mosqpub|22365-Nobuyukin received CONNACK
    Client mosqpub|22365-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/cmdexe', ... (39 bytes))
    Client mosqpub|22365-Nobuyukin sending DISCONNECT
    ```
1. simulate to send `handover` cmd result from `pepper(floor 1)`

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000001/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000001@handover|success"
    Client mosqpub|22763-Nobuyukin sending CONNECT
    Client mosqpub|22763-Nobuyukin received CONNACK
    Client mosqpub|22763-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/cmdexe', ... (40 bytes))
    Client mosqpub|22763-Nobuyukin sending DISCONNECT
    ```

## robot busy (floor 2) face verify failure: verify failure while guiding previous visitor
1. simulate to be called `/storage/faces/` REST API by pepper(floor 2)

    ```bash
    mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);export FACEPATH=$(curl -sS -H "Authorization: bearer ${TOKEN}" -H "Content-Type: multipart/form-data" https://api.tech-sketch.jp/storage/faces/ -X POST -F face=@nobody_face.jpg | jq .path -r);echo ${FACEPATH}
    /shared/faces/Dxt1O4aN57M2akBJ.JPEG
    ```
1. simulate to detect visitor

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000002/attrs -u iotagent -P XXXXXXXX -m "$d|face|${FACEPATH}"
    Client mosqpub|97057-Nobuyukin sending CONNECT
    Client mosqpub|97057-Nobuyukin received CONNACK
    Client mosqpub|97057-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000002/attrs', ... (76 bytes))
    Client mosqpub|97057-Nobuyukin sending DISCONNECT
    ```
    * send `reask` command to `pepper(floor 2)`

        ```bash
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000002/attrs', ... (76 bytes))
        2018-08-09T18:39:20.1533807560+0900|face|/shared/faces/Dxt1O4aN57M2akBJ.JPEG
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000002/cmd', ... (34 bytes))
        pepper_0000000000000002@reask|true
        ```
    * do not send ros message to ros topic `/robot_2f_1/request`
    * do not update `r_state`

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000002/attrs/r_state/ | jq .
        {
          "type": "string",
          "value": "Guiding",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-09T18:30:00.493667+0900"
            }
          }
        }
        ```
    * do not update `visitor`

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000002/attrs/visitor/ | jq .
        {
          "type": "string",
          "value": "5b6c08f0caee090013dcbf47",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-09T18:30:00.493667+0900"
            }
          }
        }
        ```
1. simulate to send `facedetect` cmd result from `pepper(floor 2)`

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000002/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000002@facedetect|success"
    Client mosqpub|48535-Nobuyukin sending CONNECT
    Client mosqpub|48535-Nobuyukin received CONNACK
    Client mosqpub|48535-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000002/cmdexe', ... (42 bytes))
    Client mosqpub|48535-Nobuyukin sending DISCONNECT
    ```

## robot busy (floor 2) face verify failure: reask destination while guiding previous visitor
1. simulate to finish reasking destination

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000002/attrs -u iotagent -P XXXXXXXX -m "$d|dest|204号室"
    Client mosqpub|21252-Nobuyukin sending CONNECT
    Client mosqpub|21252-Nobuyukin received CONNACK
    Client mosqpub|21252-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000002/attrs', ... (50 bytes))
    Client mosqpub|21252-Nobuyukin sending DISCONNECT
    ```
    * send `handover|busy` command to `pepper(floor 2)` and do not send `robot_request` command to `guide_robot`

        ```bash
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000002/attrs', ... (50 bytes))
        2018-08-09T18:43:11.1533807791+0900|dest|204号室
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000002/cmd', ... (37 bytes))
        pepper_0000000000000002@handover|busy
        ```
    * do not send ros message to ros topic `/robot_2f_1/request`
    * do not update `r_state`

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000002/attrs/r_state/ | jq .
        {
          "type": "string",
          "value": "Guiding",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-09T18:30:00.493667+0900"
            }
          }
        }
        ```
    * do not update `visitor`

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000002/attrs/visitor/ | jq .
        {
          "type": "string",
          "value": "5b6c08f0caee090013dcbf47",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-09T18:30:00.493667+0900"
            }
          }
        }
        ```
    * record ledger automatically as reask&busy state

        ```bash
        mac:$ kubectl exec mongodb-0 -c mongodb -- mongo ledger --eval 'db.visitors.find().sort({"receptionDatetime":-1}).limit(2).pretty()'
        MongoDB shell version v3.6.5
        connecting to: mongodb://127.0.0.1:27017/ledger
        MongoDB server version: 3.6.5
        {
          "_id" : ObjectId("5b6c0a6a55d7fb0013c57187"),
          "status" : "reception",
          "face" : "/shared/faces/hYuXCIssiVrsYsCy.JPEG",
          "faceIds" : [
            "e7f044c7-7fad-43ef-aee5-844f29f13e82"
          ],
          "dest" : {
            "dest_human_sensor_id" : "dest_human_sensor_0000000000000003",
            "dest_led_id" : "dest_led_0000000000000003",
            "dest_led_pos_x" : 19,
            "dest_led_pos_y" : -19,
            "dest_pos_x" : 20,
            "dest_pos_y" : -10,
            "floor" : 2,
            "id" : "5b63d6787597100013d0b2a9",
            "name" : "204号室"
          },
          "receptionDatetime" : ISODate("2018-08-09T09:33:30.323Z")
        }
        {
          "_id" : ObjectId("5b6c08f0caee090013dcbf47"),
          "status" : "reception",
          "face" : "/shared/faces/Kib1LCqLG2MLryFm.JPEG",
          "faceIds" : [
            "5858e177-93a3-4aa6-9a0d-7d1b56ab9b0d"
          ],
          "dest" : {
            "dest_human_sensor_id" : "dest_human_sensor_0000000000000002",
            "dest_led_id" : "dest_led_0000000000000002",
            "dest_led_pos_x" : 19,
            "dest_led_pos_y" : 19,
            "dest_pos_x" : 20,
            "dest_pos_y" : 20,
            "floor" : 2,
            "id" : "5b63d672f6f8a80013b85abf",
            "name" : "203号室"
          },
          "receptionDatetime" : ISODate("2018-08-09T09:27:12.176Z")
        }
        ```
        ```bash
        mac:$ kubectl exec mongodb-0 -c mongodb -- mongo ledger --eval 'db.visitors.find().sort({"reaskDatetime":-1}).limit(1).pretty()'
        MongoDB shell version v3.6.5
        connecting to: mongodb://127.0.0.1:27017/ledger
        MongoDB server version: 3.6.5
        {
          "_id" : ObjectId("5b6c0caf55d7fb0013c57189"),
          "status" : "busy",
          "face" : null,
          "faceIds" : [ ],
          "dest" : {
            "dest_human_sensor_id" : "dest_human_sensor_0000000000000003",
            "dest_led_id" : "dest_led_0000000000000003",
            "dest_led_pos_x" : 19,
            "dest_led_pos_y" : -19,
            "dest_pos_x" : 20,
            "dest_pos_y" : -10,
            "floor" : 2,
            "id" : "5b63d6787597100013d0b2a9",
            "name" : "204号室"
          },
          "reaskDatetime" : ISODate("2018-08-09T09:43:11.418Z"),
          "busyDatetime" : ISODate("2018-08-09T09:43:11.470Z")
        }
        ```

## robot busy (floor 2) face verify failure: arrival previous visitor
1. simulate to receive robot state (Standby)
    * publish ros message to `/robot_2f_1/state`

    ```bash
    root@rosbridge:/opt/ros_ws# rostopic pub -1 /robot_2f_1/state office_guide_robot/r_state "
    time: '2018-10-09 08:07:16'
    r_mode: 'Standby'
    pos:
      x: 20.0
      y: 20.2
      theta: 19.5
    "
    ```
    * update `r_state` to `Suspending` automatically

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000002/attrs/r_state/ | jq .
        {
          "type": "string",
          "value": "Suspending",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-09T18:48:13.749136+0900"
            }
          }
        }
        ```
1. simuate visitor arriving at the destination

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /dest_human_sensor/dest_human_sensor_0000000000000002/attrs -u iotagent -P XXXXXXXX -m "$d|arrival|$d"
    Client mosqpub|65572-Nobuyukin sending CONNECT
    Client mosqpub|65572-Nobuyukin received CONNACK
    Client mosqpub|65572-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/dest_human_sensor/dest_human_sensor_0000000000000002/attrs', ... (79 bytes))
    Client mosqpub|65572-Nobuyukin sending DISCONNECT
    ```
    * receive MQTT message and send `action|off` message to `dest_led_0000000000000002` and `robot_request` command to `guide_robot_0000000000000002` automatically

        ```bash
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/dest_human_sensor/dest_human_sensor_0000000000000002/attrs', ... (79 bytes))
        2018-08-09T18:49:39.1533808179+0900|arrival|2018-08-09T18:49:39.1533808179+0900
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/dest_led/dest_led_0000000000000002/cmd', ... (36 bytes))
        dest_led_0000000000000002@action|off
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000002/cmd', ... (65 bytes))
        guide_robot_0000000000000002@robot_request|r_cmd|Navi|x|0.0|y|0.0
        Client mosqsub|27602-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000002/cmdexe', ... (105 bytes))
        guide_robot_0000000000000002@robot_request|result,success/time,2018-08-09 18:49:39/r_cmd,Navi/x,0.0/y,0.0
        ```
    * send ros message to ros topic `/robot_2f_1/request` automatically

        ```bash
        root@rosbridge:/opt/ros_ws# rostopic echo /robot_2f_1/request
        time: "2018-08-09 18:49:39"
        r_cmd: "Navi"
        pos:
          x: 0.0
          y: 0.0
        ---
        ```
    * update `r_state` to `Returning` automatically

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000002/attrs/r_state/ | jq .
        {
          "type": "string",
          "value": "Returning",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-09T18:49:39.529474+0900"
            }
          }
        }
        ```
    * record ledger automatically

        ```bash
        mac:$ kubectl exec mongodb-0 -c mongodb -- mongo ledger --eval 'db.visitors.find().sort({"receptionDatetime":-1}).limit(2).pretty()'
        MongoDB shell version v3.6.5
        connecting to: mongodb://127.0.0.1:27017/ledger
        MongoDB server version: 3.6.5
        {
          "_id" : ObjectId("5b6c0a6a55d7fb0013c57187"),
          "status" : "reception",
          "face" : "/shared/faces/hYuXCIssiVrsYsCy.JPEG",
          "faceIds" : [
            "e7f044c7-7fad-43ef-aee5-844f29f13e82"
          ],
          "dest" : {
            "dest_human_sensor_id" : "dest_human_sensor_0000000000000003",
            "dest_led_id" : "dest_led_0000000000000003",
            "dest_led_pos_x" : 19,
            "dest_led_pos_y" : -19,
            "dest_pos_x" : 20,
            "dest_pos_y" : -10,
            "floor" : 2,
            "id" : "5b63d6787597100013d0b2a9",
            "name" : "204号室"
          },
          "receptionDatetime" : ISODate("2018-08-09T09:33:30.323Z")
        }
        {
          "_id" : ObjectId("5b6c08f0caee090013dcbf47"),
          "status" : "arrival",
          "face" : "/shared/faces/Kib1LCqLG2MLryFm.JPEG",
          "faceIds" : [
            "5858e177-93a3-4aa6-9a0d-7d1b56ab9b0d"
          ],
          "dest" : {
            "dest_human_sensor_id" : "dest_human_sensor_0000000000000002",
            "dest_led_id" : "dest_led_0000000000000002",
            "dest_led_pos_x" : 19,
            "dest_led_pos_y" : 19,
            "dest_pos_x" : 20,
            "dest_pos_y" : 20,
            "floor" : 2,
            "id" : "5b63d672f6f8a80013b85abf",
            "name" : "203号室"
          },
          "receptionDatetime" : ISODate("2018-08-09T09:27:12.176Z"),
          "arrivalDatetime" : ISODate("2018-08-09T09:49:39.457Z")
        }
        ```

## robot busy (floor 2) face verify failure: clean robot
1. set `r_state` of guide robot as `Waiting`

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v1/updateContext -d @-<<__EOS__ | jq .
    {
      "contextElements": [
        {
          "id": "guide_robot_0000000000000002",
          "isPattern": "false",
          "type": "guide_robot",
          "attributes": [
            {
              "name": "r_state",
              "value": "Waiting",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }, {
              "name": "destx",
              "value": "",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }, {
              "name": "desty",
              "value": "",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }, {
              "name": "visitor",
              "value": "",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }
          ]
        }
      ],
      "updateAction": "UPDATE"
    }
    __EOS__
    ```

## auto-return (floor 1): initialize robot
1. set `r_state` of guide robot as `Waiting`

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v1/updateContext -d @-<<__EOS__ | jq .
    {
      "contextElements": [
        {
          "id": "guide_robot_0000000000000001",
          "isPattern": "false",
          "type": "guide_robot",
          "attributes": [
            {
              "name": "r_state",
              "value": "Waiting",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }, {
              "name": "destx",
              "value": "",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }, {
              "name": "desty",
              "value": "",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }, {
              "name": "visitor",
              "value": "",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }
          ]
        }
      ],
      "updateAction": "UPDATE"
    }
    __EOS__
    ```

## auto-return (floor 1): guidance a visitor
1. simulate to finish reception (floor 1)

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000001/attrs -u iotagent -P XXXXXXXX -m "$d|face|null|dest|管理センター"
    Client mosqpub|37117-Nobuyukin sending CONNECT
    Client mosqpub|37117-Nobuyukin received CONNACK
    Client mosqpub|37117-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/attrs', ... (100 bytes))
    Client mosqpub|37117-Nobuyukin sending DISCONNECT
    ```
    * send `handover` command to `pepper(floor 1)` and `robot_request` command to `guide_robot` automatically

        ```bash
        Client mosqsub|94929-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/attrs', ... (69 bytes))
        2018-08-23T16:47:46.1535010466+0900|face|null|dest|管理センター
        Client mosqsub|94929-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/cmd', ... (34 bytes))
        pepper_0000000000000001@handover|1
        Client mosqsub|94929-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000001/cmd', ... (68 bytes))
        guide_robot_0000000000000001@robot_request|r_cmd|Navi|x|-10.0|y|10.0
        Client mosqsub|94929-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000001/cmdexe', ... (108 bytes))
        guide_robot_0000000000000001@robot_request|result,success/time,2018-08-23 16:47:47/r_cmd,Navi/x,-10.0/y,10.0
        ```
    * send ros message to ros topic `/robot_1f_1/request` automatically

        ```bash
        root@rosbridge:/opt/ros_ws# rostopic echo /robot_1f_1/request
        time: "2018-08-23 16:47:47"
        r_cmd: "Navi"
        pos:
          x: -10.0
          y: 10.0
        ---
        ```
    * update `r_state` to `Guiding` automatically

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000001/attrs/r_state/ | jq .
        {
          "type": "string",
          "value": "Guiding",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-23T16:47:47.111182+0900"
            }
          }
        }
        ```
    * set `visitor` automatically

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000001/attrs/visitor/ | jq .
        {
          "type": "string",
          "value": "5b7e66a34baa0d001781c0c1",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-23T16:47:47.111182+0900"
            }
          }
        }
        ```
    * record ledger automatically

        ```bash
        mac:$ kubectl exec mongodb-0 -c mongodb -- mongo ledger --eval 'db.visitors.find().sort({"receptionDatetime":-1}).limit(1).pretty()'
        MongoDB shell version v3.6.6
        connecting to: mongodb://127.0.0.1:27017/ledger
        MongoDB server version: 3.6.6
        {
          "_id" : ObjectId("5b7e66a34baa0d001781c0c1"),
          "status" : "reception",
          "face" : null,
          "faceIds" : [ ],
          "dest" : {
            "dest_human_sensor_id" : "dest_human_sensor_0000000000000001",
            "dest_led_id" : "dest_led_0000000000000001",
            "dest_led_pos_x" : -9,
            "dest_led_pos_y" : 9,
            "dest_pos_x" : -10,
            "dest_pos_y" : 10,
            "floor" : 1,
            "id" : "5b72414dbfec11001637d12f",
            "name" : "管理センター"
          },
          "receptionDatetime" : ISODate("2018-08-23T07:47:47.010Z")
        }
        ```
1. simulate to send `welcome` cmd result from `pepper(floor 1)`

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000001/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000001@welcome|success"
    Client mosqpub|22365-Nobuyukin sending CONNECT
    Client mosqpub|22365-Nobuyukin received CONNACK
    Client mosqpub|22365-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/cmdexe', ... (39 bytes))
    Client mosqpub|22365-Nobuyukin sending DISCONNECT
    ```
1. simulate to send `handover` cmd result from `pepper(floor 1)`

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000001/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000001@handover|success"
    Client mosqpub|22763-Nobuyukin sending CONNECT
    Client mosqpub|22763-Nobuyukin received CONNACK
    Client mosqpub|22763-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/cmdexe', ... (40 bytes))
    Client mosqpub|22763-Nobuyukin sending DISCONNECT
    ```

## auto-return (floor 1): navigating a visitor & auto-return
1. simulate to receive robot state (Standby)
    * publish ros message to `/robot_1f_1/state`

    ```bash
    root@rosbridge:/opt/ros_ws# rostopic pub -1 /robot_1f_1/state office_guide_robot/r_state "
    time: '2018-09-08 07:06:15'
    r_mode: 'Standby'
    pos:
      x: -10.01
      y: 10.02
      theta: 9.1
    "
    ```
    * receive MQTT message

        ```bash
        Client mosqsub|94929-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000001/attrs', ... (98 bytes))
        2018-08-23T16:51:09.055745+0900|time|2018-09-08 07:06:15|r_mode|Standby|x|-10.01|y|10.02|theta|9.1
        ```
    * update `r_state` to `Suspending` automatically

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000001/attrs/r_state/ | jq .
        {
          "type": "string",
          "value": "Suspending",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-23T16:51:09.168243+0900"
            }
          }
        }
        ```
1. after 15 seconds, robot return automatically
    * receive MQTT message and send `action|off` message to `dest_led_0000000000000001` and `robot_request` command to `guide_robot_0000000000000001` automatically

        ```bash
        Client mosqsub|94929-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000001/cmd', ... (65 bytes))
        guide_robot_0000000000000001@robot_request|r_cmd|Navi|x|0.0|y|0.0
        Client mosqsub|94929-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000001/cmdexe', ... (105 bytes))
        guide_robot_0000000000000001@robot_request|result,success/time,2018-08-23 16:51:24/r_cmd,Navi/x,0.0/y,0.0
        Client mosqsub|94929-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/dest_led/dest_led_0000000000000001/cmd', ... (36 bytes))
        dest_led_0000000000000001@action|off
        ```
    * send ros message to ros topic `/robot_1f_1/request` automatically

        ```bash
        root@rosbridge:/opt/ros_ws# rostopic echo /robot_1f_1/request
        time: "2018-08-23 16:51:24"
        r_cmd: "Navi"
        pos:
          x: 0.0
          y: 0.0
        ---
        ```
    * update `r_state` to `Returning` automatically

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000001/attrs/r_state/ | jq .
        {
          "type": "string",
          "value": "Returning",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-23T16:51:24.914075+0900"
            }
          }
        }
        ```
    * reset `visitor` automatically

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000001/attrs/visitor/ | jq .
        {
          "type": "string",
          "value": "",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-23T16:51:24.914075+0900"
            }
          }
        }
        ```
    * but, do not record ledger

        ```bash
        mac:$ kubectl exec mongodb-0 -c mongodb -- mongo ledger --eval 'db.visitors.find().sort({"receptionDatetime":-1}).limit(1).pretty()'
        MongoDB shell version v3.6.6
        connecting to: mongodb://127.0.0.1:27017/ledger
        MongoDB server version: 3.6.6
        {
          "_id" : ObjectId("5b7e66a34baa0d001781c0c1"),
          "status" : "reception",
          "face" : null,
          "faceIds" : [ ],
          "dest" : {
            "dest_human_sensor_id" : "dest_human_sensor_0000000000000001",
            "dest_led_id" : "dest_led_0000000000000001",
            "dest_led_pos_x" : -9,
            "dest_led_pos_y" : 9,
            "dest_pos_x" : -10,
            "dest_pos_y" : 10,
            "floor" : 1,
            "id" : "5b72414dbfec11001637d12f",
            "name" : "管理センター"
          },
          "receptionDatetime" : ISODate("2018-08-23T07:47:47.010Z")
        }
        ```

## auto-return (floor 1): clean robot
1. set `r_state` of guide robot as `Waiting`

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v1/updateContext -d @-<<__EOS__ | jq .
    {
      "contextElements": [
        {
          "id": "guide_robot_0000000000000001",
          "isPattern": "false",
          "type": "guide_robot",
          "attributes": [
            {
              "name": "r_state",
              "value": "Waiting",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }, {
              "name": "destx",
              "value": "",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }, {
              "name": "desty",
              "value": "",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }, {
              "name": "visitor",
              "value": "",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }
          ]
        }
      ],
      "updateAction": "UPDATE"
    }
    __EOS__
    ```

## auto-return (floor 2): initialize robot
1. set `r_state` of guide robot as `Waiting`

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v1/updateContext -d @-<<__EOS__ | jq .
    {
      "contextElements": [
        {
          "id": "guide_robot_0000000000000002",
          "isPattern": "false",
          "type": "guide_robot",
          "attributes": [
            {
              "name": "r_state",
              "value": "Waiting",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }, {
              "name": "destx",
              "value": "",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }, {
              "name": "desty",
              "value": "",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }, {
              "name": "visitor",
              "value": "",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }
          ]
        }
      ],
      "updateAction": "UPDATE"
    }
    __EOS__
    ```

## auto-return (floor 2): guidance a visitor
1. simulate to be called `/storage/faces/` REST API by pepper(floor 1)

    ```bash
    mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);export FACEPATH=$(curl -sS -H "Authorization: bearer ${TOKEN}" -H "Content-Type: multipart/form-data" https://api.tech-sketch.jp/storage/faces/ -X POST -F face=@face.jpg | jq .path -r);echo ${FACEPATH}
    /shared/faces/tZGqEzEEvuc8jhw0.JPEG
    ```
1. simulate to finish reception (floor 2)

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000001/attrs -u iotagent -P XXXXXXXX -m "$d|face|${FACEPATH}|dest|203号室"
    Client mosqpub|37447-Nobuyukin sending CONNECT
    Client mosqpub|37447-Nobuyukin received CONNACK
    Client mosqpub|37447-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/attrs', ... (91 bytes))
    Client mosqpub|37447-Nobuyukin sending DISCONNECT
    ```
    * send `handover` command to `pepper(floor 1)` and `facedetect` command to `pepper(floor 2)` automatically

        ```bash
        Client mosqsub|94929-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/attrs', ... (91 bytes))
        2018-08-23T17:07:19.1535011639+0900|face|/shared/faces/vvlqS5dtbFjdpZ8v.JPEG|dest|203号室
        Client mosqsub|94929-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000002/cmd', ... (40 bytes))
        pepper_0000000000000002@facedetect|start
        Client mosqsub|94929-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/cmd', ... (34 bytes))
        pepper_0000000000000001@handover|2
        ```
    * record ledger automatically

        ```bash
        mac:$ kubectl exec mongodb-0 -c mongodb -- mongo ledger --eval 'db.visitors.find().sort({"receptionDatetime":-1}).limit(1).pretty()'
        MongoDB shell version v3.6.6
        connecting to: mongodb://127.0.0.1:27017/ledger
        MongoDB server version: 3.6.6
        {
          "_id" : ObjectId("5b7e6b374baa0d001781c0c3"),
          "status" : "reception",
          "face" : "/shared/faces/vvlqS5dtbFjdpZ8v.JPEG",
          "faceIds" : [
            "eeaab0a4-eab6-4cbe-9e60-8cdf5ee728ff"
          ],
          "dest" : {
            "dest_human_sensor_id" : "dest_human_sensor_0000000000000002",
            "dest_led_id" : "dest_led_0000000000000002",
            "dest_led_pos_x" : 19,
            "dest_led_pos_y" : 19,
            "dest_pos_x" : 20,
            "dest_pos_y" : 20,
            "floor" : 2,
            "id" : "5b724152dcccea00163fb71a",
            "name" : "203号室"
          },
          "receptionDatetime" : ISODate("2018-08-23T08:07:19.274Z")
        }
        ```
1. simulate to send `welcome` cmd result from `pepper(floor 1)`

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000001/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000001@welcome|success"
    Client mosqpub|22365-Nobuyukin sending CONNECT
    Client mosqpub|22365-Nobuyukin received CONNACK
    Client mosqpub|22365-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/cmdexe', ... (39 bytes))
    Client mosqpub|22365-Nobuyukin sending DISCONNECT
    ```
1. simulate to send `handover` cmd result from `pepper(floor 1)`

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000001/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000001@handover|success"
    Client mosqpub|22763-Nobuyukin sending CONNECT
    Client mosqpub|22763-Nobuyukin received CONNACK
    Client mosqpub|22763-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/cmdexe', ... (40 bytes))
    Client mosqpub|22763-Nobuyukin sending DISCONNECT
    ```

## auto-return (floor 2): detect face
1. simulate to be called `/storage/faces/` REST API by pepper(floor 2)

    ```bash
    mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);export FACEPATH=$(curl -sS -H "Authorization: bearer ${TOKEN}" -H "Content-Type: multipart/form-data" https://api.tech-sketch.jp/storage/faces/ -X POST -F face=@another_face.jpg | jq .path -r);echo ${FACEPATH}
    /shared/faces/JFbVvPd1MW0hvWhP.JPEG
    ```
1. simulate to detect visitor

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000002/attrs -u iotagent -P XXXXXXXX -m "$d|face|${FACEPATH}"
    Client mosqpub|97057-Nobuyukin sending CONNECT
    Client mosqpub|97057-Nobuyukin received CONNACK
    Client mosqpub|97057-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000002/attrs', ... (76 bytes))
    Client mosqpub|97057-Nobuyukin sending DISCONNECT
    ```
    * send `handover` command to `pepper(floor 2)` and `robot_request` command to `guide_robot` automatically

        ```bash
        Client mosqsub|94929-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000002/attrs', ... (76 bytes))
        2018-08-23T17:11:46.1535011906+0900|face|/shared/faces/q9avHdfVDI14PsvH.JPEG
        Client mosqsub|94929-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000002/cmd', ... (41 bytes))
        pepper_0000000000000002@handover|continue
        Client mosqsub|94929-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000002/cmd', ... (67 bytes))
        guide_robot_0000000000000002@robot_request|r_cmd|Navi|x|20.0|y|20.0
        Client mosqsub|94929-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000002/cmdexe', ... (107 bytes))
        guide_robot_0000000000000002@robot_request|result,success/time,2018-08-23 17:11:47/r_cmd,Navi/x,20.0/y,20.0
        ```
    * send ros message to ros topic `/robot_2f_1/request` automatically

        ```bash
        root@rosbridge:/opt/ros_ws# rostopic echo /robot_2f_1/request
        time: "2018-08-23 17:11:47"
        r_cmd: "Navi"
        pos:
          x: 20.0
          y: 20.0
        ---
        ```
    * update `r_state` to `Guiding` automatically

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000002/attrs/r_state/ | jq .
        {
          "type": "string",
          "value": "Guiding",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-23T17:11:47.839444+0900"
            }
          }
        }
        ```
    * set `visitor` automatically

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000002/attrs/visitor/ | jq .
        {
          "type": "string",
          "value": "5b7e6b374baa0d001781c0c3",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-23T17:11:47.839444+0900"
            }
          }
        }
        ```
1. simulate to send `facedetect` cmd result from `pepper(floor 2)`

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000002/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000002@facedetect|success"
    Client mosqpub|48535-Nobuyukin sending CONNECT
    Client mosqpub|48535-Nobuyukin received CONNACK
    Client mosqpub|48535-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000002/cmdexe', ... (42 bytes))
    Client mosqpub|48535-Nobuyukin sending DISCONNECT
    ```
1. simulate to send `handover` cmd result from `pepper(floor 2)`

    ```bash
    mac:$ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/DST_Root_CA_X3.pem -d -t /pepper/pepper_0000000000000002/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000002@handover|success"
    Client mosqpub|48779-Nobuyukin sending CONNECT
    Client mosqpub|48779-Nobuyukin received CONNACK
    Client mosqpub|48779-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000002/cmdexe', ... (40 bytes))
    Client mosqpub|48779-Nobuyukin sending DISCONNECT
    ```

## auto-return (floor 2): navigating a visitor & auto-return
1. simulate to receive robot state (Standby)
    * publish ros message to `/robot_2f_1/state`

    ```bash
    root@rosbridge:/opt/ros_ws# rostopic pub -1 /robot_2f_1/state office_guide_robot/r_state "
    time: '2018-10-09 08:07:16'
    r_mode: 'Standby'
    pos:
      x: 20.0
      y: 20.2
      theta: 19.5
    "
    ```
    * receive MQTT message

        ```bash
        Client mosqsub|94929-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000002/attrs', ... (96 bytes))
        2018-08-23T17:16:53.393796+0900|time|2018-10-09 08:07:16|r_mode|Standby|x|20.0|y|20.2|theta|19.5
        ```
    * update `r_state` to `Suspending` automatically

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000002/attrs/r_state/ | jq .
        {
          "type": "string",
          "value": "Suspending",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-23T17:16:53.471443+0900"
            }
          }
        }
        ```
1. after 15 seconds, robot return automatically
    * receive MQTT message and send `action|off` message to `dest_led_0000000000000002` and `robot_request` command to `guide_robot_0000000000000002` automatically

        ```bash
        Client mosqsub|94929-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000002/cmd', ... (65 bytes))
        guide_robot_0000000000000002@robot_request|r_cmd|Navi|x|0.0|y|0.0
        Client mosqsub|94929-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/guide_robot/guide_robot_0000000000000002/cmdexe', ... (105 bytes))
        guide_robot_0000000000000002@robot_request|result,success/time,2018-08-23 17:17:08/r_cmd,Navi/x,0.0/y,0.0
        Client mosqsub|94929-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/dest_led/dest_led_0000000000000002/cmd', ... (36 bytes))
        dest_led_0000000000000002@action|off
        ```
    * send ros message to ros topic `/robot_2f_1/request` automatically

        ```bash
        time: "2018-08-23 17:17:08"
        r_cmd: "Navi"
        pos:
          x: 0.0
          y: 0.0
        ---
        ```
    * update `r_state` to `Returning` automatically

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000002/attrs/r_state/ | jq .
        {
          "type": "string",
          "value": "Returning",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-23T17:17:08.866387+0900"
            }
          }
        }
        ```
    * reset `visitor` automatically

        ```bash
        mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" https://api.tech-sketch.jp/orion/v2/entities/guide_robot_0000000000000002/attrs/visitor/ | jq .
        {
          "type": "string",
          "value": "",
          "metadata": {
            "TimeInstant": {
              "type": "ISO8601",
              "value": "2018-08-23T17:17:08.866387+0900"
            }
          }
        }
        ```
    * but, do not record ledger

        ```bash
        mac:$ kubectl exec mongodb-0 -c mongodb -- mongo ledger --eval 'db.visitors.find().sort({"receptionDatetime":-1}).limit(1).pretty()'
        MongoDB shell version v3.6.6
        connecting to: mongodb://127.0.0.1:27017/ledger
        MongoDB server version: 3.6.6
        {
          "_id" : ObjectId("5b7e6b374baa0d001781c0c3"),
          "status" : "reception",
          "face" : "/shared/faces/vvlqS5dtbFjdpZ8v.JPEG",
          "faceIds" : [
            "eeaab0a4-eab6-4cbe-9e60-8cdf5ee728ff"
          ],
          "dest" : {
            "dest_human_sensor_id" : "dest_human_sensor_0000000000000002",
            "dest_led_id" : "dest_led_0000000000000002",
            "dest_led_pos_x" : 19,
            "dest_led_pos_y" : 19,
            "dest_pos_x" : 20,
            "dest_pos_y" : 20,
            "floor" : 2,
            "id" : "5b724152dcccea00163fb71a",
            "name" : "203号室"
          },
          "receptionDatetime" : ISODate("2018-08-23T08:07:19.274Z")
        }
        ```

## auto-return (floor 2): clean robot
1. set `r_state` of guide robot as `Waiting`

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-Servicepath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v1/updateContext -d @-<<__EOS__ | jq .
    {
      "contextElements": [
        {
          "id": "guide_robot_0000000000000002",
          "isPattern": "false",
          "type": "guide_robot",
          "attributes": [
            {
              "name": "r_state",
              "value": "Waiting",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }, {
              "name": "destx",
              "value": "",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }, {
              "name": "desty",
              "value": "",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }, {
              "name": "visitor",
              "value": "",
              "metadatas": [
                {
                  "name": "TimeInstant",
                  "type": "ISO8601",
                  "value": "${d}"
                }
              ]
            }
          ]
        }
      ],
      "updateAction": "UPDATE"
    }
    __EOS__
    ```
