#!/usr/bin/env python
"""
mqtt_ckient.py : program to test publishing MQTT messages.  Capn' Proto is used to encode the message.  We send a message containing the system timestamp
and various metrics about the system every 60 seconds
"""
import paho.mqtt.client as paho
import os
import time
import time
import capnp
from uuid import getnode as get_mac
 
broker = "iot.eclipse.org"
port = 1883

CONNECT_TIMEOUT_S = 60
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

def getNetworkByteCount(dev_name):
    '''Return (no. received bytes, no transmitted bytes) for network device dev_name'''
    with open('/proc/net/dev') as fp:
        for line in fp:
            line = line.split()
            if line[0].startswith(dev_name):
                return int(line[1]), int(line[9])
    return 0,0

 
data_capnp = capnp.load('data.capnp')

mypid = os.getpid()
client_uniq = "pubclient_"+str(mypid)
mqttc = paho.Client(client_uniq, False)
 
#connect to broker
mqttc.connect(broker, port, CONNECT_TIMEOUT_S)
 
#remain connected and publish
mqttc.loop_start()

while True:
    data = data_capnp.Data.new_message()
    macAddress = get_mac()
    data.systemIdHi = macAddress >> 32 & 0xffff
    data.systemIdLo = macAddress & 0xffffffff
    data.timestamp = int(time.time())
    data.freeRam = getFreeRam()['free']
    ppp0ByteCount = getNetworkByteCount("ppp0")
    data.ppp0RxBytes = ppp0ByteCount[0]
    data.ppp0TxBytes = ppp0ByteCount[1]
    databytes = bytearray(data.to_bytes())
    mqttc.publish("com.sunedison.rsc.freeram", databytes, QOS, False)
    time.sleep(60)
