import logging
import sys
import time
from daemon import DaemonContext
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from celery import *
from watchdog_functions import *


BASE_KEY = 'watchdog:json:'


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, logger):
        self.logger = logger
        process_name = "fix_watchdog"
        register_pid(process_name)
        # self.q = Queue(connection=redis.Redis())

    def on_modified(self, event):
        if event.src_path[-5:] == ".json":
            self.logger.debug("modified = " + str(event.src_path))

            update_key_in_redis.delay('modification', open(event.src_path).read())

    def on_created(self, event):
        if event.src_path[-5:] == ".json":
            self.logger.debug("created = " + str(event.src_path))
            add_key_to_redis.delay('creation',open(event.src_path).read())

    def on_deleted(self, event):
        if event.src_path[-5:] == ".json":
            self.logger.debug("deleted = " + str(event.src_path))
            delete_key_from_redis.delay(open(event.src_path).read())


def do_launch_main_program(logger):
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = FileChangeHandler(logger)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def run():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler("./fix_watchdog.log")
    logger.addHandler(fh)
    with DaemonContext(files_preserve=[fh.stream, ], ):
        do_launch_main_program(logger)


if __name__ == "__main__":
    run()
