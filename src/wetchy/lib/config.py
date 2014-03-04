# -*- coding: utf-8 -*-

# Wetchy Configuration parser.

import os
import configparser

from wetchy.lib import common

class Config:
    def __init__(self):
        self.cp = configparser.ConfigParser()
        
        # Create instance pointer.
        common.INSTANCES["CONFIG"] = self
        
        # Configuration dictionary we will work with.
        self.config = {}
        
        # Make sure we will save our current settings. It must be only
        # project path for now.
        self.old_settings = common.SETTINGS
        
        # Parse configuration from launched project.
        self.parse_configuration()
        
    def parse_configuration(self):
        """
        Parse configuration files.
        
        Firstly we will parse default configuration provided with
        Wetchy. Afterwards, we will parse project-specific configuration
        and replace default values with project-defined ones.
        """
        print("Loading Wetchy configuration...")
        # Parse default configuration.
        # First, we get path of this module.
        wetchy_path = os.path.abspath(os.path.dirname(__file__))
        # Remove last element.
        wetchy_path = os.path.dirname(wetchy_path)
        # Get configs listing from wetchy_path/config
        configs = os.listdir(os.path.join(wetchy_path, "config"))
        for config in configs:
            # We will parse only files that ends with "conf".
            if "conf" in config:
                self.cp.read(os.path.join(wetchy_path, "config", config))
                
        # Now same thing, but for project-specific configuration.
        print("Loading project configuration...")
        configs = os.listdir(os.path.join(self.old_settings["SCRIPT_PATH"], "config"))
        for config in configs:
            # We will parse only files that ends with "conf".
            if "conf" in config:
                self.cp.read(os.path.join(self.old_settings["SCRIPT_PATH"], "config", config))
                
        # Replace themes things. Variables that will be replaced:
        #   * PROJECT_PATH - will be replaced on real project path.
        #   * WETCHY_PATH - will be replaced on real wetchy path.
        self.cp["themes"]["templates_path"] = self.cp["themes"]["templates_path"].replace("PROJECT_PATH", self.old_settings["SCRIPT_PATH"])
        
        # Re-generate configuration.
        self.config = dict(self.cp)
        self.config.update(self.old_settings)
        
        # Insert WETCHY_PATH variable into config.
        self.config["WETCHY_PATH"] = wetchy_path
        
        # Replace common.SETTINGS with newly parsed configuration.
        # Actually, we should not use it at all, but in case of
        # emergency nothing should break itself.
        common.SETTINGS = self.config
