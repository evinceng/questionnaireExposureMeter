# -*- coding: utf-8 -*-
"""
Created on Tue May 22 11:55:46 2018

@author: evin
"""

import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import os, sys
import logging
from pydispatch import dispatcher
from EventType import EventType
from collections import OrderedDict
import ActionUnit

class Scheduler:
    """
    Scheduler class for executing predefined events to be excuted in exact times(timeActionUnit)
    or to be executed when certain events occur(eventActionUnit)
    """
    def __init__(self):
        #self.masterFrame = masterFrame
        self.initLogger()
        self.timeActionUnit = ActionUnit.timeActionUnit
        self.eventActionUnit = ActionUnit.eventActionUnit
        
        #self.readActionUnit("actionUnit.txt")
        self.scheduler = BackgroundScheduler()
        
    def initLogger(self):
        self.logger = logging.getLogger('apscheduler.executors.default')
        self.logger.setLevel(logging.INFO)  # DEBUG
        
    
    def addFileHandlerToLogger(self):
        APP_FOLDER = os.path.dirname(os.path.realpath(sys.argv[0]))
        fileName = "Scheduler_" +  self.sessionStartTime.strftime("%Y-%m-%d_%H%M%S") + ".log"
        filePath = os.path.join(APP_FOLDER, fileName)
        fileHandler = logging.FileHandler(filePath, "w")
        self.logger.addHandler(fileHandler)

    def setSessionStartTimeAndActionUnits(self, startTime):
        """
        The start time of the experiment is set and timeaction unit is added
        to the scheduler when the start button is pressed
        """
        self.sessionStartTime = startTime
        #this should be here so as to have sessioStartTime to name the log file
        self.addFileHandlerToLogger()
        
        #add jobs to scheduler at exact times starting from session start
        for action in self.timeActionUnit:
            actionTime = self.sessionStartTime + datetime.timedelta(seconds=action["time"])
            self.scheduler.add_job(action["function"], 'date', run_date=actionTime, args=action["args"])
        
        #connect eventsignals to defined methods. In methods you can either execute through scheduler.add_job(preffered) or call them directly.
        #see below printLeftEyeGaze method for how to use use
        for action in self.eventActionUnit:
            dispatcher.connect(action["function"], signal=action["eventSignal"], sender=action["eventSender"])
        
        self.logger.info("Session start time is " + str(self.sessionStartTime))
        print "################################################################################"        
        print "Session start time is ", self.sessionStartTime
        print "################################################################################"
        
        
    def startScheduler(self):
        """
        The scheduler is started
        """
        self.scheduler.start()
        self.logger.info("Scheduler started at " + str(datetime.datetime.now()))
                
    def stopScheduler(self):
        """
        The scheduler is stopped
        """
        self.scheduler.shutdown() 
        self.logger.info("Scheduler stopped at " + str(datetime.datetime.now()))
        handlers = self.logger.handlers[:]
        for handler in handlers:
            handler.close()
            self.logger.removeHandler(handler)
        logging.shutdown()
        
      
#    def printLeftEyeGaze(self, sender, eyeGaze):
#        try:
#            #SchedulerHelperMethods.printLeftGaze(eyeGaze)
#            #self.scheduler.add_job("SchedulerHelperMethods:printLeftGaze", args=[eyeGaze]) #possible to give the function moduleName:functionName
#            self.scheduler.add_job(SchedulerHelperMethods.printLeftGaze, args=[eyeGaze])
#        except Exception,e:
#            print e.message
        
        
#    def readActionUnit(self, fileName):
#        self.timeActionUnit=[]
#        self.eventActionUnit=[]
#        isTimeActionList = None
#        with open(fileName, "r") as file:
#            for line in file:
#                line = line.strip()
#                print line
#                print "!!!!!!!!!!!"
#                if line.startswith('#') or (not line):
#                    continue
#                elif line == "timeActionUnit:":
#                    isTimeActionList = True
#                elif line == "eventActionUnit:":
#                    isTimeActionList = False
#                else:
#                    dataDict = json.loads(line, object_pairs_hook=OrderedDict)
#                    if isTimeActionList:
#                        self.timeActionUnit.append(dataDict)
#                    else:
#                        self.eventActionUnit.append(dataDict)
#        print self.timeActionUnit
#        print "@@@@@@@@@@@"
#        print self.eventActionUnit
    
#    def printText(self, text):
#        print "################################################################################"
#        print "I am a text: ", text, datetime.datetime.now()
#        print "################################################################################"
#        self.logger.info("I am a text: %s %s" % (text, str(datetime.datetime.now())))

#            
#    def playSound(self, sender, fileName):
#        try:
#            SchedulerHelperMethods.playSound(self.logger, fileName)
#        except Exception,e:
#            print e.message
#            
#    def openPopupWindow(self, sender, frame):
#        try:
#            SchedulerHelperMethods.popupWindow(frame)
#        except Exception,e:
#            print e.message
            
            