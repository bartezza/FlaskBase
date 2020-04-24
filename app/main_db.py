
import pymongo
import json
import logging

_log = logging.getLogger(__name__)


class MainDB:
    def __init__(self, url=None, config=None):
        if config is None:
            from .config import Config
            config = Config()
        if url is None:
            #with open(config.MONGO_SETTINGS_FILE, "r") as fp:
            #    settings_db = json.load(fp)

            settings_db = {
                "username": config.MONGO_USERNAME,
                "password": config.MONGO_PASSWORD,
                "host": config.MONGO_HOST
            }

            url = "mongodb://{}:{}@{}/{}".format(settings_db["username"], settings_db["password"], settings_db["host"],
                                                 config.MONGO_DB_NAME)
            # print(url)

            _log.debug("Connecting to mongo db at {}...".format(config.MONGO_HOST))
        else:
            _log.debug("Connecting to mongo db...")
        self.client = pymongo.MongoClient(url)
        self.client.server_info()

        self.db = self.client[config.MONGO_DB_NAME]

    def get_coll(self, name):
        return self.db[name]
