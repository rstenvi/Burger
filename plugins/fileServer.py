
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from ctrl import Controller 
import builtins

class FileServer(Controller):
	name = "FileServer"
	def __init__(self, server):
		Controller.__init__(self, server)
		self.status=200
		self.base = builtins.CFG.get(self.name, "servbase")
		self.gbase = builtins.CFG.get("global", "basepath")
		self.lbase = builtins.CFG.get(self.name, "servpath")
		self.serv_path = os.path.join(self.gbase, self.lbase)


	def file2string(self, File):
		ret = ""
		with open(File, "r") as f:
			ret = f.read()
		return ret

	def send_file(self, File, content):
		self.server.send_response(200)
		self.server.send_header('Content-type', content)
		self.server.end_headers()
		
		resp = self.file2string(File)
		self.server.wfile.write(resp)

	def send_error(self):
		self.server.send_response(404)
		self.server.end_headers()
		#self.server.wfile.write(None)

	def ftype2mime(self, ftype):
		# TODO: Add some more extensions
		a = ftype.lower()
		if a == "js":	return "application/javascript"
		elif a == "html":	return "text/html"
		else:			return "application/octet-stream"

	def action(self):
		get = self.server.path[len(self.base)+1:]
		if get == "":
			self.send_error()
		else:
			read = os.path.join(self.serv_path, get)
			if os.path.isfile(read):
				ftype="unknown"
				dot = get.find(".")
				if dot != -1:
					ftype = get[dot+1:]
				self.send_file(read, self.ftype2mime(ftype))
			else:
				self.send_error()

	def get_routes(self):
		ret = [];
		ret.append({'regexp': r'^' + self.base + '/', 'controller': 'FileServer', 'action': 'action'});
		return ret;


