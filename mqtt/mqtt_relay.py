#!/usr/bin/python
# -*- coding: utf-8 -*-


#import context  # Ensures paho is in PYTHONPATH
import paho.mqtt.client as mqtt
import time

# If you want to use a specific client id, use
# mqttc = mqtt.Client("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
mqttc_wan = mqtt.Client()
mqttc_lan = mqtt.Client()


def wan_on_connect(mqttc, obj, flags, rc):
    print("mqtt relay wan port connect response: " + str(rc))


def wan_on_message(mqttc, obj, msg):
	print("mqtt relay wan port receive msssage:")
	print("topic: " + msg.topic + " qos: " + str(msg.qos) + " payload: " + str(msg.payload))
	infot = mqttc_lan.publish(msg.topic, msg.payload, qos=2)
	infot.wait_for_publish()

def wan_on_publish(mqttc, obj, mid):
    print("mqtt relay wan port publish response mid: " + str(mid))


def wan_on_subscribe(mqttc, obj, mid, granted_qos):
    print("mqtt relay wan port subscribe reponse mid: " + str(mid) + " granted_qos: " + str(granted_qos))


def wan_on_log(mqttc, obj, level, string):
	print("mqtt relay wan port log:")
	print(string)


def lan_on_connect(mqttc, obj, flags, rc):
    print("mqtt relay lan port connect response: " + str(rc))


def lan_on_message(mqttc, obj, msg):
	print("mqtt relay lan port receive msssage:")
	print("topic: " + msg.topic + " qos: " + str(msg.qos) + " payload: " + str(msg.payload))
	infot = mqttc_wan.publish(msg.topic, msg.payload, qos=2)
	infot.wait_for_publish()

def lan_on_publish(mqttc, obj, mid):
    print("mqtt relay lan port publish response mid: " + str(mid))


def lan_on_subscribe(mqttc, obj, mid, granted_qos):
    print("mqtt relay lan port subscribe reponse mid: " + str(mid) + " granted_qos: " + str(granted_qos))


def lan_on_log(mqttc, obj, level, string):
	print("mqtt relay lan port log:")
	print(string)


if __name__ == "__main__":
	mqttc_wan.on_message = wan_on_message
	mqttc_wanon_connect = wan_on_connect
	mqttc_wan.on_publish = wan_on_publish
	mqttc_wan.on_subscribe = wan_on_subscribe
	mqttc_lan.on_message = lan_on_message
	mqttc_lan.on_connect = lan_on_connect
	mqttc_lan.on_publish = lan_on_publish
	mqttc_lan.on_subscribe = lan_on_subscribe
	# Uncomment to enable debug messages
	# mqttc.on_log = on_log
	mqttc_wan.connect("140.82.48.144", 1037, 60)
	mqttc_lan.connect("127.0.0.1", 1037, 60)
	
	mqttc_wan.loop_start()
	mqttc_lan.loop_start()
	
	mqttc_wan.subscribe("home_pi/wan/#", 2)
	mqttc_lan.subscribe("home_pi/lan/#", 2)
	
	while True:
		time.sleep(1)	