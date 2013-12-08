# -*- coding: utf-8 -*-

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

# HTML status - HTTP/1.1 status code.
# Refer to http://en.wikipedia.org/wiki/List_of_HTTP_status_codes
# for proper code. By default it will return "200 OK".
HTML_RESPONSE_CODE = "200 OK"
