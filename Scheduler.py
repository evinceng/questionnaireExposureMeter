# -*- coding: utf-8 -*-
"""
Created on Tue May 22 11:55:46 2018

@author: evin
"""

import datetime
from apscheduler.schedulers.background import BackgroundScheduler
#import mp3play
import os, sys
import Playmp3
import logging

class Scheduler:
    """
    Scheduler class for executing predefined events to be excuted in exact times(timeActionUnit)
    or to be executed when certain events occur(eventActionUnit)
    """
    def __init__(self):
        self.initLogger()
        self.timeActionUnit = [{"time":1, "function":Playmp3.playSound, "args":[self.logger, "media/first.mp3"]},
                               {"time":2, "function":self.printText, "args":[self.logger, "first"]},
                               {"time":4, "function":Playmp3.playSound, "args":[self.logger, "media/second.mp3"]},
              {"time":6, "function":self.printText, "args":[self.logger, "second"]}]
        
#        eventActionUnit = [{"event":Event.PLAY_AUDIO, "function":playAudio, "args":["media/first.mp3"]},
##              {"event":Event.OPEN_QUESTIONNAIRE, "function":openQuestionnaire, "args":["OpeningQuestionnaire"]},
##              {"event":Event.CLOSE_QUESTIONNAIRE, "function":closeQuestionnaire, "args":["OpeningQuestionnaire"]}
#              ]
        self.scheduler = BackgroundScheduler()       
    
    def initLogger(self):
        self.logger = logging.getLogger('apscheduler.executors.default')
        self.logger.setLevel(logging.INFO)  # DEBUG
        
    
    def addFileHandlerToLogger(self):
        APP_FOLDER = os.path.dirname(os.path.realpath(sys.argv[0]))
        #fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
        fileName = "Scheduler_" +  self.sessionStartTime.strftime('%Y-%m-%d_%H%M%S') + ".log"
        filePath = os.path.join(APP_FOLDER, fileName)
        fileHandler = logging.FileHandler(filePath, "w")#logging.StreamHandler()
        #fileHandler.setFormatter(fmt)
        self.logger.addHandler(fileHandler)

    def setSessionStartTimeAndActionUnits(self, startTime):
        """
        The start time of the experiment is set and timeaction unit is added
        to the scheduler when the start button is pressed
        """
        self.sessionStartTime = startTime
        #this should be here so as to have sessioStartTime to naem the log file
        self.addFileHandlerToLogger()
        
        for action in self.timeActionUnit:
            actionTime = self.sessionStartTime + datetime.timedelta(seconds=action["time"])
            self.scheduler.add_job(action["function"], 'date', run_date=actionTime, args=action["args"])
        
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
        self.logger.info("Scheduler stopped at ", datetime.datetime.now())
        
    def printText(self, logger, text):
        print "################################################################################"
        print "I am a text: ", text, datetime.datetime.now()
        print "################################################################################"
        logger.info("I am a text: %s %s" % (text, str(datetime.datetime.now())))



