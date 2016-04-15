class Port:
	'''Class that represents a Port from a Switch with atributtes to graph'''
	def __init__(self,name,switchname,rx,tx):
		self.name = name
		self.switchname = switchname
		self.rx = rx
		self.tx = tx
