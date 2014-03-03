#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Wetchy - Web toolchain written in python 3.
#
# This is a main class, that contains wetchy initializations.
import os
import sys
import wsgiref
wsgiref.multiprocess = True
from wsgiref.simple_server import make_server
import mimetypes
import cgi

from wetchy.lib import common
from wetchy.lib.config import Config
from wetchy.lib.renderer import Renderer
from wetchy.lib.router import Router

class Wetchy:
    def __init__(self, project_path):
        self.WSGI_INPUT = ""
        
        common.INSTANCES["WETCHY"] = self
        
        # Initializing Wetchy libraries.
        self.wetchy_common = common
        common.SETTINGS["SCRIPT_PATH"] = project_path
        self.config_instance = Config()
        self.config = common.SETTINGS
        self.renderer = Renderer()
        self.router = Router()
        
        if "DEBUG" in os.environ:
            if os.environ["DEBUG"] == "true":
                print("Listening on http://localhost:8051/")
                httpd = make_server('localhost', 8051, self.application)
                httpd.serve_forever()
        else:
            # No debug, but still trying to launch as standalone? NOWAI!
            print("This site should not be running as standalone application.")
            print("You should use one of these great application servers:")
            print("gunicorn, uwsgi.")
            print("If you still want to run this site as standalone application,")
            print("use this command:\n")
            print("\tDEBUG=true ./project.py")
            exit(1)

    def serve_file(self, full_path, responser):
        """
        Serving some static file.
        
        It is not recommended to use this method in "everyfile" case,
        better to configure your webserver for serving static data.
        
        In future this method may be enchanced with download rights
        checks.
        """
        mime = mimetypes.guess_type(full_path)[0] or 'text/plain'
        response_headers = [("Content-Type", mime)]
        status = '200 OK'
        self.responser(status, response_headers)
        return [open(full_path, 'rb').read()]

    def process_request(self, responser):
        """
        Starting point for processing client request.
        """
        self.process()
        self.router.route_request()
        status, response_body = self.get_response()
        response_headers = [("Content-Type", "text/html; charset=utf-8")]
        responser(status, response_headers)
        return [response_body.encode("utf-8")]

    def application(self, environ, responser):
        """
        Starting point for application processing.
        """
        os.environ["HTTP_HOST"] = environ.get("HTTP_HOST", "127.0.0.1")
        os.environ["REQUEST_URI"] = str(environ.get("PATH_INFO", "/"))
        os.environ["REMOTE_ADDR"] = environ.get("REMOTE_ADDR", "127.0.0.1")
        os.environ["HTTP_ACCEPT_LANGUAGE"] = environ.get("HTTP_ACCEPT_LANGUAGE", "en-US")
        os.environ["HTTP_USER_AGENT"] = environ.get("HTTP_USER_AGENT", "[Not Set]")
        if "HTTP_COOKIE" in environ:
            os.environ["HTTP_COOKIE"] = environ["HTTP_COOKIE"]

        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0

        if environ['REQUEST_METHOD'] == 'POST':
            # Hey, we got a POST :) Let's export it!
            self.WSGI_INPUT = cgi.FieldStorage(
                fp=environ['wsgi.input'],
                environ=environ,
                keep_blank_values=True
            )
        else:
            self.WSGI_INPUT = cgi.FieldStorage()

        if "DEBUG" in os.environ:
            if os.environ["DEBUG"] == "true":
            # try to serve local file
                full_path = os.environ["PWD"] + "/public" + os.environ["REQUEST_URI"]
                if os.environ["REQUEST_URI"] != "/" and os.path.exists(full_path):
                    return serve_file(full_path, responser)
                else:
                    return self.process_request(responser)

        return self.process_request(responser)
        
    def get_response(self):
        """
        Returns HTML page contents and HTML status code.
        """
        return(common.HTML_RESPONSE_CODE, common.HTML_RESPONSE)
