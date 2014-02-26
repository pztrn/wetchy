# -*- coding: utf-8 -*-

<<<<<<< HEAD
# Wetchy version :)
VERSION = "0.1-alpha"
# Version tuple - for those, who rely on versions.
VERSION_TUPLE = ("0", "1", "a")

# HTML response - full HTML text of page.
# By default it will print some Hello World thing.
HTML_RESPONSE = """
<html>
<head>
<title>Wetchy is ready to serve you!</title>
</head>
<body>
<h1>Hello!</h1>
<p>This is <a href='https://github.com/pztrn/wetchy/'>Wetchy</a>, the <b>WE</b>b <b>T</b>ool<b>CH</b>ain written in p<b>Y</b>thon.</p>
<p>If you see this message, then everything is okay and Wetchy ready to serve you!<p>
<hr>
<i>Wetchy 0.1-alpha</i>
</body>
</html>
"""
# Configuration dictionary. This dictionary will be filed with
# help of lib/config.py/Config().
#
# WARNING! THIS IS STATIC SETTINGS DICTIONARY! DO NOT CHANGE THEM!
# OTHERWISE WETCHY MAY PRODUCE ERRORS OR EVEN FAIL TO START!
SETTINGS = {}

# Temporary settings. These settings can be changed runtime.
TEMP_SETTINGS = {}

# Instances of all base classes, like configuration.
INSTANCES = {}
