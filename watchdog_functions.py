#!/usr/bin/python3
import os
import subprocess
import redis
from celery import *

DES_KEY = "-ySh}9/x"
BASE_KEY = 'nca_scheduler:json:'


def file_encrypt(input_file, output_file, encryption_key):
    FNULL = open(os.devnull, 'w')  # use this if you want to suppress output to stdout from the subprocess
    args = "opt/scheduler/tools/des-amd64 -E -u -k " + encryption_key + ' ' + input_file + output_file
    subprocess.call(args, stdout=FNULL, stderr=FNULL, shell=True)


def file_decrypt(input_file, output_file, encryption_key):
    FNULL = open(os.devnull, 'w')  # use this if you want to suppress output to stdout from the subprocess
    args = "opt/scheduler/tools/des-amd64 -D -u -k " + encryption_key + ' ' + input_file + output_file
    subprocess.call(args, stdout=FNULL, stderr=FNULL, shell=True)


app = Celery('watchdog_functions', broker='redis://localhost:6379/0')


@task
def add_key_to_redis(file_name, file_content):
    # r = redis.StrictRedis()
    r_server = redis.Redis()  # '192.168.0.154') #this line creates a new Redis object and
    r_server.set(BASE_KEY + file_name, file_content)
    r_server.publish(BASE_KEY + file_name, file_content)
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
