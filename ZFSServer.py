import methods 
import pandas as pd
import glob
import Pptxr

class ZFSServer:
	'''Class that represents a ZFSServer with atributtes to graph'''
	def __init__(self):
		self.name = ''
		self.mem = pd.DataFrame()
		self.cpu = pd.DataFrame()
		self.nfsv4ops = pd.DataFrame()
		self.hit = pd.DataFrame()
		self.miss = pd.DataFrame()
		self.network = pd.DataFrame()
		self.arc = pd.DataFrame()
		self.diskusge = pd.DataFrame()

	def graphcpu(self,cf):
		methods.graph(self.cpu,'Start Time (UTC)','Average percent', self.name,cf,'% CPU','darkturquoise')
	def graphmem(self,cf):
		methods.graph(self.mem,'Start Time (UTC)','Average MB', self.name,cf,'% Memory','darkturquoise')
	def graphnfsv4ops(self,cf):
		methods.graph(self.nfsv4ops,'Start Time (UTC)','Average operations per second', self.name,cf,'# NFSV4 Ops','darkturquoise')
	def graphnetwork(self,cf):
		methods.graph(self.network,'Start Time (UTC)','Average KB per second', self.name,cf,'Kbps','darkturquoise')
	def grapharc(self,cf):
		methods.graph(self.arc,'Start Time (UTC)','Average value per second', self.name,cf,'# ARC Ops','darkturquoise')
	def graphhit(self,cf):
		methods.graph(self.hit,'date', 'closewait', self.name,cf)
	def graphmiss(self,cf):
		methods.graph(self.miss,'date','finw1', self.name,cf)
	def graphdiskusage(self,cf):
		methods.graph(self.diskusage,'date','finw2', self.name,cf)
	def graphzfs(self,cf):
		self.grapharc(cf)
		self.graphcpu(cf)
		self.graphmem(cf)
		self.graphnfsv4ops(cf)
		self.graphnetwork(cf)
	def meancpu(self):
		return self.cpu.mean()
	def meanmem(self):
		return self.mem.mean()
	def meanarc(self):
		return self.arc.mean()
	def meannfsv4ops(self):
		return self.nfsv4ops.mean()
	def meanhit(self):
		return self.hit.mean()
	def meanmiss(self):
		return self.miss.mean()
	def meannetwork(self):
		return self.network.mean()
	def meandiskusage(self):
		return self.diskusage.mean()

	def importdatatozfs(self,cf):
		'''
			The function that imports data from CSV file to a ZFS.
			The order is: CPU, MEMORY, NFSV4OPS, NETWORK,ARC
		'''
		data_dir = cf.variables['data_files_dir'] + '/ZFSstatsData' +'/*.csv'
		csvfiles = glob.glob(data_dir)

		name = cf.variables['exalogic_name'] + cf.variables['exalogic_sn_prefix'] + '01'
		self.name = name

		#ARC
		data=pd.read_csv(csvfiles[0],parse_dates=['Start Time (UTC)'],dayfirst=True)
		self.arc = data[['Start Time (UTC)','Average value per second']]

		# CPU
		data=pd.read_csv(csvfiles[1],parse_dates=['Start Time (UTC)'],dayfirst=True)
		self.cpu = data[['Start Time (UTC)','Average percent']]

		#Memory
		data=pd.read_csv(csvfiles[2],parse_dates=['Start Time (UTC)'],dayfirst=True)
		self.mem = data[['Start Time (UTC)','Average MB']]

		#NFSV4OPS
		data=pd.read_csv(csvfiles[3],parse_dates=['Start Time (UTC)'],dayfirst=True)
		self.nfsv4ops = data[['Start Time (UTC)','Average operations per second']]
		
		#NETWORK
		data=pd.read_csv(csvfiles[6],parse_dates=['Start Time (UTC)'],dayfirst=True)
		self.network = data[['Start Time (UTC)','Average KB per second']]

	def zfspptxreport(self,cf,pptxr):
		arc_mean=str(format(self.meanarc()[0],'.2f'))
		cpu_mean=str(format(self.meancpu()[0],'.2f'))
		mem_mean=str(format(self.meanmem()[0],'.2f'))
		nfsv4_mean=str(format(self.meannfsv4ops()[0],'.2f'))
		nw_mean=str(format(self.meannetwork()[0],'.2f'))

		#First slide with CPU and Mem
		title = "ZFS " + self.name + " Exalogic "
		img1 = cf.variables['graph_dir'] + "/" + self.name + "/" + self.name + "_Average percent.png"
		textimg1 = "Promedio: " + cpu_mean + "%"
		img2 = cf.variables['graph_dir'] + "/" + self.name + "/" + self.name + "_Average MB.png"
		textimg2 = "Promedio: " + mem_mean + "Mb"
		pptxr.twoimageslidepptx(title,img1,img2,textimg1,textimg2)	
		#Second slide with NFSV4 and ARC
		title = "ZFS " + self.name + " Exalogic "
		img1 = cf.variables['graph_dir'] + "/" + self.name + "/" + self.name + "_Average operations per second.png"
		textimg1 = "Promedio: " + nfsv4_mean + "ops"
		img2 = cf.variables['graph_dir'] + "/" + self.name + "/" + self.name + "_Average value per second.png"
		textimg2 = "Promedio: " + arc_mean + "ops"
		pptxr.twoimageslidepptx(title,img1,img2,textimg1,textimg2)	
		#One slide for network
		title = "ZFS " + self.name + " Exalogic " 
		img = cf.variables['graph_dir'] + "/" + self.name + "/" + self.name + "_Average KB per second.png"
		textimg = "Promedio: " + nw_mean + "Kbps"
		pptxr.oneimageslidepptx(title,img,textimg)