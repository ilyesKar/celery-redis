#!/bin/sh

# Make sure only root can run our script
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

mkdir -p /opt/scheduler
mkdir -p /var/log/scheduler
mkdir -p /opt/scheduler/encrypted_files/
mkdir -p /opt/scheduler/req_files/
mkdir -p /opt/scheduler/tools/

cp -f  ./*.py /opt/scheduler 
cp -rf ./templates/ /opt/scheduler/
cp -f ./tools/* /opt/scheduler/tools
##copy init file
cp -f ./init/* /etc/init.d/

## project path
cd /opt/scheduler
chmod +x *.py





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
        echo "$FIX_WATCHDOG exists."
else
        $PYTHON $REGISTER_DAEMON $FIX_WATCHDOG $FIX_DAEMON
fi



##WATCH_PATH = "/home/ilyes/celery-redis/watch" ## change to the directory to watch




##### start  redis + celery worker
apt-get install --upgrade redis-server
#redis-server &
#redis-cli config set notify-keyspace-events KEA &
#celery worker -A fix_watchdog --app watchdog_functions:app -l info -c5 &


## start the daemons
#python3 fix_watchdog.py $WATCH_PATH &
#python3 scheduler.py  &
#python3 ftp_watcher.py &

