# -*- coding: utf-8 -*-
"""
Created on Tue May 22 11:55:46 2018

@author: evin
"""

import datetime
from apscheduler.schedulers.background import BackgroundScheduler
#import mp3play
import os, sys
import SchedulerHelperMethods
import logging
from pydispatch import dispatcher
from EventType import EventType

class Scheduler:
    """
    Scheduler class for executing predefined events to be excuted in exact times(timeActionUnit)
    or to be executed when certain events occur(eventActionUnit)
    """
    def __init__(self):
        #self.masterFrame = masterFrame
        self.initLogger()
        self.timeActionUnit = [
                               {"time":1, "function":self.printText, "args":[self.logger, "first"]},
                               #{"time":3, "function":SchedulerHelperMethods.playSound, "args":[self.logger, "media/first.mp3"]},
                               {"time":2, "function":SchedulerHelperMethods.playSoundAndOpenQuestionnaire, "args":["media/preQuestionnaire.ogg", "Pre Questionnaire", "questionnaire/pre_questions.csv"]},
                               #{"time":5, "function":SchedulerHelperMethods.playSound, "args":[self.logger, "media/second.mp3"]},
                               {"time":6, "function":self.printText, "args":[self.logger, "second"]}]
        
        #here is just usage info, relevant send script whereever your conditions are endured
        self.questionnaireActionUnit = [{"example":'dispatcher.send(EventType.PlayAudioAndOpenQuestSignal, EventType.PlayAudioAndOpenQuestSender, "media/postQuestionnaire.ogg", "Post Questionnaire", "questionnaire/post_questions.csv")',
                                         "example2":'dispatcher.send(EventType.OpenQuestSignal, EventType.OpenQuestSender, "Pre Questionnaire", "questionnaire/pre_questions.csv")'}] 

        
        self.eventActionUnit = [{"function":SchedulerHelperMethods.printMessege, "eventSignal":EventType.PrintMessageSignal, "eventSender":EventType.PrintMessageSender },
                                #{"function":self.printLeftEyeGaze, "eventSignal":EventType.EyeGazeGTTSignal, "eventSender":EventType.EyeGazeSender },
                                #{"function":self.playSound, "eventSignal":EventType.PlayAudioSignal, "eventSender":EventType.PlayAudioSender }
                                ]
        
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
        
        for action in self.timeActionUnit:
            actionTime = self.sessionStartTime + datetime.timedelta(seconds=action["time"])
            self.scheduler.add_job(action["function"], 'date', run_date=actionTime, args=action["args"])
        
        for action in self.eventActionUnit:
            #self.scheduler.add_job(action["function"], 'date', run_date=eventActionDummyTime, args=action["args"])
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
        
    def printText(self, logger, text):
        print "################################################################################"
        print "I am a text: ", text, datetime.datetime.now()
        print "################################################################################"
        logger.info("I am a text: %s %s" % (text, str(datetime.datetime.now())))
        
    def printLeftEyeGaze(self, sender, eyeGaze): #, 
        try:
            #SchedulerHelperMethods.printLeftGaze(eyeGaze)
            #self.scheduler.add_job("SchedulerHelperMethods:printLeftGaze", args=[eyeGaze]) #possible to give the function moduleName:functionName
            self.scheduler.add_job(SchedulerHelperMethods.printLeftGaze, args=[eyeGaze])
        except Exception,e:
            print e.message
            
    def playSound(self, sender, fileName):
        try:
            SchedulerHelperMethods.playSound(self.logger, fileName)
        except Exception,e:
            print e.message
            
    def openPopupWindow(self, sender, frame):
        try:
            SchedulerHelperMethods.popupWindow(frame)
        except Exception,e:
            print e.message
            
            