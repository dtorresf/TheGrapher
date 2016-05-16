import methods
import pandas as pd 
import Pptxr

class Server:
	'''Class that represents a Server with atributtes to graph'''
	def __init__(self):
		self.name = ''
		self.mem = pd.DataFrame()
		self.cpu = pd.DataFrame()
		self.established = pd.DataFrame()
		self.timewait = pd.DataFrame()
		self.closewait = pd.DataFrame()
		self.finw1 = pd.DataFrame()
		self.finw2 = pd.DataFrame()
		self.nprocs = pd.DataFrame()
		self.nopenf = pd.DataFrame()

	def importdatatoserver(self,csvfile,cf):
		'''The function that imports data from CSV file to a Server'''
		'''The head variable must be global and is on the config file'''
		head = cf.variables['computenode_head']
		methods.addheadformat(csvfile,head)
		data=pd.read_csv(csvfile,parse_dates=['date'],dayfirst=True)
		name_data = data[['name']]
		name_value = name_data.values
		name = str(name_value[0])
		self.name = name[2:-2]
		self.mem = data[['date','mem']]
		self.cpu = data[['date','cpu']]
		self.established = data[['date','established']]
		self.timewait = data[['date','timewait']]
		self.closewait = data[['date','closewait']]
		self.finw1 = data[['date','finw1']]
		self.finw2 = data[['date','finw2']]
		self.nprocs = data[['date','nprocs']]
		self.nopenf = data[['date','nopenf']]
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
	def graphcpu(self,cf):
		methods.graph(self.cpu,'date','cpu', self.name,cf,'% CPU','darkturquoise')
	def graphmem(self,cf):
		methods.graph(self.mem,'date','mem', self.name,cf,'% Memory','darkturquoise')
	def graphestablished(self,cf):
		methods.graph(self.established,'date','established', self.name,cf,'# Established Connections','darkturquoise')
	def graphtimewait(self,cf):
		methods.graph(self.timewait,'date','timewait', self.name,cf,'# Time Wait Connections','darkturquoise')
	def graphclosewait(self,cf):
		methods.graph(self.closewait,'date', 'closewait', self.name,cf,'# Close Wait Connections','darkturquoise')
	def graphfinw1(self,cf):
		methods.graph(self.finw1,'date','finw1', self.name,cf,'# Fin Wait 1 Connections','darkturquoise')
	def graphfinw2(self,cf):
		methods.graph(self.finw2,'date','finw2', self.name,cf,'# Fin Wait 2 Connections','darkturquoise')
	def graphnprocs(self,cf):
		methods.graph(self.nprocs,'date','nprocs', self.name,cf, '# Running Processes','darkturquoise')
	def graphnopenf(self,cf):
		methods.graph(self.nopenf,'date','nopenf', self.name,cf,'# Open Files','darkturquoise')
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
	def serverpptxreport(self,cf,pptxr):
		cpu_mean=str(format(self.meancpu()[0],'.2f'))
		mem_mean=str(format(self.meanmem()[0],'.2f'))
		title = "Nodo: " + self.name + " Exalogic " 
		img1 = cf.variables['graph_dir'] + "/" + self.name + "/" + self.name + "_cpu.png"
		textimg1 = "Promedio de consumo CPU: " + cpu_mean + "%"
		img2 = cf.variables['graph_dir'] + "/" + self.name + "/" + self.name + "_mem.png"
		textimg2 = "Promedio de Memoria: " + mem_mean + "%"
		pptxr.twoimageslidepptx(title,img1,img2,textimg1,textimg2)	

