# maubot-mqtt-hbmqtt

A [maubot](https://github.com/maubot/maubot) plugin to publish/subscribe mqtt messages to a MQTT broker (using [hbmqtt](https://hbmqtt.readthedocs.io/en/latest/) library as client)

## install python mqtt client library

In our virtualenv for maubot
```
pip install hbmqtt
python -m maubot
```

## Install Mosquitto Broker

```
sudo apt-get update
sudo apt-get install mosquitto mosquitto-clients
```

## publish to the a topic (from your bot)

type in your chat window
```
!pub info Hello World
```

## subscribe to a topic (from your bot)

type in your chat window
```
!sub info
```

## test from "outside"

### listening to what you type in your bot

fire up a termnial and subscribe to the "/info" topic
```
mosquito_sub -h localhost -t info
```

### publish to bot

fire up a termnial and publish to "/info" topic
```
mosquito_pub -h localhost -t info
```
