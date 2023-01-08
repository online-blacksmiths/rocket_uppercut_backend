import logging
from pymongo.monitoring import (
    CommandListener,
    register
)
from mongoengine import connect

from common.config.settings import conf


log = logging.getLogger('pymongo')
log.setLevel(logging.DEBUG)


class MongoLogger(CommandListener):
    def started(self, event):
        log.debug("Command {0.command_name} with request id "
                  "{0.request_id} started on server "
                  "{0.connection_id}".format(event))

    def succeeded(self, event):
        log.debug("Command {0.command_name} with request id "
                  "{0.request_id} on server {0.connection_id} "
                  "succeeded in {0.duration_micros} "
                  "microseconds".format(event))

    def failed(self, event):
        log.debug("Command {0.command_name} with request id "
                  "{0.request_id} on server {0.connection_id} "
                  "failed in {0.duration_micros} "
                  "microseconds".format(event))


def mongodb():
    if conf().DEBUG:
        register(MongoLogger())

    if conf().TEST_MODE:
        connect('mongoenginetest', host='mongomock://localhost')
    else:
        connect(host=conf().MONGO_DB_URL)
