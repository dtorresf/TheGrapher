#!/usr/local/bin/python3.5

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

###### Variables

csvfile = "test09.csv"


##### Colocar Cabecera Sobre archivo 

# read the current contents of the file
f = open(csvfile)
text = f.read()
f.close()
# open the file again for writing
f = open(csvfile, 'w')
f.write("name,date,mem,cpu,esta,timew,closew,finw1,finw2,proc,openf\n")
# write the original contents
f.write(text)
f.close()

#### Remover %
"""
# open the source file and read it
fh = file(csvfile, 'r')
subject = fh.read()
fh.close()

# create the pattern object. Note the "r". In case you're unfamiliar with Python
# this is to set the string as raw so we don't have to escape our escape characters
pattern = re.compile(r'%,')
# do the replace
result = pattern.sub("('',", subject)

# write the file
f_out = file('test.sql', 'w')
f_out.write(result)
f_out.close()
"""

#### Colores 

# These are the "Tableau 20" colors as RGB.  
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),  
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),  
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),  
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),  
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]  

# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.  
for i in range(len(tableau20)):  
    r, g, b = tableau20[i]  
    tableau20[i] = (r / 255., g / 255., b / 255.)  

#### Graficos

data=pd.read_csv(csvfile,parse_dates=['date'],dayfirst=True)
mydata=data[['date','cpu']]
mydata.plot(x='date', y='cpu', color=tableau20[10])


#### Promedios 

datamean=data.mean()

#print(datamean['cpu'])


plt.show()