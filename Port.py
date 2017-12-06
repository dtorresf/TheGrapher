import Methods
import pandas as pd

class Port:
	'''Class that represents a Port from a Switch with atributtes to graph
	'''
	def __init__(self):
		self.name = ''
		self.switchname = ''
		self.rx = pd.DataFrame()
		self.tx = pd.DataFrame()

	def meanrx(self):
		return self.rx.mean()
	def meantx(self):
		return self.tx.mean()
	def importdatatoport(self,csvfile,cf):
		'''The function that imports data from CSV file to a Port'''
		'''The head variable must be global and is on the config file'''
		head = cf.variables['switch_head']
		Methods.addheadformat(csvfile,head)
		data=pd.read_csv(csvfile,parse_dates=['date'],dayfirst=True)
		port_data = data[['port']]
		name_data = data[['name']]
		port_value = port_data.values
		name_value = name_data.values
		port = str(port_value[0])
		name = str(name_value[0])

		#Convert to KB from bytes 
		Methods.dividedfcolumn(data,'rxb',1024)
		Methods.dividedfcolumn(data,'txb',1024)

		self.name = port[2:-2]
		self.switchname = name[2:-2]
		self.rx = data[['date','rxb']]
		self.tx = data[['date','txb']]