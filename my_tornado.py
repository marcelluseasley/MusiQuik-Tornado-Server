__author__ = 'measley'

# port = 26395

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from mqflasklogger import app

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(26395)
IOLoop.instance().start()
