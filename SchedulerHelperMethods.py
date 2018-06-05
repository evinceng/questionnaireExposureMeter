# -*- coding: utf-8 -*-
"""
Created on Thu May 24 14:57:45 2018

@author: evin
"""
import os 
import datetime
from pydispatch import dispatcher
from EventType import EventType
import logging 
import Questionnaire
from pygame import mixer # Load the required library

def getAbsPath(fileName):
    """
    returns absolute path of a given fileName
    """
    APP_FOLDER = os.getcwd()#path.dirname(os.path.realpath(sys.argv[0]))
    filePath = os.path.join(APP_FOLDER, fileName)
    return filePath

def playSound(fileName):
    """
    plays the sound file where the relative path to the file is inputted
    """
    filePath = getAbsPath(fileName)
    mixer.init()
    mixer.music.load(filePath)
    mixer.music.play()
    logMessage("Sound file named : %s played at %s" % (filePath, str(datetime.datetime.now())))

def printMessage(message):
    print "::::::::::::::::::::::::::::::::::"
    print "Message is ", message
    print "::::::::::::::::::::::::::::::::::"

def openQuestionnaire(masterFrame, title, questType, questionFileName):
    """
    open the questionnaire window with params 
    """
    filePath = getAbsPath(questionFileName)
    questionnaire = Questionnaire.Questionnaire(masterFrame, title, questType, filePath)
    questionnaire.run()
    logMessage("Questionnaire file named : %s opened at %s" % (questionFileName, str(datetime.datetime.now())))
        
def playSoundAndOpenQuestionnaire(soundFileName, questTitle, questType, questFileName):
    """
    Sound is played and dispatcher send the signal to open the questionnaire
    """
    playSound(soundFileName)
    #move this line to whenever you want to open popup window
    dispatcher.send(EventType.OpenQuestSignal, EventType.OpenQuestSender, questTitle, questType, questFileName)
    logMessage("Open questionnaire  %s event sent: %s" % (questFileName, str(datetime.datetime.now())))

def logMessage(message):
    """
    Appends the message to the scheduler default logger
    """
    logger = logging.getLogger('apscheduler.executors.default')
    if logger:
        logger.info(message)
        
        
#import tkinter as Tk
#def popupWindow(frame):
#    """
#    Just for trying to open a simple popupwindow
#    """
#    counter = 1
#    t = Tk.Toplevel(frame)
#    t.wm_title("Window #%s" % counter)
#    l = Tk.Label(t, text="This is window #%s" % counter)
#    l.pack(side="top", fill="both", expand=True, padx=100, pady=100)