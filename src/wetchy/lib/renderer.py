# -*- coding: utf-8 -*-

# Wetchy renderer module.
# Responsible for content rendering.

import cgi
import os
import sys
import traceback

from wetchy.lib import common

from wetchy.thirdparty.tenjin import tenjin

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
        Initialize renderer with settings, provided by user.
        """
        self.engine = tenjin.Engine(path = [os.path.join(common.SETTINGS["SCRIPT_PATH"], common.SETTINGS["themes"]["templates_path"], common.SETTINGS["themes"]["template_name"])], escapefunc="cgi.escape", tostrfunc="str")
        # Force cache storage to memory, to keep clean templates directory.
        tenjin.Engine.cache = tenjin.MemoryCacheStorage()
        tenjin.set_template_encoding("utf-8")
        
    def emergency_init_renderer(self):
        """
        Initialize renderer with emergency settings.
        """
        self.engine = tenjin.Engine(path = [os.path.join(common.SETTINGS["WETCHY_PATH"], "public", "themes", "default")], escapefunc="cgi.escape", tostrfunc="str")
        # Force cache storage to memory, to keep clean templates directory.
        tenjin.Engine.cache = tenjin.MemoryCacheStorage()
        tenjin.set_template_encoding("utf-8")

    def render(self, data, template = "index.pyhtml"):
        """
        Render things.
        """
        try:
            html = self.engine.render(template, data)
            common.HTML_RESPONSE = html
        except NameError as e:
            self.render_error(e)
        except tenjin.TemplateNotFoundError as e:
            self.render_error(e)
            
    def render_error(self, error):
        """
        Renders a HTML with error.
        """
        print("Encountered error: {0}".format(error))
        print("Re-initializing renderer with emergency values...")
        self.emergency_init_renderer()
        exc_type, exc_value, exc_traceback = sys.exc_info()
        data = {
            "error"                 : error,
            "traceback"             : traceback.extract_tb(exc_traceback),
        }
        html = self.engine.render("exception.pyhtml", data)
        common.HTML_RESPONSE = html
        self.init_renderer()
        
    def set_response_code(self, code):
        """
        Set response code.
        
        code [int] - integer of HTTP/1.1 code to be passed.
        """
        codes = {
            200: "200 OK",
            301: "301 Moved Permanently",
            401: "401 Unauthorized",
            404: "404 Not Found",
            501: "501 Not Implemented"
        }
        common.HTML_RESPONSE_CODE = codes[code]
