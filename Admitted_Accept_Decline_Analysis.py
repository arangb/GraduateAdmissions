import pandas
import numpy as np
import matplotlib.pyplot as plt
plt.rc('font', family='sans-serif', size=16)

apps = pandas.read_excel('2020_offerstatus_scores_all.xlsx')

DOff = apps[apps['Decision Status'].isin(['ADMIT','ADMIT/ACCEPT','ADMIT/DECLINE'])]
score_list = DOff['AVE']

x_scores=np.arange(4.0,min(score_list),-0.1)
score_change_index=[]
for x in x_scores:
	# find index where this score first appears:
	i=score_list[score_list<=x].idxmax()
	score_change_index.append(i)
print(x_scores,score_change_index)
# Plot histogram of accepts per rank
accepts = apps[apps['Decision Status']=="ADMIT/ACCEPT"].reset_index(drop = True).dropna(how='all', axis=1)
rank_list = accepts['RANK']
#print(rank_list)

fig, ax1 = plt.subplots()
ax1 = rank_list.plot.hist(bins=max(rank_list), alpha=0.8, color='black')
#ax1 = rank_list.plot.hist(bins=40, alpha=0.8, color='black')
ax1.set_xlim(0,max(rank_list)+1)
#ax1.set_ylim(0,3)
import matplotlib.ticker as ticker # otherwise it only plots at 0,50,100,150
ax1.xaxis.set_major_locator(ticker.MultipleLocator(25))
ax1.set_xlabel("Rank Number")
ax1.set_ylabel("Students")
plt.title("Rank number of accepted offers")
# add horizontal axis with score ranges on top:
ax1top=ax1.twiny()
ax1top.set_xlim(ax1.get_xlim())
ax1top.set_xticks(score_change_index)
x_spaced_labels=[] # we need to skip a few labels if they are too close to each other in rank
for i in range(len(score_change_index)):
	if i == len(score_change_index)-1: # the last case which involves a i+1 and would crash the loop
		if x_spaced_labels[i-1] == '': # if previous is empty, fill it
			x_spaced_labels.append("{:0.1f}".format(x_scores[i]))
		else:
			x_spaced_labels.append('')
	else:
		if score_change_index[i+1]-score_change_index[i] > 9: 
			x_spaced_labels.append("{:0.1f}".format(x_scores[i]))
		else:
			x_spaced_labels.append('')
#print(x_spaced_labels)
ax1top.set_xticklabels(x_spaced_labels)
ax1top.set_xlabel("Average Score")
#plt.savefig("accepted_rank.png") 

# Print how many accepts we have in the first rank levels: 
first=[25,50,75,100,125]
print('%8s %5s  %-4s'%('Rank <','Count','%'))
for f in first:
	tot=len(rank_list)
	count=len(rank_list[rank_list<f])
	print('%8i %3i  %-.2f%%'%(f,count,count/tot*100))

# Now plot the cumulative fraction vs rank:
x=np.arange(0, max(rank_list)+1)
x_perc_acc=[]
for i in x:
	count=len(rank_list[rank_list<=i]) # how many students below
	x_perc_acc.append(count/tot) # fraction of students

#plt.figure()
ax2 = ax1.twinx()  # instantiate a second ax that shares the same x-axis
color = 'tab:red'
ax2.plot(x,x_perc_acc,'-',lw=3,color=color)
ax2.set_ylim(ax1.get_ylim()) # match y axis too
ax2.grid()
ax2.set_ylabel('Cumulative fraction of accepts',color=color)
ax2.tick_params(axis='y', labelcolor=color)
fig.tight_layout()
plt.savefig("perc_acc_per_rank.png")

# Make table of universities
u = apps[~apps['School Attending - if known'].isin(['unknown','Unknown'])] # remove any row with "unknown"
u = u['School Attending - if known'].dropna() # drop any empty cells
print(u.value_counts().sort_index(ascending=True).sort_values(ascending=False))

# Print numbers for GACHistory.xlsx
NDomOff = DOff['Citizenship'].str.contains(r'US|PR').sum()
NDomOffWom = len(DOff[((DOff['Citizenship'] == 'US') | (DOff['Citizenship'] == 'PR')) & (DOff['Sex'] == 'F')])
NDomOffURM = len(DOff[((DOff['Citizenship'] == 'US') | (DOff['Citizenship'] == 'PR')) & (DOff['URM'] == 'Yes')])
#print(len(DOff),NDomOff,NDomOffWom,NDomOffURM)
DIntOff = DOff[~DOff['Citizenship'].str.contains(r'US|PR')]
NIntOffWom = len(DIntOff[DIntOff['Sex'] == 'F'])
NIntOffURM = len(DIntOff[DIntOff['URM'] == 'Yes'])
#print(len(DIntOff),NIntOffWom,NIntOffURM)
DAcc = apps[apps['Decision Status'].isin(['ADMIT/ACCEPT'])]
NDomAcc = DAcc['Citizenship'].str.contains(r'US|PR').sum()
NDomAccWom = len(DAcc[((DAcc['Citizenship'] == 'US') | (DAcc['Citizenship'] == 'PR')) & (DAcc['Sex'] == 'F')])
NDomAccURM = len(DAcc[((DAcc['Citizenship'] == 'US') | (DAcc['Citizenship'] == 'PR')) & (DAcc['URM'] == 'Yes')])
#print(len(DAcc),NDomAcc,NDomAccWom,NDomAccURM)
DIntAcc = DAcc[~DAcc['Citizenship'].str.contains(r'US|PR')]
NIntAccWom = len(DIntAcc[DIntAcc['Sex'] == 'F'])
NIntAccURM = len(DIntAcc[DIntAcc['URM'] == 'Yes'])
#print(len(DIntAcc),NIntAccWom,NIntAccURM)
labels=['Domestic','DomWom','DomURM','DomOff','DomOffWom','DomOffURM','DomAcc','DomAccWom','DomAccURM','International','IntlWom','IntlURM','IntlOff','IntlOffWom','IntlOffURM','IntlAcc','IntlAccWom','IntlAccURM']
numbers=[np.nan,np.nan,np.nan,NDomOff,NDomOffWom,NDomOffURM,NDomAcc,NDomAccWom,NDomAccURM,np.nan,np.nan,np.nan,len(DIntOff),NIntOffWom,NIntOffURM,len(DIntAcc),NIntAccWom,NIntAccURM]
print(labels)
print("\t".join(str(x) for x in numbers))  # you can copy paste this from the terminal to the spreadsheet
