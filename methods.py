'''
TheGrapher takes custom generated CSV files with Exalogic's compute nodes and 
IB Switches's information, loads them into python structures and graphs the variables
recolected. 

Copyright (C) 2016  Daniela Torres Faria 
GitHub: dtorresf
Mail: daniela.torres.f@gmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later versi
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more detai
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''

import csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib
matplotlib.style.use('ggplot')
import os
import Config
from pptx import Presentation
from datetime import datetime
import sys

def grouped(list, n):
	return zip(*[iter(list)]*n)

def dividedfcolumn(df,column,scalar):
	df[column] = df[column].apply(lambda x: x/scalar)

def addheadformat(csvfile, head):
	'''Adds the head format to the CSV file. Validates existence of the head'''
	with open(csvfile, 'r') as file:
		first_line = file.readline()
		if 'name' not in first_line:
			f = open(csvfile)
			text = f.read()
			f.close()
			# open the file again for writing
			f = open(csvfile, 'w')
			f.write(head)
			# write the original contents
			f.write(text)
			f.close()

def graph3(data,x,y,name,cf):
	'''The function that does the magic, graphs x vs y'''
	param_graph_dir = cf.variables['graph_dir']
	graph_dir= param_graph_dir + '/' + name + '/'

	try:
		if not os.path.exists(graph_dir):
			os.mkdir(graph_dir) 
		graph_name=graph_dir + name + '_' + y + '.png'
		data_to_plot=data[[x,y]]
		ax=data_to_plot.plot(x=x, y=y)
		fig = ax.get_figure()
		fig.savefig(graph_name)
		plt.close(fig)
	except TypeError:
		print("ERROR: Bad data file format, please validate data for node: ",name)
		sys.exit(1)

def graph(data,x,y,name,cf,ylabel,color):
	'''The function that does the magic, graphs x vs y'''
	param_graph_dir = cf.variables['graph_dir']
	graph_dir= param_graph_dir + '/' + name + '/'

	try:
		if not os.path.exists(graph_dir):
			os.mkdir(graph_dir) 
		graph_name=graph_dir + name + '_' + y + '.png'
		data_to_plot=data[[x,y]]
		s = pd.Series(data_to_plot[y]).ewm(span=60).mean()
		data_to_plot[y] = s
		if y == 'cpu' or y == 'mem' or y == 'Average percent':
			ax=data_to_plot.plot(x=x, y=y,legend=False,ylim=(0,100),color=color)
			plt.axhline(y=60, xmin=0, xmax=1, hold=None,color='gold')
			plt.axhline(y=80, xmin=0, xmax=1, hold=None,color='darkred')
		else:
			ax=data_to_plot.plot(x=x, y=y,legend=False,color=color)
		ax.set_xlabel("Fecha")
		ax.set_ylabel(ylabel)
		fig = ax.get_figure()
		fig.savefig(graph_name)
		plt.close(fig)
	except TypeError:
		print("ERROR: Bad data file format, please validate data for node: ",name)
		sys.exit(1)

def generatepptxreport(cf,servers,switches,zfs):

	date = datetime.now().strftime("%d%m%Y-%H%M%S")
	report_name = cf.variables['pptx_report'] + '/' + 'Exalogic_Report_'+ date + '.pptx'
	#Title presentation

	prs = Presentation(cf.variables['pptx_template'])
	title_slide = prs.slides[0]
	title = title_slide.shapes.title
	title.text = "Informe de desempeño de nodos Exalogic"
	placeholder_content = title_slide.placeholders[1]
	placeholder_content.text = 'EXALOGIC THE GRAPHER REPORT - ' + date 

	#Slide with images for Servers

	for s in servers:
		cpu_mean=str(format(s.meancpu()[0],'.2f'))
		mem_mean=str(format(s.meanmem()[0],'.2f'))

		image_slide = prs.slides.add_slide(prs.slide_layouts[25])
		title = image_slide.shapes.title
		title.text = "Nodo: " + s.name + " Exalogic " 
		
		placeholder = image_slide.placeholders[1] #Capture first image placeholder for CPU
		image = cf.variables['graph_dir'] + "/" + s.name + "/" + s.name + "_cpu.png"
		picture = placeholder.insert_picture(image)
		image_slide.placeholders[2].text = "Promedio de consumo CPU: " + cpu_mean + "%"
		
		placeholder = image_slide.placeholders[13]  # idx key, not position
		image = cf.variables['graph_dir'] + "/" + s.name + "/" + s.name + "_mem.png"
		picture = placeholder.insert_picture(image)
		image_slide.placeholders[14].text = "Promedio de Memoria: " + mem_mean + "%"

	#Slide with images for Switches

	for sw in switches:
		ports = sw.ports
		for p in ports:	
			rx_mean=str(format(p.meanrx()[0],'.2f'))
			tx_mean=str(format(p.meantx()[0],'.2f'))

			image_slide = prs.slides.add_slide(prs.slide_layouts[25])
			title = image_slide.shapes.title
			title.text = "Switch: " + sw.name + " Puerto: " + p.name + " Exalogic " 
			
			placeholder = image_slide.placeholders[1] #Capture first image placeholder for TX
			image = cf.variables['graph_dir'] + "/" + sw.name + "/" + sw.name + "_" + p.name + "_rx.png"
			picture = placeholder.insert_picture(image)
			image_slide.placeholders[2].text = "Promedio: " + rx_mean + "Kbps"
			
			placeholder = image_slide.placeholders[13]  # idx key, not position
			image = cf.variables['graph_dir'] + "/" + sw.name + "/" + sw.name + "_" + p.name + "_tx.png"
			picture = placeholder.insert_picture(image)
			image_slide.placeholders[14].text = "Promedio: " + tx_mean + "Kbps"

	#Slide with images for ZFS storage 

	arc_mean=str(format(zfs.meanarc()[0],'.2f'))
	cpu_mean=str(format(zfs.meancpu()[0],'.2f'))
	mem_mean=str(format(zfs.meanmem()[0],'.2f'))
	nfsv4_mean=str(format(zfs.meannfsv4ops()[0],'.2f'))
	nw_mean=str(format(zfs.meannetwork()[0],'.2f'))

	#First slide with CPU and Mem
	image_slide = prs.slides.add_slide(prs.slide_layouts[25])
	title = image_slide.shapes.title
	title.text = "ZFS " + zfs.name + " Exalogic " 

	placeholder = image_slide.placeholders[1] #Capture first image placeholder for TX
	image = cf.variables['graph_dir'] + "/" + zfs.name + "/" + zfs.name + "_Average percent.png"
	picture = placeholder.insert_picture(image)
	image_slide.placeholders[2].text = "Promedio: " + cpu_mean + "%"
	
	placeholder = image_slide.placeholders[13]  # idx key, not position
	image = cf.variables['graph_dir'] + "/" + zfs.name + "/" + zfs.name + "_Average MB.png"
	picture = placeholder.insert_picture(image)
	image_slide.placeholders[14].text = "Promedio: " + mem_mean + "Mb"

	#Second slide with NFSV4 and ARC
	image_slide = prs.slides.add_slide(prs.slide_layouts[25])
	title = image_slide.shapes.title
	title.text = "ZFS " + zfs.name + " Exalogic " 

	placeholder = image_slide.placeholders[1] #Capture first image placeholder for TX
	image = cf.variables['graph_dir'] + "/" + zfs.name + "/" + zfs.name + "_Average operations per second.png"
	picture = placeholder.insert_picture(image)
	image_slide.placeholders[2].text = "Promedio: " + nfsv4_mean + "ops"
	
	placeholder = image_slide.placeholders[13]  # idx key, not position
	image = cf.variables['graph_dir'] + "/" + zfs.name + "/" + zfs.name + "_Average value per second.png"
	picture = placeholder.insert_picture(image)
	image_slide.placeholders[14].text = "Promedio: " + arc_mean + "ops"

	#One slide for network
	image_slide = prs.slides.add_slide(prs.slide_layouts[24])
	title = image_slide.shapes.title
	title.text = "ZFS " + zfs.name + " Exalogic " 

	placeholder = image_slide.placeholders[1] #Capture first image placeholder for TX
	image = cf.variables['graph_dir'] + "/" + zfs.name + "/" + zfs.name + "_Average KB per second.png"
	picture = placeholder.insert_picture(image)
	image_slide.placeholders[2].text = "Promedio: " + nw_mean + "Kbps"


	prs.save(report_name)
