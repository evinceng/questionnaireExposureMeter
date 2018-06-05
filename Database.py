# -*- coding: utf-8 -*-
"""
Created on Thu May 31 13:49:16 2018

@author: evin
"""
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import config
import sys
from datetime import datetime
from dateutil.tz import tzlocal
from collections import OrderedDict

"""
user properties dictionary like username, sessionID, start time, timezone etc..
"""
userPropsDict = {}
    
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


def createUserPropsDict(userName, sessionStartTime):
    """
    Creates the user info dictionary
    """
    userPropsArr = []
    userPropsArr.append(("userName", userName))
    userPropsArr.append(("sessionStartTime", sessionStartTime))

#   from tzlocal import get_localzone
#   local_tz_name = get_localzone()
        
    local_tz_name = datetime.now(tzlocal()).tzname()
    userPropsArr.append(("timeZoneName", local_tz_name))
        
    userPropsArr.append(("sessionID", userName + str(sessionStartTime)))
        
    userPropsArr.append(("relativeTime", 0))
        
    return OrderedDict(userPropsArr)

def saveToDB(configSectionName, dataDict, collectionName="DBCollectionName"):
    """
    saves data, by calculating relative time to session start time, to the collection 
    in configSectionName section in the config.ini file.
    The collection name will be "DBCollectionName" by default if not provided
    """
    if not userPropsDict:
        raise Exception("Please set username, sessionstarttime and userpropsdict in Model.py")
    #calculate relative time since the start of the session
    diff = dataDict["timeStamp"] - userPropsDict["sessionStartTime"]
    userPropsDict["relativeTime"] = diff.total_seconds()
        
    #add user nd session related info infront of the sensor info
    concatedDict = OrderedDict(list(userPropsDict.items()) + list(dataDict.items()))
        
    collection = dbhost[config.getConfig().get(configSectionName, collectionName)]
    #save to DB
    collection.insert_one(concatedDict)





   
