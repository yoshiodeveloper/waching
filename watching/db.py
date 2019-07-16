# -*- encoding: utf-8 -*-

import pymongo

from watching.config import (MONGO_DB, MONGO_URI)


def get_db():
    """ Retorna um client do MongoDB. """
    client = pymongo.MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    return db
