
import re

# A simple class to do some basic JS parsing. Used to find functions and maybe only include some functions.
class CreateJS:
	def __init__(self):
		self.js = ""	# User-defined JS
		self.jsg = ""	# Global JS - for variables

		# List of available JS functions
		self.js_funcs = {};

	# Add source code at the beginning of the file
	def add_global_sc(self, sc):
		self.jsg += sc

	# Add source code withtout parsing
	def add_source_code(self, sc):
		self.js += sc;

	# Internal function to get all date between "{" and "}"
	def get_function_code(self, string, index):
		i = string.find("{", index) + 1
		brackets = 1;
		while brackets > 0 and i < len(string):
			if(string[i] == '{'):	brackets += 1
			elif(string[i] == '}'):	brackets -= 1
			i += 1
		if i >= len(string):
			return -1
		else:
			return i

	def add_functions(self, sc):
		ins = ""
		loc = 0;
		while(1):
			ind = sc.find("function", loc);
			if(ind == -1):	break;

			loc2 = self.get_function_code(sc, ind);
			if loc2 > loc:
				func = sc[ind:loc2+1]
				search = re.search("function ([a-zA-Z_$][0-9a-zA-Z_$]*)[ \t\n]*\(", func, re.IGNORECASE)
				if search:
					self.js_funcs[search.group(1)] = func;
				loc = loc2+1
			else:
				break

	def get_function_list(self):
		return self.js_funcs.keys()

	def print_function(self, fname):
		print self.js_funcs.get(fname, "Function does not exist")

	def get_js(self):
		return self.js

	def generate_js(self, funcs):
		ret = ""
		ret += self.jsg
		ret += "\n"
		for func in funcs:
			ret += self.js_funcs.get(func, "")
		ret += "\n"
		ret += self.js
		return ret

