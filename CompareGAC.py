''' Aran Garcia-Bellido (February 2019)
    This script will compare two (or more) datasets (from two different files, or from the same file)
    overlaying plots relevant to the GAC process like the GPA score, GRE subject score, the 
    recommender rankings, the declared interests, the University rankings, and the nationalities. 
    It is easily expandable to include several datasets or new variables to plot from the spreadsheet.
'''
## Uncomment for Jupyter notebook:
## %matplotlib inline 
import pandas
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from Analytics import get_URankCountsDictionary, get_RecLettScore,normalize_GPA

f1=pandas.read_excel('18_data_all.xlsx')
f2=pandas.read_excel('190215_scores_all.xlsx')
d1=f1[(f1['Institution 1 GPA Score']>0)].reset_index(drop = True)
d1=d1[(d1['GRE Quantitative']>0)].reset_index(drop = True)
d2=f2
#d2=f2[(f2['STATUS']=='ADMIT')].reset_index(drop = True)
#d4=f2[(f2['Citizenship']=='FN')].reset_index(drop = True)
#f1=pandas.read_excel('18_data_all.xlsx')
#f2=pandas.read_excel('190125_data_allapps.xlsx')
#d1=f1[(f1['Citizenship']=='US') | (f1['Citizenship']=='PR')].reset_index(drop = True)
#d2=f2[(f2['Citizenship']=='US') | (f2['Citizenship']=='PR')].reset_index(drop = True)
#d3=f1[(f1['Citizenship']=='FN')].reset_index(drop = True)
#d4=f2[(f2['Citizenship']=='FN')].reset_index(drop = True)
#datasets=[d1,d2,d3,d4] # hlabels=['2018 US','2019 US', '2018 FN', '2019 FN']
datasets=[d1,d2]
hlabels=['2018','2019']
variables_to_plot = ['Institution 1 GPA Score','GRE Subject Total Score %','GRE Quantitative Percentile','Recommender']
variables_histp = [[20,2.5,4.0,2],[20,0,100,2],[20,0,100,2],[30,0,30,1]] # the parameters [Nbins, xmin, xmax, legloc] for each histogram/variable
#hcolors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
hcolors = ['#1f77b4', '#ff7f0e','#1f77b4', '#ff7f0e']
hstyles = ['-','-','--','--',':',':'] # ['-','--',':','-.']

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

def plot_statbox(ax=None,xpos=0.90,ypos=0.90,name="",nentries=0,mean=0.,median=0.,mode=0.,c='k'):
	# The transform=ax.transAxes makes the absolute coordinates with 0,0 = lower left and 1,1 = upper right
	ax.text(xpos,ypos,'%14s\n%-7s %6i\n%-7s %5.2f \n%-7s %5.2f'%(name.center(12),'Entries',nentries,'Mean',mean,'Median',median),fontsize=12,label=name,bbox={'facecolor':'white', 'pad':3},transform=ax.transAxes,color=c)
	
for n,v in enumerate(variables_to_plot):
	# start with a rectangular Figure
	fig, ax = plt.subplots(1,figsize=(10, 6))
	goodNbins, xmin, xmax, legloc = variables_histp[n]
	for j,d in enumerate(datasets):
		title=""
		if 'Recommender' in v:
			# Translate the scores given by the recommenders:
			recs={'Among the very best': 1, 'Top 5%': 5., 'Top 10%': 10., 'Top Quarter': 25., 'Average': 50.}
			d=d.replace(recs.keys(),recs.values()) # replace text with numbers
			# Take the average of the 4 recommenders:
			d['AvgRecLet'] = d[['Recommender 1 Rating', 'Recommender 2 Rating', 'Recommender 3 Rating', 'Recommender 4 Rating']].mean(axis=1)
			h=d['AvgRecLet'].dropna()
			title="Scores: AB=1, 5%=5, 10%=10, TopQt=25, Avg=50"
		else:
			h=d[v].dropna()
		if 'GPA' in v:
			h=normalize_GPA(h)
		#Put some stats on the labels:
		lbltxt=hlabels[j]+': N=%3i Mean=%5.2f Median=%5.2f'%(len(h),np.mean(h),np.median(h))
		#Plot histogram:
		ax.hist(h, goodNbins, density=True, range=[xmin,xmax], lw=3, linestyle=hstyles[j], color=hcolors[j], histtype='step', label=lbltxt)
		#bboxwidth=.15
		#plot_statbox(ax,0.35+j*bboxwidth,0.8,hlabels[j],len(h),np.mean(h),np.median(h),stats.mode(h)[0][0],c=hcolors[j]) # 1.005 for boxes on the right
	xtitle=h.name
	if v=='Recommender':
		xtitle="Average of recommendation letters scores per student"
	ytitle="Normalized counts"
	ax.grid()
	leg=ax.legend(fontsize=14,loc=legloc)
	ax.set_title(title, size = 18)
	ax.set_xlabel(xtitle, size = 16)
	ax.set_ylabel(ytitle, size= 16)
	plotname="%02d"%(n+1)+'_'+xtitle.replace(' ','_').replace('[','').replace(']','').replace('%','Perct')+'.png'
	fig.savefig(plotname)

#
# Now let's plot trends with interests
#
fig, ax = plt.subplots(1,figsize=(10, 6))
#print('Check the two files have the same topic list:')
for j,d in enumerate(datasets):
	# Store unique list of student topics (to be used in pie chart)
	interests=d['App - physics_focus'].dropna()
	topics = []
	for i in interests.values:
		# Various cleanup steps for the topic list. This ensures that
		# entries with multiple topics will be properly split
		i = i.replace(".", ",")
		if not 'A/AP' in i:
			i = i.replace("/", ",")
		# Do the splitting and stuff unique topics into the topics list
		subj = i.split(",")
		for s in subj:
			s = s.strip()
			if not s in topics:
				topics.append(s)
	# Now loop through each student entry and count the interests
	#print(topics)
	topicCount = dict.fromkeys(sorted(topics),0)
	for i in interests:
		for t in sorted(topics):
			if t in i:
				topicCount[t] += 1

	print(topicCount)
	bar_width = 0.35
	x = np.arange(len(topics))
	ax.bar(x+j*bar_width, list(topicCount.values()), bar_width, color=hcolors[j],label=hlabels[j]+' N=%3i'%len(interests))
	counts=np.array(list(topicCount.values()))
	# Write the percentage with respect to the total students each year on top of the bar:
	for idx, c in enumerate(counts):
		perc='{:2}%'.format(int(c*100/np.sum(counts)))
		ax.annotate(perc, (x[idx]-bar_width+j*bar_width, c+3) ) 

ax.set_ylim(top=1.2*ax.get_ylim()[1])
xtitle='Field interests from application form'
ax.set_xlabel(xtitle,size = 16)
ax.set_ylabel('Students',size = 16)
ax.set_title('',size = 18)
ax.set_xticks(x + bar_width / 2)
ax.set_xticklabels(sorted(topics))
ax.legend(loc=2)
ax.grid()
plotname="%02d"%(n+2)+'_'+xtitle.replace(' ','_').replace('[','').replace(']','').replace('%','Perct')+'.png'
#fig.tight_layout()
fig.savefig(plotname)

#
# Now the trend of university rankings 
#
fig, ax = plt.subplots(1,figsize=(10, 6))
x=np.arange(4)
bar_width=0.3
for j,d in enumerate(datasets):
	ntot=len(d['Institution 1 Name'].dropna())
	u_tier_count,u_tier_tot=get_URankCountsDictionary(d['Institution 1 Name'].dropna())
	print(u_tier_count,u_tier_tot)
	ax.bar(x+j*bar_width, u_tier_count.values(), bar_width, color=hcolors[j], label=hlabels[j]+' N=%3i'%ntot)

ax.set_xlabel('Carnegie Classification of University of applicant, as of 2018',size = 16)
ax.set_ylabel('Students',size = 16)
ax.set_title('Top Liberal Arts colleges from Times Higher Education',size = 18)
ax.text(0.4,0.95,"R1: Doctoral Highest Research [N=%3i]"%u_tier_tot['R1'],transform=ax.transAxes)
ax.text(0.4,0.9,"R2: Doctoral Higher Research [N=%3i]"%u_tier_tot['R2'],transform=ax.transAxes)
ax.text(0.4,0.85,"R3: Doctoral Moderate Research [N=%3i]"%u_tier_tot['R3'],transform=ax.transAxes)
ax.set_xticks(x + bar_width / 2)
ax.set_xticklabels(u_tier_count.keys())
ax.set_ylim(top=1.2*ax.get_ylim()[1])
ax.legend(loc=2)
ax.grid()
plotname="%02d"%(n+3)+'_UniversityResearchTier.png'
plt.savefig(plotname)
#
# Now the trend of nationalities 
#
fig, ax = plt.subplots(1,figsize=(10, 6))
fig.subplots_adjust(bottom=0.2) # make room for big country names
bothnames=[]
for j,d in enumerate(datasets):
	natcount=d.groupby('Citizenship1').Citizenship1.count() # counts for each unique country
	bignatcount=natcount[natcount>4] # only include countries with more than 4 students
	#print(type(bignatcount))
	names=[x for x,v in bignatcount.items()]
	bothnames+=names
# Now remove duplicate entries from bothnames and sort alphabetically:
natnames=sorted(list(set(bothnames)))
x=np.arange(len(natnames))
bar_width=0.4
# Ok, now we have the country names, we can go back and count the entries:
for j,d in enumerate(datasets):
	n_us=len(d[(d['Citizenship']=='US') | (d['Citizenship']=='PR')]['Citizenship'].dropna())
	n_fn=len(d[(d['Citizenship']=='FN')]['Citizenship'].dropna())
	natcount=d.groupby('Citizenship1').Citizenship1.count() # counts for each unique country
	y=[]
	for nat in natnames:
		if nat in natcount.index: # in case one country is in one dataset but not the other!
			y.append(natcount[nat])
		else:
			y.append(0)
	print(dict(zip(natnames, y)))
	ax.bar(x+j*bar_width, y, bar_width, color=hcolors[j], label=hlabels[j]+' US=%3i FN=%3i'%(n_us,n_fn))
	
#ax.set_xlabel('',size = 16)
ax.set_ylabel('Students',size = 16)
ax.set_title('(Main) Nationalities of applicants',size = 18)
ax.set_xticks(x + bar_width / 2)
ax.set_xticklabels(natnames,rotation=45)
#ax.set_ylim(top=1.2*ax.get_ylim()[1])
ax.legend(loc=2)
ax.grid()
plotname="%02d"%(n+4)+'_Nationalities.png'
plt.savefig(plotname)
