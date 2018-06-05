# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 15:43:44 2018

@author: evin
@brief: Class in order to enable CORS - .JS getting data from another web address
       sourced from: http://stackoverflow.com/questions/17262170/bottle-py-enabling-cors-for-jquery-ajax-requests
"""

from bottle import response
import bottle

class EnableCors(object):
    """Class in order to enable CORS - .JS getting data from another web address
       sourced from: http://stackoverflow.com/questions/17262170/bottle-py-enabling-cors-for-jquery-ajax-requests
    """
    name = 'enable_cors'
    api = 2

    def apply(self, fn, context):
        def _enable_cors(*args, **kwargs):
            # set CORS headers
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

            if bottle.request.method != 'OPTIONS':
                # actual request; reply with the actual response
                return fn(*args, **kwargs)
        return _enable_cors