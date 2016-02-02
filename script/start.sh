#!/bin/sh

#sudo -s


## project path
cd ~
cd celery-redis


### add daemon in /etc/init.d
PYTHON="python3"
TEMPLATE="/etc/init.d/skeleton"
SCHEDULER="/etc/init.d/scheduler"
FTP_WATCHER="/etc/init.d/ftp_watcher"
FIX_WATCHDOG="/etc/init.d/fix_watchdog"
SCH_DAEMON="scheduler"
FTP_DAEMON="ftp_watcher"
FIX_DAEMON="fix_watchdog"
REGISTER_DAEMON="register_process.py"

cd /etc/init.d
echo pwd
echo $SCHEDULER
if [ -f "$SCHEDULER" ]
then
	echo  "$SCHEDULER exists."
else
	$PYTHON $REGISTER_DAEMON $SCHEDULER $SCH_DAEMON
fi



if [ -f "$FTP_WATCHER" ]
then
        echo "$FTP_WATCHER exists."
else
	$PYTHON $REGISTER_DAEMON $FTP_WATCHER $FTP_DAEMON
fi


if [ -f "$FIX_WATCHDOG" ]
then
        echo "$FIX_WATCHDOG found."
else
        $PYTHON $REGISTER_DAEMON $FIX_WATCHDOG $FIX_DAEMON
fi



##WATCH_PATH = "/home/ilyes/celery-redis/watch" ## change to the directory to watch




##### start  redis + celery worker
redis-server &
redis-cli config set notify-keyspace-events KEA &
celery worker -A fix_watchdog --app watchdog_functions:app -l info -c5 &


## start the daemons

#python3 fix_watchdog.py $WATCH_PATH &
#python3 scheduler.py  &
#python3 ftp_watcher.py &

