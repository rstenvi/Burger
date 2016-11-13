#!/usr/bin/python

import builtins
import os, logging

# Used to make it easier to specify IP address, but not required
try:
	import netifaces
except ImportError:
	logging.warning("Unable to import netifaces module")
	netifaces = None



# Solution from http://stackoverflow.com/questions/431684/how-do-i-cd-in-python/13197763#13197763
# Change directory during an operation, use like "with cd("path"): <statements>
class cd:
	def __init__(self, newPath):
		 self.newPath = os.path.expanduser(newPath)

	def __enter__(self):
		self.savedPath = os.getcwd()
		os.chdir(self.newPath)

	def __exit__(self, etype, value, traceback):
		os.chdir(self.savedPath)





def create_dir(f):
	d = os.path.dirname(f)
	if not os.path.exists(d):
		os.makedirs(d)

def get_iplist():
	ip_list = []
	for interface in netifaces.interfaces():
		for link in netifaces.ifaddresses(interface).get(netifaces.AF_INET, ()):
			ip_list.append(link['addr'])
	return ip_list

def choose_list(lst, msg):
	for i in range(0, len(lst)):
		print "[" + str(i+1) + "] " + lst[i]
	ind = raw_input(msg)
	ind = int(ind)-1
	if ind < 0 or ind >= len(lst):
		return choose_list(lst, msg)
	else:
		return lst[ind]

def choose_return_ip():
	ip = None
	if netifaces == None:
		ip = raw_input("Enter return IP: ")
	else:
		ips = get_iplist()
		ip = choose_list(ips, "Choose return IP ")
	return ip



def file2string(fname):
	ret = ""
	with open(fname, "r") as f:
		ret = f.read()
	return ret

def string2file(s, fname):
	with open(fname, "w") as f:
		f.write(s)



