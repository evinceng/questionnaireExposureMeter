# -*- coding: utf-8 -*-
"""
Created on Thu May 24 14:57:45 2018

@author: evin
"""
import os, sys 
import datetime
from pydispatch import dispatcher
from EventType import EventType

def getAbsPath(fileName):
    """
    returns absolute path of a given fileName
    """
    APP_FOLDER = os.path.dirname(os.path.realpath(sys.argv[0]))
    filePath = os.path.join(APP_FOLDER, fileName)
    return filePath


from pygame import mixer # Load the required library

def playSound(logger, fileName, signal=None, sender=None, args=None):
    """
    plays the sound file where the relative path to the file is inputted
    """
    filePath = getAbsPath(fileName)
    mixer.init()
    mixer.music.load(filePath)
    mixer.music.play()
    message = "Sound file named : %s played at %s" % (filePath, str(datetime.datetime.now()))
    logger.info(message)

def printLeftGaze(eyeGaze): #eyeGaze
    print "Left eye gaze value is ", eyeGaze
    print "::::::::::::::::::::::::::::::::::"

import Questionnaire
def runQuestionnaire(masterFrame, title, questionFileName): #logger, 
    """
    runs the questionnaire with params 
    """
    filePath = getAbsPath(questionFileName)
    questionnaire = Questionnaire.Questionnaire(masterFrame, title, filePath)
    questionnaire.run()
#    message = "Questionnaire : %s displayed at %s" % (filePath, str(datetime.datetime.now()))
#    logger.info(message)
    
import tkinter as Tk
def popupWindow(frame):
    counter = 1
    t = Tk.Toplevel(frame)
    t.wm_title("Window #%s" % counter)
    l = Tk.Label(t, text="This is window #%s" % counter)
    l.pack(side="top", fill="both", expand=True, padx=100, pady=100)