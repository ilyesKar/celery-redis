#!/usr/bin/python3
import os

import redis
from celery import *
from pyDes import *
DES_KEY = "-ySh}9/x"
BASE_KEY = 'ilyes:json:'


def file_encrypt(input_file, output_file, encryption_key):
    f = open(input_file, "rb+")
    d = f.read()
    f.close()
    k = des(encryption_key)

    d = k.encrypt(d, " ")
    f = open(output_file, "wb+")
    f.write(d)
    f.close()


def file_decrypt(input_file, output_file, encryption_key):
    f = open(input_file, "rb+")
    d = f.read()
    f.close()
    k = des(encryption_key)
    d = k.decrypt(d, " ")
    f = open(output_file, "wb+")
    f.write(d)
    f.close()


app = Celery('watchdog_functions', broker='redis://localhost:6379/0')


@task
def add_key_to_redis(file_name, file_content):
    # r = redis.StrictRedis()
    r_server = redis.Redis()  # '192.168.0.154') #this line creates a new Redis object and
    r_server.set(BASE_KEY + file_name, file_content)
    r_server.publish(BASE_KEY + file_name, file_content)
    # test = r.set(BASE_KEY + file_name, file_content)
    print(file_content)


@task
def update_key_in_redis(file_name, file_content):
    print(file_name)
    print(file_content)
    add_key_to_redis(file_name, file_content)


@task
def delete_key_from_redis(file_name):
    r = redis.StrictRedis()
    r.delete(BASE_KEY + file_name)


def register_pid(process_name):
    file = open("/var/run/" + process_name + ".pid", 'w')
    file.write(str(os.getpid()))
    file.close()
    return os.getpid()
