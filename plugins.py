
import os, sys, re

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from CGIHTTPServer import CGIHTTPRequestHandler

from ctrl import Controller

class Plugins():
	def __init__(self):
		self.plugins = {}
		self.loaded = {}

	def find_plugins(self):
		plugdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plugins/")
		plugfiles = [x[:-3] for x in os.listdir(plugdir) if x.endswith(".py")]
		sys.path.insert(0, plugdir)
		for plug in plugfiles:
			mod = __import__(plug)
	
	def register_plugins(self):
		for plugin in Controller.__subclasses__():
			self.plugins[plugin.name] = plugin
			globals()[plugin.name] = plugin



	def init_plugins(self):
		self.find_plugins();
		self.register_plugins();
	
	def get_plugin_names(self):
		return self.plugins.keys();

	def get_routes(self):
		ret = []
		for name in self.loaded.keys():
			routes = self.loaded[name].get_routes()
			for route in routes:
				ret.append(route)
		return ret

	def load_plugin(self, name, server):
		if name not in self.loaded:
			self.loaded[name] = self.plugins[name](server);
			return True
		else:
			return False






# http://stackoverflow.com/questions/932069/building-a-minimal-plugin-architecture-in-python
# http://aventures-logicielles.blogspot.no/2011/04/very-simple-http-server-with-basic-mvc.html

class Router(object):
	def __init__(self, server):
		self.__server = server
		self.__routes = []
	def addRoute(self, regexp, controller, action):
		self.__routes.append({'regexp': regexp, 'controller': controller, 'action': action})
	
	def addRouteDict(self, Dict):
		self.__routes.append(Dict)

	def route(self, path):
		for route in self.__routes:
			if re.search(route['regexp'], path):
				cls = globals()[route['controller']]
				func = cls.__dict__[route['action']]
				obj = cls(self.__server)
				apply(func,(obj, ))
				return
		self.__server.send_response(404)
		self.__server.end_headers()


class MyHTTPServer(HTTPServer):
	def __init__(self, server_address, RequestHandlerClass, handler):
		HTTPServer.__init__(self, server_address, RequestHandlerClass)
		self.handler = handler


class MyRequestHandler(CGIHTTPRequestHandler):
	def __init__(self, request, client_address, server):
		#routes = plugins
		self.__router = Router(self)
		for route in self.routes:
			self.__router.addRouteDict(route)
		BaseHTTPRequestHandler.__init__(self, request, client_address, server)

	def aRRoute(self, Dict):
		self.__router.addRouteDict(Dict)

	def do_GET(self):
		# TODO: Create a log of all requests
		self.__router.route(self.path)
	
	def do_POST(self):
		# TODO: Create a log of all requests
		self.__router.route(self.path)
	def do_OPTIONS(self):
		self.send_response(200, "ok")
		self.send_header('Access-Control-Allow-Origin', "*")
		self.send_header('Access-Control-Allow-Methods', 'GET', 'POST, OPTIONS')


