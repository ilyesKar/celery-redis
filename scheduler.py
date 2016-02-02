#!/usr/bin/python3
import ftplib
import json
import logging
import threading

from daemon import DaemonContext

from watchdog_functions import *

BASE_KEY = '__key*__:*'

__HOST__ = "192.168.0.103"
__LOGIN__ = "Ilyes"
__PSW__ = "password210#"


def ftp_store(host, login, psw, filename):
    ftp = ftplib.FTP(host)
    ftp.login(login, psw)
    ftp.cwd("/req")
    ftp.storlines("STOR " + "ilyes.req", open(filename, 'rb'))


def create_req(output_file, isin_set, logger):
    logger.debug("create start")
    try:
        bond_req = open("/opt/scheduler/templates/bond_test.req", "r")
    except:
        logger.debug("input create error")
    try:
        bond_req_res = open(output_file, "w")

    except:
        logger.debug("ouput create error")
    for line in bond_req.read().split('\n'):
        bond_req_res.writelines(line + "\n")
        if line == "START-OF-DATA":
            for data in isin_set:
                bond_req_res.writelines(data + " Corp\n")
    bond_req_res.close()
    bond_req.close()
    output_filename = os.path.basename(output_file)
    encrypt_file  = "/opt/scheduler/encrypted_files/" + output_filename
    file_encrypt(output_file,encrypt_file , DES_KEY)
    ftp_store(__HOST__, __LOGIN__, __PSW__, encrypt_file)
    logger.debug("create end")


class Listener(threading.Thread):
    def __init__(self, r, channels, logger):
        threading.Thread.__init__(self)
        self.redis = r
        self.pubsub = self.redis.pubsub()
        self.pubsub.psubscribe(channels)
        process_name = "scheduler"
        register_pid(process_name)
        self.logger = logger

    def work(self, item):
        if item['channel'] == b'__keyevent@0__:set' and item['data'].decode('utf-8')[:11] == 'ilyes:json:':
            print(item['data'])
            # print(item)
            json_data = r.get(item['data']).decode("utf-8")
            print(json_data)
            data = json.loads(json_data)
            isin_set = set()
            for key, value in data.items():
                if key == "ProductData":
                    for d in value:
                        if not isin_set.issuperset(d["Isin"]):
                            isin_set.add(d["Isin"])
            create_req("/opt/scheduler/req_files/request_test.req",isin_set, self.logger)
            return r.get(item['data'])

    def run(self):
        for item in self.pubsub.listen():
            self.work(item)


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler("/var/log/scheduler/scheduler.log")
    logger.addHandler(fh)
    # with DaemonContext(files_preserve=[fh.stream, ], ):
    with DaemonContext(files_preserve=[fh.stream, ], ):
        r = redis.Redis()
        client = Listener(r, [BASE_KEY], logger)
        client.start()
