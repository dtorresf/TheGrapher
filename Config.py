import json

class Config():
	'''Class that represents the Configuration for the whole thing'''
	instance = None

	#Singlenton implementation

	def __call__(cls, *args, **kw):
		if not cls.instance:
			cls.instance = super(ConfigFile, cls).__call__(*args, **kw)
		return cls.instance

	#Initialization for object
	def __init__(self):
		self.variables = {} #Empty dictionary that will hold the values of the config file parameters

	#Load config file function
	def loadconfigfile(self, file):
		'''Method that loads the file to the structure, JSON file'''
		config = json.loads(open(file).read())

		if config['exalogic_rack_size'] == 'quarter':
			config['cn_number'] = 8
			config['gw_number'] = 2
		elif config['exalogic_rack_size'] == 'half': 
			config['cn_number'] = 16
			config['gw_number'] = 2
		else: 
			config['cn_number'] = 30
			config['gw_number'] = 4

		self.variables = config
