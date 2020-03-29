# mqtt-hbmqtt

A [maubot](https://github.com/maubot/maubot) plugin to publish/subscribe mqtt messages to a MQTT broker using [hbmqtt](https://hbmqtt.readthedocs.io/en/latest/) library as client


## (Optional) How to make a virtualenv for maubot
```
mkdir maubot && cd maubot
python3 -m venv .
source bin/activate
```

## (OPTIONAL) Install Mosquitto Broker and client tools

```
sudo apt-get update
sudo apt-get install mosquitto mosquitto-clients
```

## install python mqtt client library

(If not done yet) Activate your virtualenv and install hqmtt 
```
pip install hbmqtt
python -m maubot
```

## install the bot

clone this repo
```
git clone https://github.com/vherolf/mqtt-hbmqtt.git
```

```
mbc login
```

```
mbc build --upload ./mqtt-hbmqtt
```

make a instance in maubot gui  

## subscribe to a topic (from your bot)

type in your chat window
```
!sub info
```

## publish to the a topic (from your bot)

type in your chat window
```
!pub info Hello World
```

## test from "outside"

### subscribe to a topic (from a shell)

fire up a termnial and subscribe to the "/info" topic
```
mosquito_sub -h localhost -t info
```

### publish to a topic (from a shell)

fire up a termnial and publish to "/info" topic
```
mosquito_pub -h localhost -t info -m "test from shell"
```
