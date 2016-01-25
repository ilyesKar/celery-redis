import redis
from celery import *

BASE_KEY = 'ilyes:json:'

app = Celery('watchdog_functions', broker='redis://localhost:6379/0')


@task
def add_key_to_redis(file_name, file_content):
    #r = redis.StrictRedis()
    r_server = redis.Redis()#'192.168.0.154') #this line creates a new Redis object and
    r_server.set(BASE_KEY + file_name, file_content)
    r_server.publish(BASE_KEY + file_name, file_content)
    #test = r.set(BASE_KEY + file_name, file_content)
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



