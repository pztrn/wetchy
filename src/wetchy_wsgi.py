#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# WSGI handler for Wetchy.
import os
import sys
#import wsgi
#wsgi.multiprocess = True
from wsgiref.simple_server import make_server
import mimetypes
import cgi

class Wetchy_WSGI:
    def __init__(self, project_main):
        self.WSGI_INPUT = ""
        self.instances = {}
        self.project_main = project_main
            
        # If we got "DEBUG" in operating system environment - we will
        # launch an internal web server for testing purposes.
        if "DEBUG" in os.environ:
            if os.environ["DEBUG"] == "true":
                httpd = make_server('localhost', 8051, self.application)
                httpd.serve_forever()
        
    def initialize(self):
        """
        Wetchy initialization.
        """
        return self

    def serve_file(self, full_path, responser):
        mime = mimetypes.guess_type(full_path)[0] or 'text/plain'
        response_headers = [("Content-Type", mime)]
        status = '200 OK'
        responser(status, response_headers)
        return [open(full_path, 'rb').read()]

    def process_request(self, responser):
        status, response_body = self.project_main.get_response()
        response_headers = [("Content-Type", "text/html; charset=utf-8")]
        responser(status, response_headers)
        return [response_body.encode("utf-8")]

    def application(self, environ, responser):
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

        #response_body = ['%s: %s' % (key, value)
        #                for key, value in sorted(environ.items())]
        #response_body = '\n'.join(response_body)

        if "DEBUG" in os.environ:
            if os.environ["DEBUG"] == "true":
            # try to serve local file
                full_path = os.environ["PWD"] + "/public" + os.environ["REQUEST_URI"]
                if os.environ["REQUEST_URI"] != "/" and os.path.exists(full_path):
                    return self.serve_file(full_path, responser)
                else:
                    return self.process_request(responser)

        return process_request(responser)
        
    def __getattr__(self, key):
        """
        Overloaded for usage of dot syntax. You can access package
        metadata thru, e.g., wetchy.name, instead of wetchy[smthing]["name"].
        """
        # First, try to return from metadata
        try:
            return self.instances[key]
        except KeyError:
            pass
        # If that fails, return default behavior so we don't break everything.
        try:
            return self.__dict__[key]
        except KeyError:
            raise AttributeError(key)
