# -*- coding: utf-8 -*-

# Wetchy Router module.
# Responsible for routing things.

import os
import sys

from wetchy.lib import common

class Router:
    def __init__(self):
        common.INSTANCES["ROUTER"] = self
        
    def route_request(self):
        """
        Route request to site's application.
        """
        # Get URI.
        uri = os.environ["REQUEST_URI"]
        
        # Split it to get first parameter. This is application
        # name.
        app_name = uri.split("/")[1]
        
        # If no app_name detected (e.g. - root of site) - force
        # 'index' as app_name.
        if not app_name:
            app_name = "index"

        # Get parameters we should pass.
        try:
            params = uri.split("/")[2:]
        except:
            # We got zero parameters.
            params = ["/"]
        # Like above, but if exception wasn't raised.
        if len(params) == 0:
            params = ["/"]
            
        params = "/".join(params)
            
        # Try to initialize this application.
        print("Initializing application '{0}' with parameters: '{1}'".format(app_name, params))
        __import__("apps." + app_name)
        app = sys.modules["apps." + app_name]
        exec("self.app = app." + app_name.capitalize() + "App()")
        self.app.routes[params]
