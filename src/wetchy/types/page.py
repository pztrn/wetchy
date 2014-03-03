# -*- coding: utf-8 -*-

# Wetchy Page module.
# Contains all required tools for pages.

from wetchy.lib import common

class BasePage:
    """
    Base class for pages.
    """
    def __init__(self):
        self.renderer = common.INSTANCES["RENDERER"]

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
        import markdown
        
    def markdown_to_html(self, markdown_data):
        """
        Converts markdown pages into HTML data.
        """
        return markdown.markdown(markdown_data)
