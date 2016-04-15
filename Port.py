class Port:
	'''Class that represents a Port from a Switch with atributtes to graph'''
	def __init__(self,name,rx,tx):
		self.name = name
		self.rx = rx
		self.tx = tx
