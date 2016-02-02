#!/usr/bin/python3
import logging
import os
import traceback
from ftplib import FTP
from time import sleep
from daemon import DaemonContext
from watchdog_functions import register_pid

def ftp_connect():
    ftp = FTP("192.168.15.20")
    ftp.login("griduser", "Password1")
    return ftp


def changemon(dir_to_watch, logger):
    ls_prev = set()
    process_name = "ftp_watcher"
    pid = register_pid(process_name)
    while True:
        logger.debug("still alive  :"+str(pid))
        ftp = ftp_connect()
        ftp.cwd(dir_to_watch)
        ls = set(ftp.nlst(dir_to_watch))

        add, rem = ls - ls_prev, ls_prev - ls
        if add or rem: yield add, rem

        for file_path in add:
            if str(file_path)[-4:] == ".out":
                basename = os.path.basename(file_path)
                file = open("/home/ilyes/celery-redis/files/" + basename, 'wb')
                ftp.retrbinary('RETR %s' % file_path, file.write)
                file.close()

        ls_prev = ls
        ftp.close()
        sleep(5)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("/var/log/scheduler/ftp_watcher.log")
logger.addHandler(fh)
logger.debug("aaa")
with DaemonContext(files_preserve=[fh.stream, ], ):
    try:
        for add, rem in changemon("/OutPut", logger):
            logger.debug('\n'.join('+ %s' % i for i in add))
    except:
        logger.debug(traceback.print_exc())
