#!/usr/bin/env python
#encoding: utf-8
import os
import sys
import random
import bluetooth
import time
import threading
from datetime import datetime
from twython import Twython

# For testing
ticks = random.randint(20, 300)
cups = str(int(round((ticks + 4.5) / 30.25)))
nohandle = [".", "!"]
# To generalize the Twitter API location.
os.path.expanduser('~user')
# Filenames with words and phrases for message generation.
startFiles = ['kaffe-greetings.txt', 'kaffe-verbs.txt', 'kaffe-names.txt']
doneFiles = ['kaffe-verbs2.txt', 'kaffe-containers.txt', 'kaffe-names.txt']
# Date-time initialization.

def getHandle(chance):
	if random.randint(1, chance) == chance:
		return " " + getPhrase('kaffe-handles.txt') + random.choice(nohandle)
	else:
		return random.choice(nohandle)

def getHashtag(chance):
	if random.randint(1, chance) == chance:
		return random.choice(nohandle) + " " + getPhrase('kaffe-hashtags.txt')
	else:
		return random.choice(nohandle)

def getPhrase(filename):
	file = open(filename,'r')
	phrase = random.choice(file.read().splitlines())
	file.close()
	return phrase

def composeMessage(messageType):
	if messageType == 'start':
		return getPhrase(startFiles[0]) + getHandle(10) + " " + getPhrase(startFiles[1]) + " " + getPhrase(startFiles[2]) + getHashtag(3)
	elif messageType == 'done':
		return getPhrase(doneFiles[0]) + " " + cups + " " + getPhrase(doneFiles[1]) + " " + getPhrase(doneFiles[2]) + getHashtag(3)
	else:	
		return "Ooops"
print ticks
print str(int(round((294 + 4.5) / 30.25)))
coffeeStart = "TEST: " + composeMessage('start')
coffeeDone = "TEST: " + composeMessage('done')

#Read Config file
file = open(os.path.expanduser('~') + '/twitter-conf2.txt','r')
conf = file.read().splitlines()
file.close()

#Bluetooth constants
bluetoothAddr = conf[0]
port = 1
connected = False

#Twitter constants
api_key = conf[1]
api_secret = conf[2]
access_token = conf[3]
access_token_secret = conf[4]
api = Twython(api_key, api_secret, access_token, access_token_secret)

followers = api.get_followers_ids(screen_name='ssigbgkaffe')
for i in followers['ids']:
	data = api.show_user(user_id=i)
	print(data["screen_name"])

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
#        		api.update_status(status=coffeeStart)
#			print "Tweeted: " + coffeeStart
#        	buf = buf[eol+1:]
#    except KeyboardInterrupt:
#        print("Exiting")
#        break;
#sock.close()
#api.update_status(status=coffeeDone)
print "Tweeted: " + coffeeStart
print "Tweeted: " + coffeeDone
