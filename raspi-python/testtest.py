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
import matplotlib.pyplot as plt

# For testing
ticks = random.randint(20, 300)
cups = int(round((ticks + 4.5) / 30.25))
nohandle = [".", "!"]
weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
# To generalize the Twitter API location.
home = os.path.expanduser('~')
# Filenames with words and phrases for message generation.
startFiles = ['phrases-eng/kaffe-greetings.txt', 'phrases-eng/kaffe-verbs.txt', 'phrases-eng/kaffe-names.txt']
doneFiles = ['phrases-eng/kaffe-verbs2.txt', 'phrases-eng/kaffe-containers.txt', 'phrases-eng/kaffe-names.txt']
# Date-time initialization.

#Read Config file
file = open(home + '/twitter-conf.txt','r')
conf = file.read().splitlines()
file.close()
#Get handles
file = open('phrases-eng/kaffe-handles.txt','r')
handles = file.read().splitlines()
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
username = conf[5]

#Add followers to tweet handles
# try:
# 	followers = api.get_followers_ids(screen_name=username)
# 	for i in followers['ids']:
# 		follower = api.show_user(user_id=i)
# 		handles.append('@' + follower["screen_name"])
# except TwythonError as e:
# 	print str(e)
def getCups(ticks):
	return int(round((ticks + 4.5) / 30.25))

def getHandle(chance):
	if random.randint(1, chance) == chance:
		return " " + random.choice(handles) + random.choice(nohandle)
	else:
		return random.choice(nohandle)

def getHashtag(chance):
	if random.randint(1, chance) == chance:
		return random.choice(nohandle) + " " + getPhrase('phrases-eng/kaffe-hashtags.txt')
	else:
		return random.choice(nohandle)

def getPhrase(filename):
	file = open(filename,'r')
	phrase = random.choice(file.read().splitlines())
	file.close()
	return phrase

def composeMessage(messageType):
	if messageType == 'start':
		return getPhrase(startFiles[0]) + getHandle(5) + " " + getPhrase(startFiles[1]) + " " + getPhrase(startFiles[2]) + getHashtag(3)
	elif messageType == 'done':
		return getPhrase(doneFiles[0]) + " " + str(cups) + " " + getPhrase(doneFiles[1]) + " " + getPhrase(doneFiles[2]) + getHashtag(3)
	else:	
		return "Ooops"

def updateLog(ticks):
	cups = getCups(ticks)
	fl = open(logfile, 'r+w')
	cupdata = fl.read().splitlines()
	cupdata[day] = str(int(cupdata[day]) + cups)
	fl.seek(0)
	for d in cupdata:
		fl.write(d + '\n')
	fl.close()

def tweetStats():
	print "hej"


print ticks
print str(int(round((294 + 4.5) / 30.25)))
coffeeStart = "TEST: " + composeMessage('start')
coffeeDone = "TEST: " + composeMessage('done')

logs = home + '/tweet-logs-test/'
logfile = logs + 'testcups.log'
print logfile
print logs
print logfile
if not os.path.exists(logs):
	os.makedirs(logs)
day = datetime.today().weekday()
#day = random.randint(0, 6)
print day
print weekdays[day]
cupsperday = []
if os.path.exists(logfile):
	if day == 0:
		fl = open(logfile, 'r')
		values = fl.read().splitlines()
		print values
		fl.close()
		for v in values:
			if v.isdigit():
				cupsperday.append(int(v))
		plt.bar(range(len(cupsperday)), cupsperday, align='center')
		plt.xticks(range(len(weekdays)), weekdays, size='large')
		plt.title("Coffe brewed last week")
		plt.xlabel("Day of the week.")
		plt.ylabel("Cups")
		plt.savefig(logs + 'fig.png')
		fl = open(logfile, 'w')
		fl.write("0\n0\n0\n0\n0\n0\n0")
		fl.close()
		#photo = open(os.path.expanduser('~') + '/tweet-logs/fig.png','rb')
		#response = api.upload_media(media=photo)
		#api.update_status(status="image test!", media_ids=[response['media_id']])
else:
	fl = open(logfile, 'w')
	fl.write("0\n0\n0\n0\n0\n0\n0")
	fl.seek(0)
	fl.close()
fl = open(logfile, 'r+w')
cupdata = fl.read().splitlines()
print cupdata
cupdata[day] = str(int(cupdata[day]) + cups)
print cupdata
fl.seek(0)
for d in cupdata:
	fl.write(d + '\n')
fl.close()

# today = datetime.today()
# file = open(logfile,'r')
# cons = file.read().splitlines()
# file.close()
# plt.plot(cons)
# plt.savefig(os.path.expanduser('~') + '/tweet-logs/fig.png')
# photo = open(os.path.expanduser('~') + '/tweet-logs/fig.png','rb')
# response = api.upload_media(media=photo)
# api.update_status(status="image test!", media_ids=[response['media_id']])

#followers = api.get_followers_ids(screen_name='ssigbgkaffe')
#for i in followers['ids']:
#	data = api.show_user(user_id=i)
#	print(data["screen_name"])

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
