# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 15:24:01 2018

@author: evin
@brief: Class implemented for providing the server to be stopped when the app is closed
"""

from bottle import ServerAdapter

class StoppableWSGIRefServer(ServerAdapter):
    """
    Class implemented for providing the server to be stopped when the app is closed
    """
    server = None

    def run(self, handler):
        from wsgiref.simple_server import make_server, WSGIRequestHandler
        if self.quiet:
            class QuietHandler(WSGIRequestHandler):
                def log_request(*args, **kw): pass
            self.options['handler_class'] = QuietHandler
        server = make_server(self.host, self.port, handler, **self.options)
        self.server = server
        self.server.serve_forever()

    def stop(self):
        self.server.shutdown()