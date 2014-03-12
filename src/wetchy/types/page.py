# -*- coding: utf-8 -*-

# Wetchy Page module.
# Contains all required tools for pages.

import markdown
import os

from wetchy.lib import common

class BasePage:
    """
    Base class for pages.
    """
    def __init__(self):
        self.renderer = common.INSTANCES["RENDERER"]
        
        # Database can be required anywhere :)
        self.database = common.INSTANCES["DATABASE"]
        
        self.PARAMS = common.PARAMETERS

class DynamicPage(BasePage):
    """
    This class contains methods and variables that suitable
    for dynamic pages.
    """
    def __init__(self):
        BasePage.__init__(self)
        
class StaticPage(BasePage):
    """
    This class contains methods and variables that suitable
    for static HTML page.
    """
    def __init__(self):
        BasePage.__init__(self)

class MarkdownPage(BasePage):
    """
    This class contains methods and variables that suitable
    for Markdown page.
    """
    def __init__(self):
        BasePage.__init__(self)
        # We doing it here because ONLY THIS CLASS requires markdown
        # module.
        import markdown
        
    def markdown_to_html(self, markdown_data):
        """
        Converts markdown pages into HTML data.
        """
        return markdown.markdown(markdown_data)
        
    def read_page(self, pagename):
        """
        Reads page from SITE_PATH/data/markdown, converts it to
        HTML and returns to caller.
        """
        data = open(os.path.join(common.SETTINGS["SCRIPT_PATH"], "data", "markdown", pagename)).read()
        return self.markdown_to_html(data)
