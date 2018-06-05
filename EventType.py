# -*- coding: utf-8 -*-
"""
Created on Fri May 25 16:02:38 2018

@author: evin
"""

class EventType:
    """
    Both sender and signal event are defined here, please give distinct values to each item.
    Note that yuo can provide the eventtypes in string format also as seen below: "eyeGaze_greater_than_21"
    """
    PlayAudioSignal = 0
    PlayAudioSender = 1
    EyeGazeGTTSignal = 2#"eyeGaze_greater_than_21"
    EyeGazeSender = 3 #"sensor_eyeGaze_sender"
    OpenQuestSignal = 4
    OpenQuestSender = 5
    PlayAudioAndOpenQuestSignal = 6
    PlayAudioAndOpenQuestSender = 7
    PrintMessageSignal = 8
    PrintMessageSender = 9