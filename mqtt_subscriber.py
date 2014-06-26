#!/usr/bin/env python
"""
mqtt_subscriber.py : program to test subscribing to MQTT messages.  We subscribe to a channel that publishes messages containing a timestamp and the amount of free RAM in the system.
Capn' Proto is used to encode the messages.
"""

import paho.mqtt.client as paho
import os
import time
import capnp
 
broker = "iot.eclipse.org"
port = 1883

QOS = 2

def on_connect(mosq, obj, rc):
    if rc == 0:
        print "Connected successfully."
    else:
        print "Error code %d connecting to MQTT channel" % rc

def on_message(client, userdata, message):
    #print "message received, raw payload type is %s, length is %d" % (type(message.payload), len(message.payload))
    databytes = bytearray(message.payload)
    data = data_capnp.Data.from_bytes(databytes)
    print "received message %d bytes : %s %s %d %d %d" % (len(databytes), data.systemId, data.timestamp, data.freeRam, data.ppp0RxBytes, data.ppp0TxBytes)

# Load Capn Proto data format definition
data_capnp = capnp.load('data.capnp')

mypid = os.getpid()
client_uniq = "subclient_"+str(mypid)
mqttc = paho.Client(client_uniq, False)

mqttc.on_connect = on_connect
mqttc.on_message = on_message
 
#connect to broker
mqttc.connect(broker, port, 60)
 
mqttc.subscribe("com.sunedison.rsc.freeram", QOS)

while mqttc.loop() == 0:
    pass
