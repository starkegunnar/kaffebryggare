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
# ticks = 27.55 * cups + 6.3, cups = (ticks - 6.3) / 27.55
nohandle = [".", "!"]
# To generalize the Twitter API location.
os.path.expanduser('~user')
# Filenames with words and phrases for message generation.
startFiles = ['kaffe-greetings.txt', 'kaffe-verbs.txt', 'kaffe-names.txt']
doneFiles = ['kaffe-verbs2.txt', 'kaffe-containers.txt', 'kaffe-names.txt']
# Date-time initialization.

class timestamp(object):
	def __init__(self):
		self.lock = threading.Lock()
		self.value = datetime.now()
	def refresh(self):
		self.lock.acquire()
		try:
			self.value = datetime.now()
		finally:
			self.lock.release()
def getCups(ticks):
	return int(round((ticks - 6.3) / 27.55))

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

def composeMessage(messageType, ticks):
	if messageType == 'start':
		return getPhrase(startFiles[0]) + getHandle(10) + " " + getPhrase(startFiles[1]) + " " + getPhrase(startFiles[2]) + getHashtag(3)
	elif messageType == 'done':
		return getPhrase(doneFiles[0]) + " " + str(getCups(ticks)) + " " + getPhrase(doneFiles[1]) + " " + getPhrase(doneFiles[2]) + getHashtag(3)
	else:	
		return "Ooops"

def messagePoll(t):
	strBuffer = ""
	tweet = ""
	while(1):
		try:
			strBuffer += sock.recv(512)
			eol = strBuffer.find('\n')
			if eol != -1:
				received = strBuffer[:eol]
				print received
				if received == 'active':
					tweet = composeMessage('start', 0)
					api.update_status(status=tweet)
					t.refresh()
					print "Tweeted: " + tweet
				else if "done" in received:
					ticks = int(received.split(" ")[1])
					print str(ticks)
					if ticks > 20:
						 tweet = composeMessage('start', 0)
						api.update_status(status=tweet)
						t.refresh()
						print "Tweeted: " + tweet
				strBuffer = strBuffer[eol+1:]
		except KeyboardInterrupt:
			print("Exiting")
			sock.close()
			break;

def timePoll(t):
	try:
		while 1:
			if datetime.now().minute > t.value.minute:
				t.refresh()
				print "timestamp refreshed on timer"
				print t.value
			time.sleep(1)
	except KeyboardInterrupt:
		print "Exiting timePoll"
		return

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

try:
   sock = bluetooth.BluetoothSocket (bluetooth.RFCOMM)
   sock.connect((bluetoothAddr, port))
   print("Connected")
   conn = 1
except BluetoothError as bt:
   print('cannot connect to host' + str(bt))
   exit(0)

ts = timestamp()
t1 = threading.Thread(target=messagePoll, args=(ts,))
t2 = threading.Thread(target=timePoll, args=(ts,))
t1.start()
t2.start()
