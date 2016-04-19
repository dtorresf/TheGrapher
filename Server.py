import methodServer
import methods 

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
		methods.graph(self.cpu,'date','cpu', self.name)
	def graphmem(self):
		methods.graph(self.mem,'date','mem', self.name)
	def graphestablished(self):
		methods.graph(self.established,'date','established', self.name)
	def graphtimewait(self):
		methods.graph(self.timewait,'date','timewait', self.name)
	def graphclosewait(self):
		methods.graph(self.closewait,'date', 'closewait', self.name)
	def graphfinw1(self):
		methods.graph(self.finw1,'date','finw1', self.name)
	def graphfinw2(self):
		methods.graph(self.finw2,'date','finw2', self.name)
	def graphnprocs(self):
		methods.graph(self.nprocs,'date','nprocs', self.name)
	def graphnopenf(self):
		methods.graph(self.nopenf,'date','nopenf', self.name)
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