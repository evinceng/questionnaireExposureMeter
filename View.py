# -*- coding: utf-8 -*-
"""
Created on Wed Apr 04 13:12:21 2018

@author: evin
@brief: The user interface(GUI) of multimedia exposure meter app.
        (View of MVC)
"""

import Tkinter as Tk

class View():
    """ The user interface(GUI) of multimedia exposure meter app.
        (View of MVC)
    """
    
    def __init__(self, master):
        self.frame = Tk.Frame(master)
        self.frame.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)
        #first benchmark commented out
#        self.mainPanel = MainPanel(master)
        self.sidePanel=SidePanel(master)
        
#first benchmark commented out
#class MainPanel():
#    """Class including the benchmark visuals: graphs, sliders etc.
#    
#    """
#    def __init__(self, root):
#        self.frame2 = Tk.Frame(root)
#        self.frame2.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)
#        self.progressbar = ttk.Progressbar(self.frame2, length=200,
#                                           mode="determinate")
#        self.progressbar.pack()
#        self.slider = Tk.Scale(self.frame2, from_ = 0, to_ = 1,
#                               orient=Tk.HORIZONTAL, resolution = 0.001)
#        
#        self.slider.pack()        
        
class SidePanel():
    """Class managing the start and stop buttons.
    
    """
    def __init__(self, root):
        self.frame3 = Tk.Frame(root)
        self.frame3.pack(side=Tk.RIGHT, fill=Tk.BOTH, expand=1)
        self.startButton = Tk.Button(self.frame3, text="Start")
        self.startButton.pack(side="top",fill=Tk.BOTH)
        self.stopButton = Tk.Button(self.frame3, text="Stop", state="disabled")
        self.stopButton.pack(side="top",fill=Tk.BOTH)
