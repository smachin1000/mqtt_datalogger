#!/usr/bin/env python
"""
mqtt_ckient.py : program to test publishing MQTT messages.  Capn' Proto is used to encode the message.  We send a message containing the system timestamp
and amount of free RAM eveyr 60 seconds.
"""
import paho.mqtt.client as paho
import os
import time
import datetime
import capnp
from array import array
 
broker = "iot.eclipse.org"
port = 1883

QOS = 2

def getFreeRam():
    """
    Get node total memory and memory usage
    """
    with open('/proc/meminfo', 'r') as mem:
        ret = {}
        tmp = 0
        for i in mem:
            sline = i.split()
            if str(sline[0]) == 'MemTotal:':
                ret['total'] = int(sline[1])
            elif str(sline[0]) in ('MemFree:', 'Buffers:', 'Cached:'):
                tmp += int(sline[1])
        ret['free'] = tmp
        ret['used'] = int(ret['total']) - int(ret['free'])
    return ret
 
data_capnp = capnp.load('data.capnp')

mypid = os.getpid()
client_uniq = "pubclient_"+str(mypid)
mqttc = paho.Client(client_uniq, False) #nocleanstart
 
#connect to broker
mqttc.connect(broker, port, 60)
 
#remain connected and publish
mqttc.loop_start()

while True:
    data = data_capnp.Data.new_message()
    data.timestamp = str(datetime.datetime.now())
    data.freeRam = getFreeRam()['free']
    databytes = bytearray(data.to_bytes())
    mqttc.publish("com.sunedison.rsc.freeram", databytes, QOS, False)
    #print "message published type %s length %d" % (type(databytes), len(databytes))
    time.sleep(60)
