
from slimit.parser import Parser
from slimit.visitors import nodevisitor
from slimit import ast
from slimit import minify

import re
from copy import deepcopy
from pprint import pprint

class ParseJS:
	def __init__(self):
		self.modules = []
		self.raw = ""
		self.raw_top = ""

	def remove_code(self, orig, rem):
		# Normalize the output string
		# This will be overwritten by to_ecma() anyway
		otrimmed = minify(orig, mangle=False, mangle_toplevel=False)
		rtrimmed = minify(rem, mangle=False, mangle_toplevel=False)

		f = otrimmed.find(rtrimmed)
		if f == -1:
			print "ORIGINAL"
			pprint(otrimmed)
			print "REMOVE"
			pprint(rtrimmed)
			raise ValueError("Unable to find extracted code in original code")
		ret = otrimmed.replace(rtrimmed, "")
		return ret


	def parse_sc(self, sc):
		parser = Parser()
		tree = parser.parse(sc)
		for node in nodevisitor.visit(tree):
			if isinstance(node, ast.VarStatement):
				varDecs = node.children()
				if len(varDecs) == 0:	continue
				elif len(varDecs) > 1:	raise ValueError("Unexpected number of children in variable declaration")
				else:
					varDec = varDecs[0]
					identifier = varDec.children()[0]
					ret = {"value": identifier.value, "code":node.to_ecma(), "type":"variable"}
					return ret
			elif isinstance(node, ast.FuncDecl):
				funcDecls = node.children()
				funcName = funcDecls[0].value
				params = []
				for i in range(1, len(funcDecls)):
					if isinstance(funcDecls[i], ast.Identifier):
						params.append(funcDecls[i].value)
					else:
						break
				ret = {"value": funcName, "code":node.to_ecma(), "type":"function", "params":params}
				return ret

		return None

	def add_sc(self, sc):
		mods = []
		res = self.parse_sc(sc)
		while res != None:
			self.modules.append(deepcopy(res))
			mods.append(res["value"])
			sc = self.remove_code(sc, res["code"])
			res = self.parse_sc(sc)
		return mods

	def add_raw_sc(self, sc):
		self.raw += sc
	def add_raw_sc_top(self, sc):
		self.raw_top = sc

	def get_function_list(self):
		ret = []
		for m in self.modules:
			ret.append(m.get("value", "ERROR"))
		return ret

	def generate_js(self, mods):
		ret = self.raw_top
		for e in self.modules:
			ret += "\n" + e["code"]
		ret += self.raw
		return ret



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

