# 4. simulate scenario

## reception
1. subscribe all topics

    ```bash
    mac:$ mosquitto_sub -h mqtt.cloudconductor.jp -p 8883 --cafile ./secrets/ca.crt -d -t /# -u iotagent -P XXXXXXXX
    ```
1. simulate to push button of `button_sensor`

    ```bash
    mac:$ d=$(date '+%Y-%m-%dT%H:%M:%S.%s+0900');mosquitto_pub -h mqtt.cloudconductor.jp -p 8883 --cafile ./secrets/ca.crt -d -t /button_sensor/button_sensor_0000000000000001/attrs -u iotagent -P XXXXXXXX -m "$d|state|on"
    Client mosqpub|52223-Nobuyukin sending CONNECT
    Client mosqpub|52223-Nobuyukin received CONNACK
    Client mosqpub|52223-Nobuyukin sending PUBLISH (d0, q0, r0, m1, '/button_sensor/button_sensor_0000000000000001/attrs', ... (44 bytes))
    Client mosqpub|52223-Nobuyukin sending DISCONNECT
    ```
1. send 'welcome' command to `pepper` automatically when receiving the `state|on` command from `button_sensor`

    ```bash
    mac:$ mosquitto_sub -h mqtt.cloudconductor.jp -p 8883 --cafile ./secrets/ca.crt -d -t /# -u iotagent -P XXXXXXXX
    ...
    Client mosqsub|52097-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/button_sensor/button_sensor_0000000000000001/attrs', ... (44 bytes))
    2018-06-26T13:43:18.1529988198+0900|state|on
    Client mosqsub|52097-Nobuyukin received PUBLISH (d0, q0, r0, m0, '/pepper/pepper_0000000000000001/cmd', ... (37 bytes))
    pepper_0000000000000001@welcome|start
    ```
1. simlate to be called `/destinations/` REST API by `pepper`

    ```bash
    mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" https://api.cloudconductor.jp/destinations/ | jq .
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

