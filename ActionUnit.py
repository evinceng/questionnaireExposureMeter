# -*- coding: utf-8 -*-
"""
Created on Thu May 31 09:13:52 2018

@author: evin
"""
import SchedulerHelperMethods
from EventType import EventType
from QuestionnaireType import QuestionnaireType

"""
Action units that will be executed throught the exposure meter session
"""
        
"""  
The actions that will be executed at exact times after session is started(start button pressed)
time is in seconds, provide the function as ModuleName.methodName, arguments are an array 
Note that these methods will be run through the scheduler, so you will have Schedular log file after a session,
There you can track which actions took place in which time
Note that sound files are located in "media" folder and questionnaire files are located in "questionnaire" folder
"""  
timeActionUnit = [
        {"time":1, "function":SchedulerHelperMethods.printMessage, "args":["first"]},
        #{"time":1, "function":self.printText, "args":[self.logger, "first"]},
        #{"time":3, "function":SchedulerHelperMethods.playSound, "args":[self.logger, "media/first.mp3"]},
        {"time":0.5, "function":SchedulerHelperMethods.playSoundAndOpenQuestionnaire, "args":["media/preQuestionnaire.ogg", "Pre Questionnaire", QuestionnaireType.PreQuest,"questionnaire/pre_questions.csv"]},
        #{"time":5, "function":SchedulerHelperMethods.playSound, "args":[self.logger, "media/second.mp3"]},
        {"time":3, "function":SchedulerHelperMethods.printMessage, "args":["second"]},
        ]
        
"""      
The actions that will be executed when specific event occurs.
You have to add new types to EventType if needed(You have to provide both signal and sender with distinct values.)
provide the function as ModuleName.methodName
--If you create the method in "Scheduler.py" then you can execute through schedular by adding a new job(scheduler.add_job) with no time provided,
this means that the method will be executed immediately (please refer to printLeftEyeGaze method within commented code for sample usage)
--If not: when you have a standalone method or you don't want to execute it through scheduler put it in SchedulerHelperMethods.py
"""
eventActionUnit = [
        {"function":SchedulerHelperMethods.printMessage, "eventSignal":EventType.PrintMessageSignal, "eventSender":EventType.PrintMessageSender },
        #{"function":self.printLeftEyeGaze, "eventSignal":EventType.EyeGazeGTTSignal, "eventSender":EventType.EyeGazeSender },
        #{"function":self.playSound, "eventSignal":EventType.PlayAudioSignal, "eventSender":EventType.PlayAudioSender }
        ]

"""
This is used only for questionnaires
And it is just usage info, you have to put relevant dispatcher.send script (example shown below) whereever your conditions are ensured (think it like creating an event with arguments)
"""
questionnaireActionUnit = [
        {"example":'dispatcher.send(EventType.PlayAudioAndOpenQuestSignal, EventType.PlayAudioAndOpenQuestSender, "media/postQuestionnaire.ogg", "Post Questionnaire", QuestionnaireType.PostQuest, "questionnaire/post_questions.csv")'},
         {"example2":'dispatcher.send(EventType.OpenQuestSignal, EventType.OpenQuestSender, "Pre Questionnaire", "questionnaire/pre_questions.csv")'}] 


    
#       self.timeActionUnit = [
#                               {"time":1, "module":"SchedulerHelperMethods",  "function":"printMessage", "args":["first"]},
#                               #{"time":1, "function":self.printText, "args":[self.logger, "first"]},
#                               #{"time":3, "function":SchedulerHelperMethods.playSound, "args":[self.logger, "media/first.mp3"]},
#                               {"time":2, "module":"SchedulerHelperMethods", "function":"playSoundAndOpenQuestionnaire", "args":["media/preQuestionnaire.ogg", "Pre Questionnaire", "questionnaire/pre_questions.csv"]},
#                               #{"time":5, "function":SchedulerHelperMethods.playSound, "args":[self.logger, "media/second.mp3"]},
#                               {"time":6, "module":"SchedulerHelperMethods",  "function":"printMessage", "args":["second"]}]
 