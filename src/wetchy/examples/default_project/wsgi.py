#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# WSGI handler for GSTools.
import os
import sys
import wsgi
wsgi.multiprocess = True
from wsgiref.simple_server import make_server
import mimetypes
import cgi

import gstools

WSGI_INPUT = ""

def serve_file(full_path, responser):
    mime = mimetypes.guess_type(full_path)[0] or 'text/plain'
    response_headers = [("Content-Type", mime)]
    status = '200 OK'
    responser(status, response_headers)
    return [open(full_path, 'rb').read()]

def process_request(responser):
    pcl_main = gstools.GSTools(WSGI_INPUT)
    status, response_body = gstools_main.get_response()
    response_headers = [("Content-Type", "text/html; charset=utf-8")]
    responser(status, response_headers)
    return [response_body.encode("utf-8")]

def application(environ, responser):
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

    global WSGI_INPUT
    if environ['REQUEST_METHOD'] == 'POST':
        # Hey, we got a POST :) Let's export it!
        WSGI_INPUT = cgi.FieldStorage(
            fp=environ['wsgi.input'],
            environ=environ,
            keep_blank_values=True
        )
    else:
        WSGI_INPUT = cgi.FieldStorage()

    #response_body = ['%s: %s' % (key, value)
    #                for key, value in sorted(environ.items())]
    #response_body = '\n'.join(response_body)

    if "DEBUG" in os.environ:
        if os.environ["DEBUG"] == "true":
        # try to serve local file
            full_path = os.environ["PWD"] + "/public" + os.environ["REQUEST_URI"]
            if os.environ["REQUEST_URI"] != "/" and os.path.exists(full_path):
                return serve_file(full_path, responser)
            else:
                return process_request(responser)

    return process_request(responser)

if "DEBUG" in os.environ:
    if os.environ["DEBUG"] == "true":
        httpd = make_server('localhost', 8051, application)
        httpd.serve_forever()
