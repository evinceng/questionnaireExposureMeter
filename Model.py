# -*- coding: utf-8 -*-
"""
Created on Wed Apr 04 13:13:48 2018

@author: evin
"""
import ThreadedSensor
import bottle
import Tobii
import config
from datetime import datetime

class Model():
    """ Class including the main operations of the app.
        (Model of MVC)
    """
    
    def __init__(self):
        self.serverHostIP = config.getConfig().get("SERVER", "IP")
        self.serverHostPort = config.getConfig().getint("SERVER", "Port")
        self.initTobiiEyeTracker()

    def initTobiiEyeTracker(self):
        __tobiiConfigSection = "TOBII"
        self.tobiiSensor = Tobii.Tobii(__tobiiConfigSection)
        self.tobiiEyeTracker = ThreadedSensor.ThreadedSensor(self.tobiiSensor, __tobiiConfigSection)
        
        __tobiiEyeTrackerServerHostRoute = config.getConfig().get(__tobiiConfigSection, "HostRoute")
        
        print "Starting http server on http://",self.serverHostIP,':',self.serverHostPort, __tobiiEyeTrackerServerHostRoute
        bottle.route(__tobiiEyeTrackerServerHostRoute)(self.tobiiEyeTracker.sensor.respondTracker)
        
    def start(self):
        startTime = datetime.now()
        #start time should be set before starting listening the port
        self.tobiiSensor.setSessionStartTime(startTime)
        self.tobiiEyeTracker.startListening()
    
    def stop(self):
        self.tobiiEyeTracker.stopListening()
          
#first benchmark commented out
#    progressBarMaxVal = 2
#    """Progress Bar's max value """
#    progressBarMinVal = 0
#    """Progress Bar's min value """
    
#    def start(self, slideVal):
#        result = 2* slideVal**2
#        print slideVal
#        print result
#        return result
         