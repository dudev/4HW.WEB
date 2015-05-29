import socket, os

soc = socket.socket()
soc.bind(("localhost", 8080))
soc.listen(1)
print 'Serving HTTP on port 8080...'

while True:
	client_connection, client_address = soc.accept()
	request = client_connection.recv(1024)
	print request

	path = '.' + request.split('\n')[0].split(' ')[1]
	if not os.path.isfile(path):
		path ='./index.html'

	if path.split('.')[-1] == "html":
		mimeType = "text/html"
	else:
		mimeType = "image/jpeg"

	fd = open(path,'r')
	client_connection.send("HTTP/1.1 200 OK\nContent-Type: " + mimeType + "\n\n\n")
	client_connection.send(fd.read())
	fd.close()

	client_connection.close()
soc.close()
