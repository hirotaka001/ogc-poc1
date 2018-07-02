# 4. simulate scenario

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
    $ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /pepper/pepper_0000000000000001/attrs -u iotagent -P XXXXXXXX -m "$d|face|/shared/faces/IoYu2c4sggdVLi49.JPEG|dest|ProjectRoom 1"
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
1. simulate to send `welcome` cmd result

    ```bash
    $ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /pepper/pepper_0000000000000001/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000001@welcome|success"
    Client mosqpub|22365-Nobuyukin sending CONNECT
    Client mosqpub|22365-Nobuyukin received CONNACK
    Client mosqpub|22365-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/cmdexe', ... (39 bytes))
    Client mosqpub|22365-Nobuyukin sending DISCONNECT
    ```

    * describe the entity of `pepper_0000000000000001`

        ```bash
        $ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-ServicePath: /" https://api.tech-sketch.jp/orion/v2/entities/pepper_0000000000000001/ | jq .
        {
          "id": "pepper_0000000000000001",
          "type": "pepper",
          "TimeInstant": {
            "type": "ISO8601",
            "value": "2018-06-29T02:18:26.00Z",
            "metadata": {}
          },
          "dest": {
            "type": "string",
            "value": "ProjectRoom 1",
            "metadata": {
              "TimeInstant": {
                "type": "ISO8601",
                "value": "2018-06-29T11:13:27.1530238407+0900"
              }
            }
          },
          "face": {
            "type": "string",
            "value": "/shared/faces/IoYu2c4sggdVLi49.JPEG",
            "metadata": {
              "TimeInstant": {
                "type": "ISO8601",
                "value": "2018-06-29T11:13:27.1530238407+0900"
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
            "value": "PENDING",
            "metadata": {
              "TimeInstant": {
                "type": "ISO8601",
                "value": "2018-06-29T02:13:31.276Z"
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
                "value": "2018-06-29T02:18:26.358Z"
              }
            }
          },
          "welcome_status": {
            "type": "commandStatus",
            "value": "OK",
            "metadata": {
              "TimeInstant": {
                "type": "ISO8601",
                "value": "2018-06-29T02:18:26.358Z"
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
1. simulate to send `handover` cmd result

    ```bash
    $ mosquitto_pub -h mqtt.tech-sketch.jp -p 8883 --cafile ./secrets/ca.crt -d -t /pepper/pepper_0000000000000001/cmdexe -u iotagent -P XXXXXXXX -m "pepper_0000000000000001@handover|success"
    Client mosqpub|22763-Nobuyukin sending CONNECT
    Client mosqpub|22763-Nobuyukin received CONNACK
    Client mosqpub|22763-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/pepper/pepper_0000000000000001/cmdexe', ... (40 bytes))
    Client mosqpub|22763-Nobuyukin sending DISCONNECT
    ```

    * describe the entity of `pepper_0000000000000001`

        ```bash
        $ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-ServicePath: /" https://api.tech-sketch.jp/orion/v2/entities/pepper_0000000000000001/ | jq .
        {
          "id": "pepper_0000000000000001",
          "type": "pepper",
          "TimeInstant": {
            "type": "ISO8601",
            "value": "2018-06-29T02:25:23.00Z",
            "metadata": {}
          },
          "dest": {
            "type": "string",
            "value": "ProjectRoom 1",
            "metadata": {
              "TimeInstant": {
                "type": "ISO8601",
                "value": "2018-06-29T11:13:27.1530238407+0900"
              }
            }
          },
          "face": {
            "type": "string",
            "value": "/shared/faces/IoYu2c4sggdVLi49.JPEG",
            "metadata": {
              "TimeInstant": {
                "type": "ISO8601",
                "value": "2018-06-29T11:13:27.1530238407+0900"
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
                "value": "2018-06-29T02:25:23.976Z"
              }
            }
          },
          "handover_status": {
            "type": "commandStatus",
            "value": "OK",
            "metadata": {
              "TimeInstant": {
                "type": "ISO8601",
                "value": "2018-06-29T02:25:23.976Z"
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
                "value": "2018-06-29T02:18:26.358Z"
              }
            }
          },
          "welcome_status": {
            "type": "commandStatus",
            "value": "OK",
            "metadata": {
              "TimeInstant": {
                "type": "ISO8601",
                "value": "2018-06-29T02:18:26.358Z"
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
