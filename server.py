import os

top = "<div class='top'>Middleware TOP</div>"
bottom = "<div class='botton'>Middleware BOTTOM</div>"

class WSGIApp(object):
	def __init__(self, app):
		self.app = app

	def __call__(self, environ, start_response):
		response = self.app(environ, start_response)[0]
		if response.find("<body>") >-1:
			response = response.replace("<body>", "<body>" + top).replace("</body>", bottom + "</body>")
			yield response
		else:
			yield top + response + bottom

def app(environ, start_response):
	path = '.' + environ['PATH_INFO']
	if not os.path.isfile(path):
		path ='./index.html'

	fd = open(path,'r')
	data = fd.read()
	fd.close()

	response_code = '200 OK'
	response_type = ('Content-Type', 'text/HTML')
	start_response(response_code, [response_type])
	return [data]

app = WSGIApp(app)


# allows use this code in the functions and classes above
# ('import serve' at the top of this file)
if __name__ == '__main__':
	from paste import reloader
	from paste.httpserver import serve

	reloader.install()
	serve(app, host='localhost', port=8082)