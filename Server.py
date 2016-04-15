import methodServer

class Server:
	'''Class that represents a Server with atributtes to graph'''
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

	def graphcpu(self):
		methodServer.graph(self.cpu, 'cpu', self.name)
	def graphmem(self):
		methodServer.graph(self.mem, 'mem', self.name)
	def graphestablished(self):
		methodServer.graph(self.established, 'established', self.name)
	def graphtimewait(self):
		methodServer.graph(self.timewait, 'timewait', self.name)
	def graphclosewait(self):
		methodServer.graph(self.closewait, 'closewait', self.name)
	def graphfinw1(self):
		methodServer.graph(self.finw1, 'finw1', self.name)
	def graphfinw2(self):
		methodServer.graph(self.finw2, 'finw2', self.name)
	def graphnprocs(self):
		methodServer.graph(self.nprocs, 'nprocs', self.name)
	def graphnopenf(self):
		methodServer.graph(self.nopenf, 'nopenf', self.name)
	def graphserver(self):
		self.graphcpu()
		self.graphmem()
		self.graphestablished()
		self.graphtimewait()
		self.graphclosewait()
		self.graphfinw1()
		self.graphfinw2()
		self.graphnprocs()
		self.graphnopenf()
	def meancpu(self):
		return self.cpu.mean()
	def meanmem(self):
		return self.mem.mean()
	def meanestablished(self):
		return self.established.mean()
	def meantimewait(self):
		return self.timewait.mean()
	def meanclosewait(self):
		return self.closewait.mean()
	def meanfinw1(self):
		return self.finw1.mean()
	def meanfinw2(self):
		return self.finw2.mean()
	def meannprocs(self):
		return self.nprocs.mean()
	def meannopenf(self):
		return self.nopenf.mean()
