# -*- coding: utf-8 -*-
"""
Created on Thu May 31 13:49:16 2018

@author: evin
"""
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import config
import sys

"""
Initializes mongoDB connection
"""
dbSectionName = "MONGODB"
__host = config.getConfig().get(dbSectionName, "Host")
__port = config.getConfig().getint(dbSectionName, "Port")
try:
    client = MongoClient(host=__host, port=__port)
except ConnectionFailure, e:
    sys.stderr.write("Could not connect to MongoDB: %s" % e)
    sys.exit(1)
    
dbhost = client[config.getConfig().get(dbSectionName, "DBName")]
#self.userCollection = dbhost[config.getConfig().get(dbSectionName, "UserCollection")]
#self.sensorCollection = dbhost[config.getConfig().get(self.configSectionName, "DBCollectionName")]
    
def saveToDB(configSectionName, data):
    """
    saves data to the collection in configSectionName section in the config.ini file.
    """
    collection = dbhost[config.getConfig().get(configSectionName, "DBCollectionName")]
    #save to DB
    collection.insert_one(data)