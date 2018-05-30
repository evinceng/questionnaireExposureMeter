# -*- coding: utf-8 -*-
"""
Created on Wed Apr 04 13:13:48 2018

@author: evin
@brief: Class establishing communication between user interface(view) and model.
       (Controller of MVC)
"""
import Model
import View
import Tkinter as Tk
from tkinter import messagebox
import bottle
import EnableCors
import threading
import StoppableWSGIRefServer
import config
from pydispatch import dispatcher
import SchedulerHelperMethods
from EventType import EventType

class Controller():
    """Class establishing communication between user interface(view) and model.
       (Controller of MVC)
    """

    def __init__(self):
        """
        Initializes the bottle server, creates Model and View part of the MVC,
        and binds the start and stop button
        """
        self.initializeBottleServer()
        self.root = Tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.onClosing)
        self.model=Model.Model()
        self.view=View.View(self.root)
        self.view.sidePanel.startButton.bind("<Button>",self.start)
        self.view.sidePanel.stopButton.bind("<Button>",self.stop)
        self.view.mainPanel.userNameVar.trace("w", self.updateStartButtonState)
        self.root.after(2000, self.root.focus_force)
        #connects OpenQuestSignal to openQuestionnaire method through dispatcher
        dispatcher.connect(self.openQuestionnaire, signal=EventType.OpenQuestSignal, sender=EventType.OpenQuestSender)
        #connects PlayAudioAndOpenQuestSignal to playAudioAndOpenQuestionnaire method through dispatcher
        dispatcher.connect(self.playAudioAndOpenQuestionnaire, signal=EventType.PlayAudioAndOpenQuestSignal, sender=EventType.PlayAudioAndOpenQuestSender)
        #since the questionnaire can not be opened form dispatcher(another thread) '<<pingOpenQuestionnaire>>' is binded to self.pingOpenQuestionnaire method
        self.root.bind('<<pingOpenQuestionnaire>>', self.pingOpenQuestionnaire)
        #since the questionnaire can not be opened form dispatcher(another thread) '<<pingPlayAudioAndOpenQuestionnaire>>' is binded to self.pingPlayAudioAndOpenQuestionnaire method
        self.root.bind('<<pingPlayAudioAndOpenQuestionnaire>>', self.pingPlayAudioAndOpenQuestionnaire)
        
        #first benchmark commented out
#        self.view.mainPanel.slider.bind("<B1-Motion>", self.calculateVal)
#        self.view.mainPanel.progressbar["maximum"] = self.model.progressBarMaxVal
        
    def run(self):
        """
        starts the user interface
        """
        self.root.title("MVC")
        self.root.deiconify()
        self.root.mainloop()
        
    def start(self,event):
        """
        Orginizes the start&stop buttons state and signals the model to start listening the sensors
        """
        #since bind does not work like command you have to check the state
        if self.view.sidePanel.startButton["state"] == "normal":
            self.view.sidePanel.startButton.config(state="disabled")
            self.view.sidePanel.stopButton.config(state="normal")
            self.model.start(self.view.mainPanel.userNameVar.get())
        #first benchmark commented out
#        self.clearSlider()
        
    def stop(self,event):
        """
        Changes the start&stop buttons state and signals the model to stop listening the sensors
        """
        #since bind does not work like command you have to check the state
        if self.view.sidePanel.stopButton["state"] == "normal":
            if self.view.mainPanel.userNameVar.get().strip():
                self.view.sidePanel.startButton.config(state="normal")
                
            self.view.sidePanel.stopButton.config(state="disabled")
            self.model.stop()
            #first benchmark commented out
#          self.clearSlider()
        
        
    def onClosing(self):
        """
        A message box is showed to the user before closing the window and model is signaled
        to stop listening the sensors and bottle server is stooped and window is destroyed
        """
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            #if the button stop is already pushed don't call stop method again
            state = str(self.view.sidePanel.stopButton["state"])
            if state == "normal":
                self.model.stop()
            self.server.stop()
            self.root.destroy()
            
    def initializeBottleServer(self):
        """
        Starts the bottle server
        """
        app = bottle.app()
        app.install(EnableCors.EnableCors())
        
        __serverHostIP = config.getConfig().get("SERVER", "IP")
        __serverHostPort = config.getConfig().getint("SERVER", "Port")
        print "Starting http server on http://",__serverHostIP,':',__serverHostPort
        
        self.server = StoppableWSGIRefServer.StoppableWSGIRefServer(host=__serverHostIP, port=__serverHostPort)
    
        self.appThread = threading.Thread(target=app.run, kwargs=dict(server=self.server))
        self.appThread.daemon = True
        self.appThread.start()
    
    def updateStartButtonState(self, *_):
        """
        The start button is enabled if only username is provided
        """
        if (self.view.sidePanel.stopButton["state"] =="disabled" and self.view.mainPanel.userNameVar.get()):
            self.view.sidePanel.startButton.config(state="normal")
        else:
            self.view.sidePanel.startButton.config(state="disabled")
    
    def openQuestionnaire(self, questTitle, questFileName):
        """
        Receives openquestionnaire event and generates ping event for tkinter to be able to pop up questionnaire window
        """
        self.questTitle = questTitle
        self.questFileName = questFileName
        self.root.event_generate('<<pingOpenQuestionnaire>>', when='tail')
        
    def pingOpenQuestionnaire(self, event):
        """
        After OpenQuestSignal received and ping event generated, event is catched here and opened as a pop up window
        """
        SchedulerHelperMethods.openQuestionnaire(self.root, self.questTitle, self.questFileName)
        
    def playAudioAndOpenQuestionnaire(self, audioFileName, questTitlePAO, questFileNamePAO):
        """
        Receives playAudioAndopenquestionnaire event and generates ping event for playing sound and tkinter to be able to  pop up questionnaire window
        """
        self.questTitlePAO = questTitlePAO
        self.questFileNamePAO = questFileNamePAO
        self.audioFileName = audioFileName
        self.root.event_generate('<<pingPlayAudioAndOpenQuestionnaire>>', when='tail')
        
    def pingPlayAudioAndOpenQuestionnaire(self, event):
        """
        After PlaySoundAndOpenQuestSignal received and ping event generated, event is catched here SchedulerHelperMethods method is called
        """
        SchedulerHelperMethods.playSoundAndOpenQuestionnaire(self.audioFileName, self.questTitlePAO, self.questFileNamePAO)
        
#first benchmark commented out
#    def calculateVal(self,event):
#        currentVal = self.view.mainPanel.slider.get()
#        modelVal = self.model.start(currentVal)
#        self.view.mainPanel.progressbar["value"] = modelVal
#        
#    def clearSlider(self):
#        self.view.mainPanel.progressbar["value"] = self.model.progressBarMinVal
        
        
  