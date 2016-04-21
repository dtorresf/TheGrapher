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

	def graphcpu(self,cf):
		methods.graph(self.cpu,'date','cpu', self.name,cf)
	def graphmem(self,cf):
		methods.graph(self.mem,'date','mem', self.name,cf)
	def graphestablished(self,cf):
		methods.graph(self.established,'date','established', self.name,cf)
	def graphtimewait(self,cf):
		methods.graph(self.timewait,'date','timewait', self.name,cf)
	def graphclosewait(self,cf):
		methods.graph(self.closewait,'date', 'closewait', self.name,cf)
	def graphfinw1(self,cf):
		methods.graph(self.finw1,'date','finw1', self.name,cf)
	def graphfinw2(self,cf):
		methods.graph(self.finw2,'date','finw2', self.name,cf)
	def graphnprocs(self,cf):
		methods.graph(self.nprocs,'date','nprocs', self.name,cf)
	def graphnopenf(self,cf):
		methods.graph(self.nopenf,'date','nopenf', self.name,cf)
	def graphserver(self,cf):
		self.graphcpu(cf)
		self.graphmem(cf)
		self.graphestablished(cf)
		self.graphtimewait(cf)
		self.graphclosewait(cf)
		self.graphfinw1(cf)
		self.graphfinw2(cf)
		self.graphnprocs(cf)
		self.graphnopenf(cf)
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