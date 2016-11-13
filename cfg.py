
import ConfigParser


# A single place to store all configuration for the application
class Cfg:
	def __init__(self, f):
		self.config = ConfigParser.RawConfigParser()
		self.config.read(f)
		self.Dict = self.config2dict(self.config)

	def config2dict(self, cfg):
		ret = {}
		sections = cfg.sections()
		for section in sections:
			if section not in ret:
				ret[section] = {}
			for item in cfg.items(section):
				ret[section][item[0]] = item[1]
		return ret

	# If you don't know if value exist, you should use "exist()" first or catch exception
	def get(self, sect, item):
		ret = self.Dict.get(sect, {}).get(item, None)
		if ret == None:
			raise ValueError('[CFG] Tried retrieving a value that does not exist')
		return ret

	def exist(self, sect, item):
		return (self.Dict.get(sect, {}).get(item, None) != None)

	def set(self, sect, item, value):
		self.Dict[sect][item] = value
	
