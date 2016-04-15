import methodSwitch

class Switch:
	'''Class that represents a Switch with atributtes to graph'''
	def __init__(self,name,mem,cpu,established,timewait,closewait,finw1,finw2,nprocs,nopenf):
		self.name = name
		self.mem = mem
		self.cpu = cpu
		self.established = established
		self.timewait = timewait
		self.closewait = closewait
		self.finw1 = finw1
		self.finw2 = finw2
		self.nprocs = nprocs
		self.nopenf = nopenf