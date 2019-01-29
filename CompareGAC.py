## Uncomment for Jupyter notebook:
## %matplotlib inline 
import pandas
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rc('font', family='sans-serif', size=16)
# Set styles and colors:
mpl.rcParams['errorbar.capsize'] = 3
mpl.rcParams['lines.linewidth'] = 3
#mpl.rcParams['lines.color'] = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
# ['b', 'g', 'r', 'c', 'm', 'y', 'k']
mpl.rcParams['lines.dashed_pattern']=[2.8, 1.2]
mpl.rcParams['lines.dashdot_pattern']=[4.8, 1.2, 0.8, 1.2]
mpl.rcParams['lines.dotted_pattern']=[1.1, 1.1]
mpl.rcParams['lines.scale_dashes']=True


data18 = pandas.read_excel('18_data_all.xlsx')
data19 = pandas.read_excel('190125_data_allapps.xlsx')

p1=data18['Institution 1 GPA Score'].fillna(-10.)
p2=data19['Institution 1 GPA Score'].fillna(-10.)

# start with a rectangular Figure
fig, ax = plt.subplots(1,figsize=(10, 6))

goodNbins, xmin, xmax = 20, 2.0, 4.0
title="Main Title"
xtitle=p1.name
ytitle="y title"

def plot_statbox(ax=None,xpos=0.90,ypos=0.90,name="",nentries=0,mean=0.,median=0.,mode=0.,c='k'):
	ax.text(xpos,ypos,'%12s\n%-7s %5i\n%-7s %4.2f \n%-7s %4.2f'%(name.center(12),'Entries',nentries,'Mean',mean,'Median',median),fontsize=10,label=name,bbox={'facecolor':'white', 'pad':3})

ax.hist(p1, goodNbins, density=True, range=[xmin,xmax], lw=3, histtype='step', label='2018')
ax.hist(p2, goodNbins, density=True, range=[xmin,xmax], lw=3, histtype='step', label='2019')
# alpha is the transparency of the data points (patch)
# normed=1 makes the y axis the fraction of events
# plt.axis([0, 400, 0, 0.01]) # sets the ranges for the x and y axis. This command overrides the range inside hist
ax.grid()
leg=ax.legend(fontsize=14,loc=2)
plot_statbox(ax,4.1,1.,'2018',len(p1),np.mean(p1),np.median(p1),0.,c='r')
plot_statbox(ax,4.1,0.7,'2019',len(p2),np.mean(p2),np.median(p2),0.,c='g')
ax.set_title(title, size = 18)
ax.set_xlabel(xtitle, size = 16)
ax.set_ylabel(ytitle, size= 16)
fig.savefig('first.png')
