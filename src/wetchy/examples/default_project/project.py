#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Project's main file.

import sys

##################################################
# CONFIGURATION
##################################################
# Path where Wetchy is located. This is the only one hardcoded variable.
wetchy_path = "/path/to/wetchy"

if not wetchy_path in sys.path:
    sys.path.insert(0, wetchy_path)
    
import os
import wetchy_wsgi

class Project:
    def __init__(self):
        # Initializing Wetchy WSGI handler.
        self.wetchy = wetchy_wsgi.Wetchy_WSGI(self)
        self.wetchy = self.wetchy.initialize()
        
    def get_response(self):
        """
        This method pushes back generated HTML, together with
        status code.
        """
        return ["200 OK", "<h1>Wetchy is here!</h1>"]

if __name__ == "__main__":
    Project()
