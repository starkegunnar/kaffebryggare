#!/usr/bin/env python
#encoding: utf-8
import os
import sys
import random
import bluetooth
import time
import threading
import OpenSSL
from datetime import datetime
from twython import Twython, TwythonError
#import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Strings
nohandle = [".", "!"]
weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
# Paths and files
home = os.path.expanduser('~/')
scriptdir = os.path.dirname(os.path.realpath(__file__))
os.chdir(scriptdir)
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
def addFollowers():
	try:
		followers = api.get_followers_ids(screen_name=username)
		for i in followers['ids']:
			follower = '@' + api.show_user(user_id=i)["screen_name"]
			if follower not in handles:
				handles.append(follower)
	except TwythonError as e:
		logPrint("Unable to add followers:\n" + str(e))
		return
	except OpenSSL.SSL.SysCallError as e:
		logPrint("Unable to add followers:\n" + str(e))
		return

def logPrint(msg):
	print >> sys.stderr, "<" + str(datetime.now()) + "> " + msg

def getCups(ticks):
	return int(round(0.1/3*ticks))

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

def tweetMessage(tweet, tweettype, media):
	retry = 10
	while retry:
		try:
			retry -= 1
			time.sleep(1)
			if tweettype == 'stats':
				api.update_status(status=tweet, media_ids=[media['media_id']])
			else:
				api.update_status(status=tweet)
			logPrint("Successfully tweeted:\n" + tweet)
			return
		except TwythonError as te:
			logPrint("Twitter error: \n" + str(te) + "\n")
			break
		except IOError as e:
			logPrint("Unable to tweet: \n" + str(e) + "\nRetrying...")
			continue
		except OpenSSL.SSL.SysCallError as e:
			logPrint("Unable to tweet: \n" + str(e) + "\nRetrying...")
			continue
	logPrint("ERROR: Tweet failed!\n")

#Coffee Statistics
def tweetStats():
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
		tweet = composeMessage('stats', totalcups)
		tweetMessage(tweet, 'stats', response)
	else:
		logPrint("This is not the right time for stats")

### MAIN LOOP ###
if __name__ == '__main__':
	strBuffer = ""
	tweet = ""
	addFollowers()
	while(1):
		logPrint("Attempting to connect to bluetooth sensor.")
		while not connected:
			try:
			   	sock = bluetooth.BluetoothSocket (bluetooth.RFCOMM)
			   	sock.connect((bluetoothAddr, port))
			   	logPrint("Connected\n")
			   	connected = True
			except bluetooth.BluetoothError as bt:
			   	logPrint("Cannot connect to host.\n" + str(bt) + "\nRetrying in 10 seconds...\n")
			   	time.sleep(10)
			   	logPrint("Retrying...\n")
			   	continue
			except KeyboardInterrupt:
				logPrint("Exiting")
				sock.close()
				exit(0)

		while connected:
			if day != datetime.today().weekday():
				day = datetime.today().weekday()
				addFollowers()
			try:
				strBuffer += sock.recv(512)
				eol = strBuffer.find('\n')
				if eol != -1:
					received = strBuffer[:eol]
					if received == 'active':
						logPrint(received)
						tweet = composeMessage('start', 0)
						tweetMessage(tweet)
					elif "done" in received:
						logPrint(received)
						ticks = int(received.split(" ")[1])
						logPrint(str(ticks))
						if ticks > 20:
							updateLog(ticks)
							tweet = composeMessage('done', ticks)
							tweetMessage(tweet,0,0)
					strBuffer = strBuffer[eol+1:]
			except bluetooth.BluetoothError as bt:
				logPrint("Connection lost." + str(bt) + "\n")
				connected = False
				sock.close()
			except KeyboardInterrupt:
				logPrint("Exiting")
				sock.close()
				exit(0)

