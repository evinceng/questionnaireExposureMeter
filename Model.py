# -*- coding: utf-8 -*-
"""
Created on Wed Apr 04 13:13:48 2018

@author: evin
@brief: Class including the main data and their operations of the multimedia exposure meter app
        (Model of MVC)
"""
import ThreadedSensor
import bottle
import Tobii
import config
from datetime import datetime

class Model():
    """ Class including the main data and their operations of the multimedia exposure meter app
        (Model of MVC)
    """
    
    def __init__(self):
        """
        Initializes serverhost ip and port numbers & the sensors
        """
        self.serverHostIP = config.getConfig().get("SERVER", "IP")
        self.serverHostPort = config.getConfig().getint("SERVER", "Port")
        self.initTobiiEyeTracker()
        ################################################################################
        #initialize scheduler here by calling initScheduler method that will do the job
        ################################################################################
     
    def initScheduler(self):
        """
        Create a Scheduler and ThreadedScheduler
        (this will run the Sceheduler class in a thread like ThreadedSensor for tobii) 
        class like in initTobiiEyeTracker method
        """
        pass
    
    def initTobiiEyeTracker(self):
        """
        Initializes TOBII eyetracker sensor and starts the bottle application        
        """
        __tobiiConfigSection = "TOBII"
        self.tobiiSensor = Tobii.Tobii(__tobiiConfigSection)
        self.tobiiEyeTracker = ThreadedSensor.ThreadedSensor(self.tobiiSensor, __tobiiConfigSection)
        
        __tobiiEyeTrackerServerHostRoute = config.getConfig().get(__tobiiConfigSection, "HostRoute")
        
        print "Starting http server on http://",self.serverHostIP,':',self.serverHostPort, __tobiiEyeTrackerServerHostRoute
        bottle.route(__tobiiEyeTrackerServerHostRoute)(self.tobiiEyeTracker.sensor.respondTracker)
        
    def start(self):
        """
        Session start time is set and the sensors are started for listening the ports
        """
        startTime = datetime.now()
        #start time should be set before starting listening the port
        self.tobiiSensor.setSessionStartTime(startTime)
        self.tobiiEyeTracker.startListening()
        ################################################################################
        #Start the scheduler here
        ################################################################################
        
    
    def stop(self):
        """
        Sensors are stopped to listening the ports
        """
        self.tobiiEyeTracker.stopListening()
        ################################################################################
        #Stop the scheduler here
        ################################################################################
          
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
         