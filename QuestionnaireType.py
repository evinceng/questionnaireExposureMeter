# -*- coding: utf-8 -*-
"""
Created on Fri Jun 01 09:48:12 2018

@author: evin
"""

class QuestionnaireType:
    """
    The type of questionnaire that will also be saved to DB to differentiate 
    between pre and post questionnaire since both have the same sessionIDs
    """
    PreQuest = "pre"
    PostQuest = "post"