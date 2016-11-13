
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from ctrl import Controller 
from urlparse import parse_qs
import builtins

class PageCatcher(Controller):
	name = "PageCatcher"
	def __init__(self, server):
		Controller.__init__(self, server)
		self.base = builtins.CFG.get(self.name, "servbase")
		self.logfile = builtins.CFG.get(self.name, "logfile")
		self.logfile = os.path.join(
			builtins.CFG.get("global","basepath"),
			self.logfile
		)

	def output2log(self, data):
		with open(self.logfile, "a+") as f:
			f.write(self.server.client_address[0] + ": " + data)

	def action(self):
		length = int(self.server.headers['content-length'])
		postvars = parse_qs(self.server.rfile.read(length), keep_blank_values=1)
		if "data" in postvars:
			self.output2log("".join(postvars["data"]) + "\n")
		self.server.send_response(200)
		self.server.send_header('Access-Control-Allow-Origin', '*')
		self.server.send_header('Content-type', 'application/json')
		self.server.end_headers()
		
		self.server.wfile.write("{status:'OK'}\n")

	def get_routes(self):
		ret = [];
		ret.append({'regexp': r'^' + self.base, 'controller': 'PageCatcher', 'action': 'action'});
		return ret;


