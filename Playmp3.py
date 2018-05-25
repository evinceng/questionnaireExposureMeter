# -*- coding: utf-8 -*-
"""
Created on Thu May 24 14:57:45 2018

@author: evin
"""
import os, sys 
from pygame import mixer # Load the required library
import datetime
  
def playSound(logger, fileName):
    """
    plays the sound file where the relative path to the file is inputted
    """
    APP_FOLDER = os.path.dirname(os.path.realpath(sys.argv[0]))
    filePath = os.path.join(APP_FOLDER, fileName)
    mixer.init()
    mixer.music.load(filePath)
    mixer.music.play()
    message = "Sound file named : %s played at %s" % (filePath, str(datetime.datetime.now()))
    logger.info(message)
