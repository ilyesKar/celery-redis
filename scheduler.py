import ftplib
import logging
import os

import redis, threading
import json
from daemon import *

BASE_KEY = '__key*__:*'
def ftp_test(filename):

    filename = "MyFile.py"
    ftp = ftplib.FTP("192.168.0.103")
    ftp.login("Ilyes", "password209#")
    ftp.cwd("/req")
    # os.chdir(r"/home/ilyes/schedelor/")
    ftp.storlines("STOR " + "ilyes.req", open("/home/ilyes/schedelor/bond_test_res.req", 'rb'))

def create_req(isin_set, logger):
    logger.debug("create start")
    try:
        bond_req = open("/home/ilyes/schedelor/bond_test.req", "r")
    except:
        logger.debug("create error 1")
    try:
        bond_req_res = open("/home/ilyes/schedelor/bond_test_res.req", "w")

    except:
        logger.debug("create error 2")
    find = False
    i = 0

    for  line in bond_req.read().split('\n'):
        bond_req_res.writelines(line + "\n")
        if line == "START-OF-DATA":
            for data in  isin_set:
                bond_req_res.writelines(data+" Corp\n")
    bond_req_res.close()
    bond_req.close()
    ftp_test('eee')
    logger.debug("create end")

class Listener(threading.Thread):
    def __init__(self, r, channels, logger):
        threading.Thread.__init__(self)
        self.redis = r
        self.pubsub = self.redis.pubsub()
        self.pubsub.psubscribe(channels)
        self.logger = logger

    def work(self, item):
        if item['channel'] == b'__keyevent@0__:set' and item['data'].decode('utf-8')[:11]== 'ilyes:json:':
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
            create_req(isin_set, self.logger)
            return r.get(item['data'])

    def run(self):
        for item in self.pubsub.listen():
                self.work(item)



if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler("./schedul.log")
    logger.addHandler(fh)
    # with DaemonContext(files_preserve=[fh.stream, ], ):
    r = redis.Redis()
    client = Listener(r, [BASE_KEY], logger)
    client.start()
