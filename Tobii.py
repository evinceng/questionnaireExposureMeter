# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 12:50:15 2018

@author: evin
@brief: Specific class for tobi eye  tracker sensor, provides shapeDataForDB implementation
"""

import Sensor
import json
import re
from collections import OrderedDict
import flattenDict as ft
from datetime import datetime

class Tobii(Sensor.Sensor):
    """
    Specific class for tobi eye  tracker sensor, provides shapeDataForDB implementation
    """
    
    def shapeDataForDB(self, data):
        omitBeginLen = len('{"tobiiEyeTracker":')
        data = data[omitBeginLen:-1]
        
        #convert double values from string to real double values with "."
        data = re.sub(r'\"(\-??\d+).(\d+)\"', r'\1.\2', data) # "-16.7315728269386" -> -16.7315728269386
        
        #convert "0" or any integer value to numeric value
        data = re.sub(r'\"(\d+)\"', r'\1', data) # "0" -> 0
        
        #load the data to an ordered dictioanry
        jsonData = json.loads(data, object_pairs_hook=OrderedDict)
        
        #flatten the data "leftPos":{"x":-0.228793755914194, to leftPos:x': -0.228793755914194
        jsonData = ft.flattenDict(jsonData)
        
        dateTime = jsonData["timeStamp"]
        
#        print "dateTime is #################"
#        print dateTime
#        print "dateTime is #################"
        
        #parse the timeStamp string to python datetime obj
        try:
            parsedDT = datetime.strptime(dateTime, "%d.%m.%Y %H:%M:%S.%f")
        except ValueError, e:
            print '"%s" is an invalid date' % dateTime
        
        jsonData["timeStamp"] = parsedDT
        
#        print "timestamp is #################"
#        print jsonData["timeStamp"]
#        print "timestamp is #################"
        
        return jsonData