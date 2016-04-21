import methodSwitch
import Port

class Switch:
	'''Class that represents a Switch with atributtes to graph'''
	def __init__(self,name,nports,ports):
		self.name = name
		self.nports = nports
		self.ports = ports

	def graphports(self,cf):
			methodSwitch.graph(self.ports, self.nports,cf)