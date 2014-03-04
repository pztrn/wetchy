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
        self.renderer.init_renderer()
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

    def process_request(self, responser):
        """
        Starting point for processing client request.
        """
        self.process()
        self.router.route_request()
        status, response_body = self.get_response()
        response_headers = common.RESPONSE_HEADERS
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

        return self.process_request(responser)
        
    def get_response(self):
        """
        Returns HTML page contents and HTML status code.
        """
        return(common.HTML_RESPONSE_CODE, common.HTML_RESPONSE)
