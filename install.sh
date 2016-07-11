# install.sh
if [ $(id -u) -ne 0 ]; then
	echo "install.sh needs to be run as root, exiting."
	exit
fi

echo "*** Installing kaffeTweet ***"
SCRIPT=$(readlink -f "$0")
# Path to install.sh, */kaffebryggare/
SCRIPTPATH=$(dirname "$SCRIPT")
echo "*** kaffebryggare path = $SCRIPTPATH ***"

# Install packages required to run
echo "*** Installing packages ***"
apt-get install bluez python-bluez python-pip python-matplotlib python-tk
pip install twython

# Install crontab job
echo "*** Installing crontab jobs to /etc/cron.d/kaffecron ***"
echo "@reboot pi python $SCRIPTPATH/raspi-python/kaffeTweet.py  >> $SCRIPTPATH/logs/kaffe.log 2>&1" >  /etc/cron.d/kaffecron
echo "0 3 * * 1 pi python $SCRIPTPATH/raspi-python/statTweet.py >> $SCRIPTPATH/logs/kaffe.log 2>&1" >> /etc/cron.d/kaffecron

# Install logrotate 
echo "*** Installing logrotate configuration to /etc/logrotate.d/kaffelog ***"
echo "$SCRIPTPATH/logs/kaffe.log {" 	>  /etc/logrotate.d/kaffelog
echo "	rotate 7" 						>> /etc/logrotate.d/kaffelog
echo "	daily" 							>> /etc/logrotate.d/kaffelog
echo "	compress" 						>> /etc/logrotate.d/kaffelog
echo "	copytruncate" 					>> /etc/logrotate.d/kaffelog
echo "	notifempty" 					>> /etc/logrotate.d/kaffelog
echo "}" 								>> /etc/logrotate.d/kaffelog

# Clean-up for testing.
#rm /etc/cron.d/kaffecron
#rm /etc/logrotate.d/kaffelog
