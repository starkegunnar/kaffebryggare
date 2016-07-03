#!/usr/bin/env python
#encoding: utf-8
import os
import sys
import random
import bluetooth
import time
import threading
from datetime import datetime
from twython import Twython, TwythonError
#import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
# For testing
# ticks = 30.25 * cups - 4.5, cups = (ticks + 4.5) / 30.25
# Strings
nohandle = [".", "!"]
weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
# Paths and files
home = os.path.expanduser('~/')
logs = home + 'tweet-logs/'
logfile = logs + 'cups.log'

if not os.path.exists(logs):
	os.makedirs(logs)

if not os.path.exists(logfile):
	fl = open(logfile, 'w')
	fl.write("0\n0\n0\n0\n0\n0\n0")
	fl.seek(0)
	fl.close()
# Filenames with words and phrases for message generation.
startFiles = ['phrases-eng/kaffe-greetings.txt', 'phrases-eng/kaffe-verbs.txt', 'phrases-eng/kaffe-names.txt']
doneFiles = ['phrases-eng/kaffe-verbs2.txt', 'phrases-eng/kaffe-containers.txt', 'phrases-eng/kaffe-names.txt']
statFiles = ['phrases-eng/kaffe-greetings.txt', 'phrases-eng/kaffe-containers.txt', 'phrases-eng/kaffe-names.txt']
# Date-time initialization.
day = datetime.today().weekday()
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

if len(conf) > 6:
	handles.append(conf[6])

#Add followers to tweet handles
try:
	followers = api.get_followers_ids(screen_name=username)
	for i in followers['ids']:
		follower = api.show_user(user_id=i)
		handles.append('@' + follower["screen_name"])
except TwythonError as e:
	print str(e)
	pass

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

def composeMessage(messageType, ticks):
	if messageType == 'start':
		return getPhrase(startFiles[0]) + getHandle(2) + " " + getPhrase(startFiles[1]) + " " + getPhrase(startFiles[2]) + getHashtag(2)
	elif messageType == 'done':
		return getPhrase(doneFiles[0]) + " " + str(getCups(ticks)) + " " + getPhrase(doneFiles[1]) + " " + getPhrase(doneFiles[2]) + getHashtag(2)
	elif messageType == 'stats':
		return getPhrase(statFiles[0]) + getHandle(2) + " Last week I made " + str(ticks) + " " + getPhrase(statFiles[1]) + " " + getPhrase(statFiles[2]) + getHashtag(2)
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

def tweetMessage(tweet):
	retry = 10
	while retry:
		try:
			retry -= 1
			api.update_status(status=tweet)
			break
		except TwythonError as te:
			print "<" + str(datetime.now()) + "> Twitter error: " + str(te) + "\n"
			break
		except IOError, e:
			print "<" + str(datetime.now()) + "> Unable to tweet: " + str(e) + "\n"
			print "Retrying...\n"
			continue

# Coffee Statistics
cupsperday = []
if day == 0 and datetime.now().hour < 5: # Monday
	fl = open(logfile, 'r')
	values = fl.read().splitlines()
	fl.close()
	for v in values:
		cupsperday.append(int(v))
	totalcups = sum(cupsperday)
	plt.bar(range(len(cupsperday)), cupsperday, align='center')
	plt.xticks(range(len(weekdays)), weekdays, size='large')
	plt.title("Coffee brewed last week")
	plt.xlabel("Day of the week.")
	plt.ylabel("Cups of Coffee")
	plt.savefig(logs + 'fig.png')
	fl = open(logfile, 'w')
	fl.write("0\n0\n0\n0\n0\n0\n0")
	fl.close()
	photo = open(os.path.expanduser('~') + '/tweet-logs/fig.png','rb')
	response = api.upload_media(media=photo)
	api.update_status(status=composeMessage('stats', totalcups), media_ids=[response['media_id']])

### MAIN LOOP ###
strBuffer = ""
tweet = ""
while(1):
	print("Attempting to connect to bluetooth sensor.")
	while not connected:
		try:
		   	sock = bluetooth.BluetoothSocket (bluetooth.RFCOMM)
		   	sock.connect((bluetoothAddr, port))
		   	print("Connected")
		   	connected = True
		except bluetooth.BluetoothError as bt:
		   	print("<" + str(datetime.now()) + "> Cannot connect to host." + str(bt) + "\nRetrying in 10 seconds...")
		   	time.sleep(10)
		   	print "Retrying..."
		   	continue
		except KeyboardInterrupt:
			print("Exiting")
			sock.close()
			exit(0)

	while connected:
		try:
			strBuffer += sock.recv(512)
			eol = strBuffer.find('\n')
			if eol != -1:
				received = strBuffer[:eol]
				if received == 'active':
					print received
					tweet = composeMessage('start', 0)
					print "Tweeting: " + tweet
					tweetMessage(tweet)
				elif "done" in received:
					print received
					ticks = int(received.split(" ")[1])
					print str(ticks)
					if ticks > 20:
						updateLog(ticks)
						tweet = composeMessage('done', ticks)
						print "Tweeting: " + tweet
						tweetMessage(tweet)
				strBuffer = strBuffer[eol+1:]
		except bluetooth.BluetoothError as bt:
			print "<" + str(datetime.now()) + "> Connection lost." + str(bt) + "\n"
			connected = False
			sock.close()
		except KeyboardInterrupt:
			print("Exiting")
			sock.close()
			exit(0)

