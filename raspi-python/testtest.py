#!/usr/bin/env python
#encoding: utf-8
import os
import sys
import random
import bluetooth
import time
from datetime import datetime
from twython import Twython

cups = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
nohandle = [".", "!"]

os.path.expanduser('~user')

startFiles = ['kaffe-greetings.txt', 'kaffe-verbs.txt', 'kaffe-names.txt']
doneFiles = ['kaffe-verbs2.txt', 'kaffe-containers.txt', 'kaffe-names.txt']

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
		return getPhrase(doneFiles[0]) + " " + random.choice(cups) + " " + getPhrase(doneFiles[1]) + " " + getPhrase(doneFiles[2]) + getHashtag(3)
	else:	
		return "Ooops"


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
# file = open('kaffe-greetings.txt','r')
# greets = file.read().splitlines()
# file.close()
# file = open('kaffe-verbs.txt','r')
# verbs = file.read().splitlines()
# file.close()
# file = open('kaffe-names.txt','r')
# names = file.read().splitlines()
# file.close()
# file = open('kaffe-containers.txt', 'r')
# conts = file.read().splitlines()
# file.close()
# file = open('kaffe-verbs2.txt', 'r')
# verbs2 = file.read().splitlines()
# file.close()
# file = open('kaffe-hashtags.txt', 'r')
# hashtags = file.read().splitlines()
# file.close()
# file = open('kaffe-handles.txt', 'r')
# handles = file.read().splitlines()
# file.close()

coffeeStart = "TEST: " + composeMessage('start')
coffeeDone = "TEST: " + composeMessage('done')

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
