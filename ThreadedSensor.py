# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 15:57:39 2018

@author: evin
@brief: Class provides the sensors having seperate threads running
"""

import threading

class ThreadedSensor():
    """
    Class provides the sensors having seperate threads running
    """
    
    def __init__(self, sensor, configSectionName):
        """
        Initialiazes the sensor 
        """
        self.sensor = sensor
        self.configSectionName = configSectionName
    
    def startListening(self):
        """
        Listening of the sensor from the socket is started on a thread
        """
        print self.configSectionName, " started listening"
        
        self.listeningSensorSocketThread = threading.Thread(target=self.sensor.listenSocketFromDotNET , args=())
        self.listeningSensorSocketThread.start()
        
    def stopListening(self):
        """
        Listening of the sensor is stopped
        """
        print self.configSectionName, " stopped listening"
        self.sensor.stop()