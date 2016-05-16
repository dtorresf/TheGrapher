import Port
import sys
import csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib
matplotlib.style.use('ggplot')
import Config
from datetime import datetime
import glob
import methods
import os
import Pptxr

class Switch:
	'''Class that represents a Switch with atributtes to graph'''
	def __init__(self):
		self.name = ''
		self.nports = 0
		self.ports = list()

	def importdatatoswitch(self,nports,files,cf):
		'''The function that imports data from CSV format to Switch'''
		'''I need a function that evaluates files on a directory and gets the info of the files for the ports'''
		
		ports = list()	

		for i in range(0,nports):
			'''Fill up an array with ports'''
			p = Port.Port()
			p.importdatatoport(files[i],cf)
			ports.append(p)

		self.name = ports[0].switchname
		self.nports = nports
		self.ports = ports
	def graphswitch(self,cf):
		param_graph_dir = cf.variables['graph_dir']
		graph_dir= param_graph_dir + '/' + self.ports[0].switchname + '/'

		try:
			if not os.path.exists(graph_dir):
				os.mkdir(graph_dir) 
			for i in range(0,self.nports):
				graph_name=graph_dir + self.ports[i].switchname + '_' + self.ports[i].name
				data_to_plot1=self.ports[i].rx
				data_to_plot2=self.ports[i].tx
				s1 = pd.Series(data_to_plot1['rxb']).ewm(span=60).mean()
				data_to_plot1['rxb'] = s1
				s2 = pd.Series(data_to_plot2['txb']).ewm(span=60).mean()
				data_to_plot2['txb'] = s2
				ax= data_to_plot1.plot(x='date', y='rxb',legend=False)
				ax2= data_to_plot2.plot(x='date', y='txb',legend=False)
				ax.set_xlabel("Fecha")
				ax.set_ylabel("RX(KB)")
				ax2.set_xlabel("Fecha")
				ax2.set_ylabel("TX(KB)")
				fig = ax.get_figure()
				fig2 = ax2.get_figure()
				fig.savefig(graph_name + '_rx' + '.png')
				fig2.savefig(graph_name + '_tx' + '.png')
				plt.close(fig)
				plt.close(fig2)
		except:
			print("ERROR: Bad data file format, please validate data for switch: ",self.ports[0].switchname)
			sys.exit(1)
	def switchpptxreport(self,cf,pptxr):
		ports = self.ports
		for p in ports:	
			rx_mean=str(format(p.meanrx()[0],'.2f'))
			tx_mean=str(format(p.meantx()[0],'.2f'))
			title = "Switch: " + self.name + " Puerto: " + p.name + " Exalogic "
			img1 = cf.variables['graph_dir'] + "/" + self.name + "/" + self.name + "_" + p.name + "_rx.png"
			textimg1 = "Promedio: " + rx_mean + "Kbps"
			img2 = cf.variables['graph_dir'] + "/" + self.name + "/" + self.name + "_" + p.name + "_tx.png"
			textimg2 = "Promedio: " + tx_mean + "Kbps"
			pptxr.twoimageslidepptx(title,img1,img2,textimg1,textimg2)
