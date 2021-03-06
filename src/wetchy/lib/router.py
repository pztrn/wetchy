# -*- coding: utf-8 -*-

# Wetchy Router module.
# Responsible for routing things.

import mimetypes
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
        
        # Just in case we run site in DEBUG mode - overwrite
        # common.RESPONSE_HEADERS with default value.
        if "DEBUG" in os.environ:
            common.RESPONSE_HEADERS = [("Content-Type", "text/html; charset=utf-8")]
        
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
        if len(params) == 0 or params == "" or not params or params[0] == "":
            params = ["/"]
            
        params = "/".join(params)
        
        # Try to initialize this application. If we call for templates,
        # we should just serve this file without any errors.
        if not "themes" in app_name and not "wetchy" in app_name and not "wetchy" in params:
            print("Initializing application '{0}' with parameters: '{1}'".format(app_name, params))
            try:
                __import__("apps." + app_name)
                app = sys.modules["apps." + app_name]
                exec("self.app = app." + app_name.capitalize() + "App()")
                # Parse parameters.
                params = self.parse_params(params)
                self.app.routes[params]()
            except ImportError as e:
                common.INSTANCES["RENDERER"].render_error(e)
        else:
            self.serve_file(app_name + "/" + params)
            
    def parse_params(self, params):
        """
        Parse parameters in metainterpretation thing, like
        "/:int/:str/" for "/3/info/".
        """
        temp_params = params.split("/")
        # Parameters should be wide-accessible thing. At least, for
        # site applications.
        common.PARAMETERS = temp_params
        params = [""]
        
        for item in temp_params:
            if item != "":
                # Try to make it int. If we failed - it's string! :)
                try:
                    int(item)
                    params.append(":int")
                except:
                    params.append(":str")
                
        params = "/".join(params)
        
        if len(params) == 0:
            params = "/"
        
        return params
            
    def serve_file(self, file_path):
        """
        Serve file. This method is useful when you run site in
        DEBUG mode.
        
        This method will serve only files from public directory
        (site or Wetchy).
        """
        # Getting real path of file.
        wetchy_public = os.path.join(common.SETTINGS["WETCHY_PATH"], "public")
        site_public = os.path.join(common.SETTINGS["SCRIPT_PATH"], "public")
        if not os.path.exists(os.path.join(site_public, file_path)):
            params = os.path.join(wetchy_public, file_path)
        else:
            params = os.path.join(site_public, file_path)
            
        if "wetchy" in file_path:
            print("Detected request for Wetchy public file")
            print(file_path.split("wetchy")[1])
            params = wetchy_public + file_path.split("wetchy")[1]

        print("Serving file '{0}'".format(params))
        
        mime = mimetypes.guess_type(params)[0] or 'text/plain'
        response_headers = [("Content-Type", mime + "; charset=utf-8")]
        common.RESPONSE_HEADERS = response_headers
        
        # Read file completely.
        try:
            data = open(params, "r").read()
            common.HTML_RESPONSE_CODE = "200 OK"
            common.HTML_RESPONSE = data
        except:
            # File reading failed. Crap.
            common.HTML_RESPONSE_CODE = "404 Not Found"
            common.HTML_RESPONSE = "File not found"
            
        return [data]
        
