import pandas
import numpy as np
import matplotlib.pyplot as plt
import json
US_states = json.load(open('us_states_list.json'))
plt.rc('font', family='sans-serif', size=16)

apps = pandas.read_excel('2020_offerstatus_scores_all.xlsx')
#apps = pandas.read_excel('~/GAC19/GraduateAdmissions/190215_scores_all.xlsx')

DOff = apps[apps['Decision Status'].isin(['ADMIT','ADMIT/ACCEPT','ADMIT/DECLINE'])]
scores_off = DOff['AVE']
#-----------------------------------------------------------------------
# Plot histogram of accepts and cumulative per rank
#-----------------------------------------------------------------------
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
x_scores=np.arange(4.0,min(scores_off),-0.1)
# Find index where this given score first appears:
score_change_index=[scores_off[scores_off<=x].idxmax() for x in x_scores]
print(x_scores,score_change_index)
ax1top=ax1.twiny()
ax1top.set_xlim(ax1.get_xlim())
ax1top.set_xticks(score_change_index)
x_spaced_labels=[] # we need to skip a few labels if they are too close to each other in rank
for i in range(len(score_change_index)):
	if i < len(score_change_index)-1: 
		if score_change_index[i+1]-score_change_index[i] > 9: 
			x_spaced_labels.append("{:0.1f}".format(x_scores[i]))
		else:
			x_spaced_labels.append('')
	else: # the last case which involves a i+1 and would crash the loop
		if x_spaced_labels[i-1] == '': # if previous is empty, fill it
			x_spaced_labels.append("{:0.1f}".format(x_scores[i]))
		else:
			x_spaced_labels.append('')
# for i in range(len(score_change_index)):
	# if i == 0:
		# x_spaced_labels.append("{:0.1f}".format(x_scores[i]))
	# else: 
		# if score_change_index[i]-score_change_index[i-1] > 10: 
			# x_spaced_labels.append("{:0.1f}".format(x_scores[i]))
		# else:
			# x_spaced_labels.append('')
print(x_spaced_labels)
ax1top.set_xticklabels(x_spaced_labels) # if we just put ["{:0.1f}".format(x) for x in x_scores], some ticks are too close to each other and overlap
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

#-----------------------------------------------------------------------
# Plot histogram of accepts per score
#-----------------------------------------------------------------------
score_list = accepts['AVE']
#print(score_list)
plt.figure()
#my_bins=[3.0,3.2,3.4,3.6,3.8,3.9,4.0] 
# Just add 3.9 between 3.8 and 4.0, then go down to the minimum value in steps of 0.2
my_bins=np.flip( np.concatenate(([4.0,3.9,3.8],np.arange(3.6,min(scores_off),-0.2)),axis=0) )
print(my_bins)
hoff,hoff_bins,op = plt.hist(scores_off, bins=my_bins, color='black', lw=3,
                    histtype='step', label='Offered N='+'{:<3}'.format(len(scores_off)))
hacc,hacc_bins,ap = plt.hist(score_list, bins=my_bins, color='tab:red', lw=3,
                    histtype='step', label='Accepted N='+'{:<3}'.format(len(score_list)))
# Write the accepted percentage with respect to the offers in each bin:
for idx, c in enumerate(hacc):
	perc='{:2}%'.format(int(c*100/hoff[idx]))
	bincenter = 0.5*(hacc_bins[idx]+hacc_bins[idx+1])
	plt.annotate(perc, (bincenter, c+0.3), fontsize=12, color='tab:blue', ha='center')
	fraction='{:2}%'.format(int(c*100/hacc.sum()))
	plt.annotate(fraction, (bincenter, c-1.), fontsize=12, color='tab:red', ha='center')
plt.xlabel("Average score")
plt.ylabel("Students")
#plt.annotate(r"$\varepsilon$=accepts/offers", (3.0,21), fontsize=14, color='tab:blue', ha='left')
plt.title(r"$\varepsilon$=accepts/offers",color='tab:blue')
plt.legend(loc='upper left')
plt.subplots_adjust(bottom=0.12,top=0.92,right=0.95)
plt.savefig("accoff_per_score.png")

#-----------------------------------------------------------------------
# Make table of universities they are going to
#-----------------------------------------------------------------------
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

#-----------------------------------------------------------------------
# Print number of students that come from US institutions:
#-----------------------------------------------------------------------
print( len(DAcc[DAcc['Institution 1 Location'].isin(US_states)]), 'come from US Universities')
