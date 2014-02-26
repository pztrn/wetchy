# -*- coding: utf-8 -*-

# Wetchy renderer module.
# Responsible for content rendering.

import os

from lib import common

from thirdparty.tenjin import tenjin

class Renderer:
    def __init__(self):
        # Template path and template name. They will be calculated
        # as "TEMPLATE_PATH/TEMPLATE_NAME". TEMPLATE_PATH, usually,
        # will be "$PROJECT_PATH/public/themes/".
        self.template_path = None
        self.template_name = None
        
        # Create instance pointer.
        common.INSTANCES["RENDERER"] = self

    def init_renderer(self):
        """
        Initialize renderer.
        """
        self.engine = tenjin.Engine(path = [os.path.join(common.TEMP_SETTINGS["SCRIPT_PATH"], common.SETTINGS["theme"]["templates_path"], common.SETTINGS["theme"]["template_name"])])#, trace = True)
        # Force cache storage to memory, to keep clean templates directory.
        tenjin.Engine.cache = tenjin.MemoryCacheStorage()
        tenjin.set_template_encoding("utf-8")
