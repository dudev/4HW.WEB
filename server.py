#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Устанавливаем стандартную внешнюю кодировку = utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import selector
from jinja2 import Environment, FileSystemLoader

to_index = u"""<a href="/">Домой</a>"""
to_about = u"""<a href="about/aboutme.html">Обо мне</a>"""

response_code = '200 OK'
response_type = ('Content-Type', 'text/html')

class BaseApp(object):
	def __init__(self, environ, start_response, link, template):
		self.env = environ
		self.start_response = start_response
		self.templates  = Environment(loader=FileSystemLoader('templates'))
		self.template = template
		self.link = link
	def __iter__(self):
		self.start_response(response_code, [response_type])
		template = self.templates.get_template(self.template)
		yield template.render(link=self.link)

class IndexApp(BaseApp):
	def __init__(self,environ,start_response):
		BaseApp.__init__(self, environ, start_response, to_about, "index.html")

class AboutApp(BaseApp):
	def __init__(self,environ,start_response):
		BaseApp.__init__(self, environ, start_response, to_index, "about/aboutme.html")

def WSGIApp():
	disp = selector.Selector()
	disp.add("/", GET = IndexApp)
	disp.add("/index.html", GET = IndexApp)
	disp.add("/about/aboutme.html", GET = AboutApp)
	return disp



# allows use this code in the functions and classes above
# ('import serve' at the top of this file)
if __name__ == '__main__':
	from paste.httpserver import serve
	app = WSGIApp()
	serve(app, host='localhost', port=8087)