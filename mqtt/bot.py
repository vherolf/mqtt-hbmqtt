from typing import Optional, Tuple, Type, Dict

from time import time
from html import escape

from mautrix.types import TextMessageEventContent, MessageType, Format, GenericEvent

from maubot import Plugin, MessageEvent
from maubot.handlers import command

import asyncio

from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_0, QOS_1, QOS_2

from .util import Config

class MqttBot(Plugin):
    config: Config

    async def start(self) -> None:
        await super().start()
        self.on_external_config_update()
        self.C = MQTTClient()
        self.mqttserver = 'mqtt://' + self.config['mqttserver']['hostname'] +':' + str(self.config['mqttserver']['port'])
        await self.C.connect( self.mqttserver )
        if self.config['subscribe_all'] == True:
            await self.C.subscribe([
                ('#', QOS_1),
            ])
            print("subscribed to all topics (not in the topic you use - must be done manually)")
        self.connected = True


    def on_external_config_update(self) -> None:
        self.config.load_and_update()

    @classmethod
    def get_config_class(cls) -> Type['BaseProxyConfig']:
        return Config

    async def stop(self) -> None:
        await self.C.disconnect()
        await super().stop()


    @command.new("publish", aliases=["pub"], help="publish a message to a topic")
    @command.argument("topic", required=True)
    @command.argument("message", pass_raw=True, required=True)
    async def pub_handler(self, evt: MessageEvent, topic:str, message: str) -> None:
        if not message:
            await evt.reply("Usage: !publish [topic] [message]")
            return
        await self.C.publish(topic, message.encode() )
        await evt.respond("published " + message + " to topic " + topic)

    @command.new("subscribe", aliases=["sub"], help="subscribe to a mqtt topic")
    @command.argument("topic", pass_raw=True)
    async def sub_handler(self, evt: MessageEvent, topic: str) -> None:
        await self.C.subscribe([
                ( topic, QOS_1),
            ])
        while self.connected == True:
            message = await self.C.deliver_message()
            packet = message.publish_packet
            print("%s => %s" % ( packet.variable_header.topic_name, str(packet.payload.data)))
            message = "received from " + packet.variable_header.topic_name + ': ' + str(packet.payload.data)
            await evt.respond( message )


    ## this is not needed for mqtt part - only playing around with generic commands
    @command.passive(regex=r"^(?i)on|--- -\.$")
    async def light_on(self, evt: GenericEvent, _: Tuple[str]) -> None:
        topic = self.config["light_on"]["topic"]
        message = self.config["light_on"]["message"]
        await self.C.publish( topic, message.encode() )
        await evt.respond( "light switched on" )

    @command.passive(regex=r"^(?i)off|--- \.\.-\. \.\.-\.$")
    async def light_off(self, evt: GenericEvent, _: Tuple[str]) -> None:
        topic = self.config["light_off"]["topic"]
        message = self.config["light_off"]["message"]
        await self.C.publish( topic, message.encode() )
        await evt.respond( "light switched off" )
