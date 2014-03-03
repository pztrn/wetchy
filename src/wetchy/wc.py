#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Wetchy control - just a control module :).

import os
import shutil
import sys

######################################################################
# HELP MESSAGE
######################################################################
HELP = \
"""Wetchy control version 0.1-alpha.
Copyright (c) 2013, Stanislav N. aka pztrn.

Syntax:
    wetchy [opt] [path]

Available options ([opt]):
    -c / --create       Create new project.
"""

class WControl:
    """
    Main control class, called by default.
    """
    def __init__(self):
        # Wetchy Control path.
        self.path = os.path.abspath(os.path.normpath(__file__))
        self.path = os.path.dirname(self.path)
        
    def parse_parameters(self):
        """
        CLI parameters parsing.
        """
        if len(sys.argv[1:]) > 0:
            self.check_dependencies()
            if sys.argv[1] in ["-c", "--create"]:
                # We need a project name and path.
                if len(sys.argv) > 2:
                    self.create_project()
                else:
                    print("Project name is empty, cannot continue")
                    exit(2)
        else:
            self.help()
            
    def check_dependencies(self):
        """
        Check if neccessary dependencies are present.
        """
        required = ["alembic", "sqlalchemy"]
        print("Checking required modules presense...")
        not_found = {}
        for item in required:
            try:
                __import__(item)
                del(item)
            except:
                not_found[item] = True
            
        if len(not_found) > 0:
            # Compose string with dependencies.
            deps_string = ", ".join(not_found.keys())
            print("These dependencies are required, but not found: %s" % deps_string)
            exit(1)
            
    def create_project(self):
        """
        Creating new project and configures it.
        """
        # First parameter must be a project name.
        project_name = sys.argv[2]
        # Second parameter - project path.
        try:
            project_path = sys.argv[3]
        except:
            print("Project path not defined")
            
        project_path = os.path.abspath(os.path.normpath(project_path))
            
        print("Creating new project '{0}'...".format(sys.argv[2]))
        
        # Copy default project.
        print("Copying default project...")
        try:
            shutil.copytree(self.path + "/examples/default_project", project_path)
        except FileExistsError:
            shutil.rmtree(project_path)
            shutil.copytree(self.path + "/examples/default_project", project_path)
        except Exception as e:
            print("Failed to copy default project: " + str(e))
            
    def help(self):
        """
        Shows help message.
        """
        print(HELP)
        
if __name__ == "__main__":
    w = WControl()
    w.parse_parameters()
