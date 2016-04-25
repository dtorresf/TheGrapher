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
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import os
import Config
from pptx import Presentation

def grouped(list, n):
	return zip(*[iter(list)]*n)

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

def graph(data,x,y,name,cf):
	'''The function that does the magic, graphs x vs y'''
	param_graph_dir = cf.variables['graph_dir']
	graph_dir= param_graph_dir + '/' + name + '/'

	if not os.path.exists(graph_dir):
		os.mkdir(graph_dir) 
	graph_name=graph_dir + name + '_' + y + '.png'
	data_to_plot=data[[x,y]]
	ax=data_to_plot.plot(x=x, y=y)
	fig = ax.get_figure()
	fig.savefig(graph_name)
	plt.close(fig)
	

def generatepptxreport(cf,servers):

	report_name = cf.variables['pptx_report']
	#Title presentation

	prs = Presentation(cf.variables['pptx_template'])
	title_slide = prs.slides[0]
	title = title_slide.shapes.title
	title.text = "Informe de desempeño de nodos Exalogic"
	placeholder_content = title_slide.placeholders[1]
	placeholder_content.text = 'EXALOGIC THE GRAPHER REPORT'

	#Slide with images 

	for s in servers:
		cpu_mean = str(s.meancpu()[0])
		mem_mean = str(s.meanmem()[0])

		image_slide = prs.slides.add_slide(prs.slide_layouts[25])
		title = image_slide.shapes.title
		title.text = "Node " + s.name + " Exalogic Report" 
		
		placeholder = image_slide.placeholders[1] #Capture first image placeholder for CPU
		image = cf.variables['graph_dir'] + "/" + s.name + "/" + s.name + "_cpu.png"
		picture = placeholder.insert_picture(image)
		image_slide.placeholders[2].text = "Promedio de consumo CPU: " + cpu_mean
		
		placeholder = image_slide.placeholders[13]  # idx key, not position
		image = cf.variables['graph_dir'] + "/" + s.name + "/" + s.name + "_mem.png"
		picture = placeholder.insert_picture(image)
		image_slide.placeholders[14].text = "Promedio de Memoria: " + mem_mean

	prs.save(report_name)
