#!/usr/bin/env python
#encoding: utf-8
import os
import sys
import random
import bluetooth
from twython import Twython

cups = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
nohandle = [",", "!"]
nohash = [".", "!", " "]

os.path.expanduser('~user')

def getHandle(stringArray, defaultArray, oneIn):
	if random.randint(1, oneIn) == oneIn:
		return " " + random.choice(stringArray) + random.choice(defaultArray)
	else:
		return random.choice(defaultArray)

#Read Config file
file = open(os.path.expanduser('~') + '/twitter-conf.txt','r')
conf = file.read().splitlines()
file.close()

#Bluetooth constants
bluetoothAddr = conf[0]
port = 1

#Twitter constants
api_key = conf[1]
api_secret = conf[2]
access_token = conf[3]
access_token_secret = conf[4]
api = Twython(api_key, api_secret, access_token, access_token_secret)

#Twitter strings
file = open('kaffe-greetings.txt','r')
greets = file.read().splitlines()
file.close()
file = open('kaffe-verbs.txt','r')
verbs = file.read().splitlines()
file.close()
file = open('kaffe-names.txt','r')
names = file.read().splitlines()
file.close()
file = open('kaffe-containers.txt', 'r')
conts = file.read().splitlines()
file.close()
file = open('kaffe-verbs2.txt', 'r')
verbs2 = file.read().splitlines()
file.close()
file = open('kaffe-hashtags.txt', 'r')
hashtags = file.read().splitlines()
file.close()
file = open('kaffe-handles.txt', 'r')
handles = file.read().splitlines()
file.close()

tweetStr = "TEST: " + random.choice(greets) + getHandle(handles, nohandle, 10) + " " + random.choice(verbs) + " " + random.choice(names) + getHandle(hashtags, nohash, 3)

#try:
#    sock = bluetooth.BluetoothSocket (bluetooth.RFCOMM)
#    sock.connect((bluetoothAddr, port))
#    print("initial connection")
#    conn = 1
#except BluetoothError as bt:
#    print('cannot connect to host' + str(bt))
#    exit(0)
#
#buf = ""
#while 1:
#    try:
#        buf += sock.recv(512)
#        eol = buf.find('\n')
#        if eol != -1:
#        	rec = buf[:eol]
#        	print buf
#        	if rec == 'tweet':
#        		api.update_status(status=tweetStr)
#			print "Tweeted: " + tweetStr
#        	buf = buf[eol+1:]
#    except KeyboardInterrupt:
#        print("Exiting")
#        break;
#sock.close()
api.update_status(status=tweetStr)
print "Tweeted: " + tweetStr
