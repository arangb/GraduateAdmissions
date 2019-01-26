
## Uncomment for Jupyter notebook:
## %matplotlib inline 
import pandas
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

mpl.rc('font', family='sans-serif', size=16)

#apps = pandas.read_excel('180108_data.xlsx')
#apps = pandas.read_excel('admitted18_stats.xlsx')
apps = pandas.read_excel('190125_data_allapps.xlsx')
# 
## Uncomment to view the entire input table.
# apps
# Make cuts:
#apps=apps[apps['GRE Subject Total Score %']>0].reset_index(drop = True)
#apps=apps[apps['Citizenship']=='US'].reset_index(drop = True)

# # GPA and GRE Breakdowns
# 
# ### Total Scores

# Plot correlation between GRE and GPA:
gres=apps['GRE Subject Total Score %'].fillna(-10.)
gpas=apps['Institution 1 GPA Score'].fillna(-10.)
normgpas=[]
print('Normalizing GPAs:')
for g in gpas:
    if g>4.0 and g<=5.0:
        print(g,g*4./5.)
        normgpas.append(g*4./5.)
    elif g>5.0 and g<=10.0:
        print(g,g*4./10.)
        normgpas.append(g*4./10.)
    elif g>10.0 and g<=20.0:
        print(g,g*4./20.)
        normgpas.append(g*4./20.)
    elif g>20. and g<=100.:
        print(g,g*4./100.)
        normgpas.append(g*4./100.)
    else:
        normgpas.append(g)
apps['Normalized GPA'] = normgpas
# definitions for the axes
left, width = 0.1, 0.65
bottom, height = 0.1, 0.65
bottom_h = left_h = left + width + 0.02

rect_scatter = [left, bottom, width, height]
rect_histx = [left, bottom_h, width, 0.2]
rect_histy = [left_h, bottom, 0.2, height]

# start with a rectangular Figure
plt.figure(1, figsize=(10,10))

axScatter = plt.axes(rect_scatter)
axHistx = plt.axes(rect_histx)
axHisty = plt.axes(rect_histy)

# the scatter plot:
axScatter.scatter(gres, normgpas)
axScatter.set_xlabel("GRE Subject Total Score %")
axScatter.set_ylabel("Undergrad GPA")

# now determine nice limits by hand:
binwidth = 0.2
xymax = np.max([np.max(np.fabs(gres)), np.max(np.fabs(normgpas))])
lim = (int(xymax/binwidth) + 1) * binwidth
axScatter.set_xlim((0, 100))
axScatter.set_ylim((2.7, 4))
#print(lim)

axHistx.hist(gres.dropna(), bins=np.arange(0, lim + 10, 10))
axHistx.axes.xaxis.set_ticklabels([]) # remove x axis labels on top plot
axHisty.hist(gpas.dropna(), bins=np.arange(0, lim + 0.2, 0.2), orientation='horizontal')
axHisty.axes.yaxis.set_ticklabels([]) # remove y axis labels on right plot
axHistx.set_xlim(axScatter.get_xlim())
axHisty.set_ylim(axScatter.get_ylim())

plt.savefig('00GAC-GPAGREcorr-projections.png')

print('\nGRE Mean = %5.3f, Median = %5.3f percentile'%(np.mean(gres[gres>0]),np.median(gres[gres>0])))
print('GPA Mean = %5.3f, Median = %5.3f \n'%(np.mean(normgpas[normgpas>0]),np.median(normgpas[normgpas>0])))

plt.figure() # New figure
fig, ax = plt.subplots(figsize=(10, 10))
# Plot correlation between GRE and GPA:
gres=apps['GRE Subject Total Score %'].fillna(-10) # just in case there are empty values
gpas=apps['Normalized GPA'].fillna(-10)   # idem
universities=apps['Institution 1 Name']
#print(gres[1],gpas[1])
plt.scatter(gres,gpas,color='blue',s=5,edgecolor='none')
for i, txt in enumerate(universities):
	#print(i,gres[i],gpas[i],txt)
	ax.annotate(txt, (gres[i],gpas[i]), size='x-small')

plt.xlabel("GRE Subject Total Score %")
plt.ylabel("Undergrad GPA")
plt.ylim(3.2,4.02)
plt.tight_layout()
plt.savefig('00GAC-GPAGREcorr-scatter.png')


axes = apps.hist(column=['GRE Verbal Percentile',
                         'GRE Subject Total Score %',
                         'GRE Analytical Writing Percentile',
                         'GRE Quantitative Percentile'],
                   sharex=True,
                   sharey=True,
                   bins=np.linspace(0,100,11),
                   color='royalblue',
                   histtype='stepfilled',
                   figsize=(10,7))

fig = plt.gcf()
fig.tight_layout()
fig.savefig("01GAC-GREBreakdown.png")

# ### Breakdown by Gender

# Print nice table with summary of gender and race
# Sometimes Laura uses "Sex" and sometimes "Gender" in her spreadsheets
print(pandas.crosstab(apps.Sex,apps.Race.fillna('N/R'),margins=True)) # <-- Check name of column: Sex or Gender

gres = ['GRE Analytical Writing Percentile',
        'GRE Quantitative Percentile',
        'GRE Subject Total Score %',
        'GRE Verbal Percentile']
fig, axes = plt.subplots(2, 2, figsize=(10,7), sharex=True, sharey=True)

for ax, gre in zip(axes.flatten(), gres):
    scores = apps.dropna(subset=[gre])
    men = scores['Sex'] == 'M'   # <-- Check name of column: Sex or Gender
    women = np.logical_not(men)
    ax.hist(scores[gre][men],
            bins=np.linspace(0, 100, 11),
            histtype='stepfilled',
            label='Men',
            alpha=0.5)
    ax.hist(scores[gre][women],
            bins=np.linspace(0, 100, 11),
            histtype='stepfilled',
            label='Women',
            alpha=0.5)
    
    ax.set(title=gre)
    ax.grid()
    
    leg=ax.legend(fontsize=12, loc=2)

fig.tight_layout()
fig.savefig("02GAC-GenderBreakdown.png")

# ### URM Breakdown

# Print nice table with summary of gender and URM
print(pandas.crosstab(apps.Sex,apps.URM.fillna('N/R'),margins=True))

gres = ['GRE Analytical Writing Percentile',
        'GRE Quantitative Percentile',
        'GRE Subject Total Score %',
        'GRE Verbal Percentile']
fig, axes = plt.subplots(2, 2, figsize=(10,7), sharex=True, sharey=True)

for ax, gre in zip(axes.flatten(), gres):
    scores = apps.dropna(subset=[gre])
    urm = scores['URM'] == 'Yes'
    rep = np.logical_not(urm)
    ax.hist(scores[gre][rep],
            bins=np.linspace(0, 100, 11),
            histtype='stepfilled',
            label='Not URM',
            alpha=0.5)
    ax.hist(scores[gre][urm],
            bins=np.linspace(0, 100, 11),
            histtype='stepfilled',
            label='URM',
            alpha=0.5)
    ax.set(title=gre)
    ax.grid()
    
    leg=ax.legend(fontsize=12, loc=2)

fig.tight_layout()
fig.savefig("03GAC-URMBreakdown.png")

### Summary percentage:
Nwomen=len(apps[apps.Sex=='F']['URM'])
NURM=len(apps[apps.URM=='Yes']['URM'])
Ntot=len(apps['URM'])
print('Women: %3i/%3i=%4.2f%%'%(Nwomen,Ntot,float(Nwomen)/float(Ntot)*100.))
print('  URM: %3i/%3i=%4.2f%%'%(NURM,Ntot,float(NURM)/float(Ntot)*100.))
print(pandas.crosstab(apps.Citizenship1,apps.Sex,margins=True))

# # Categorization by Interests
# 
# Sort students by interest, dropping records where interest is not explicitly mentioned in the students' personal statement.

# Grab a full table of interests from what they clicked or based on personal statements, dropping empty values
#interests = apps['App - physics_focus'].dropna()
whichint= 'App - physics_focus'  ### 'App - physics_focus' or 'Interest narrowed from PS'
interests = apps[whichint].dropna()

# Store unique list of student topics (to be used in pie chart)
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
print('Topics found = ', topics)
# Print pretty table of topics split by Experiment/Theory/undecided
print(10*' ' + ' '.join(['%4s']*len(topics)) % tuple(topics))
thexpint=apps.dropna(subset=[whichint,'App - physics_major']) # Drop empty rows, the physics_major is Exp/Th/Undecided
for etu in ['Experiment','Theory','Undecided']:
    rownum=[]
    for t in topics:
        #This next command creates an array of True/False requiring that the string etu is found AND that the topic t is also found in that subset
        intetu=thexpint[thexpint[whichint].str.contains(t)]['App - physics_major'].str.contains(etu)
        rownum.append(np.count_nonzero(intetu)) # This just counts how many True's we have in the array intetu
    print('%10s'%etu + ' '.join(['%4i']*len(rownum)) % tuple(rownum)) # print the row with correct formatting

# Now loop through each student entry and count the interests
import operator

topicCount = {}
for t in topics:
    topicCount[t] = 0
    
total = 0
for i in interests:
    for t in topics:
        if t in i:
            topicCount[t] += 1
            total += 1

# Sort the list of student interests to go from most to least popular
topicSorted = np.asarray(sorted(topicCount.items(),
                                key=operator.itemgetter(1),
                                reverse=True))

# Make a nice pie chart.
# Define fancy colors...
colors = ["salmon",    "lightgreen", "deepskyblue",  "cornflowerblue",
          "lightblue", "papayawhip", "cyan",         "peru",
          "plum",      "gold",       "lemonchiffon", "lightgrey",
          "white"]

# ...and make the pie chart.
fig, ax = plt.subplots(1,1, figsize=(6,5))
ax.pie(topicSorted[:,1],
       labels=topicSorted[:,0],
       #autopct="%.1f",
       autopct=lambda p: '{:.0f}'.format(p * total / 100),
       colors=colors[:len(topics)],
       startangle=90)
ax.set(aspect='equal')
if whichint =='Interest narrowed from PS':
    ax.set_title('Field interests from PS')
else:
    ax.set_title('Field interests from application form')
fig.tight_layout()
fig.savefig("04GAC-PieChartInterests.png")


# ### Box/Whisker Plots of GPA and GRE, by Interest
# 
# #### The box extends from the lower to upper quartile values of the data, with a yellow line at the median. The whisker values of whis=[2.5, 97.5] 

def infoByTopic(dframe, topic, topicSorted, whichint='App - physics_focus'):
    frame = dframe.dropna(subset=[topic, whichint])
    infoByInt = {x:[] for x in topicSorted[:,0]}
    for info, top in zip(frame[topic], frame[whichint]):
        for t in topicSorted[:,0]:
            if t in top:
                infoByInt[t].append(info)

    alldat = []
    for i, t in enumerate(topicSorted[:,0]):
        data = infoByInt[t]
        alldat.append(data)
        
    return alldat


# In[80]:
print('Box = 97.5%, Tip = 2.5%')
fig, ax = plt.subplots(1,1, figsize=(8,5))
ax.boxplot(infoByTopic(apps, 'Normalized GPA', topicSorted, whichint), 0, whis=[2.5, 97.5], sym='')
ax.set_xticklabels(topicSorted[:,0], rotation=45)
ax.set(title='Institution 1 GPA (4.0 Scale)',
       ylim=(2.7,4.0),
       ylabel='GPA')
fig.tight_layout()
fig.savefig("05GAC-GPAUndergrad.png")

fig, ax = plt.subplots(1,1, figsize=(8,5))
ax.boxplot(infoByTopic(apps, 'GRE Subject Total Score %', topicSorted, whichint), 0, whis=[2.5, 97.5], sym='')
ax.set_xticklabels(topicSorted[:,0], rotation=45)
ax.set(title='GRE Subject (Physics) Total Score %',
       ylabel='percentile',
       ylim=(0,100))
fig.tight_layout()
fig.savefig("06GAC-GREPhysicsPercentile.png")

fig, ax = plt.subplots(1,1, figsize=(8,5))
ax.boxplot(infoByTopic(apps, 'GRE Quantitative Percentile', topicSorted, whichint), 0, whis=[2.5, 97.5], sym='')
ax.set_xticklabels(topicSorted[:,0], rotation=45)
ax.set(title='GRE Quantitative Percentile',
       ylabel='percentile',
       ylim=(0,100))
fig.tight_layout()
fig.savefig("07GAC-GREQuantitativePercentile.png")

fig, ax = plt.subplots(1,1, figsize=(8,5))
ax.boxplot(infoByTopic(apps, 'GRE Analytical Writing Percentile', topicSorted, whichint), whis=[2.5, 97.5], sym='')
ax.set_xticklabels(topicSorted[:,0], rotation=45)
ax.set(title='GRE Analytical Writing Percentile',
       ylabel='percentile',
       ylim=(0,100))
fig.tight_layout()
fig.savefig("08GAC-GREAnalyticalWritingPercentile.png")


fig, ax = plt.subplots(1,1, figsize=(8,5))
ax.boxplot(infoByTopic(apps, 'GRE Verbal Percentile', topicSorted, whichint), 0, whis=[50, 50], sym='')
ax.set_xticklabels(topicSorted[:,0], rotation=45)
ax.set(title='GRE Verbal Percentile',
       ylabel='percentile',
       ylim=(0,100))
fig.tight_layout()
fig.savefig("09GAC-GREAnalyticalWritingPercentile.png")

### Recommendation Letters
import scipy.stats as stats
plt.figure() # New figure
fig, ax = plt.subplots(figsize=(10, 10))
# Translate the scores given by the recommenders:
recs={'Among the very best': 1, 'Top 5%': 5., 'Top 10%': 10., 'Top Quarter': 25., 'Average': 50.}
apps=apps.replace(recs.keys(),recs.values()) # replace text with numbers
# Take the average of the 4 recommenders:
apps['AvgRecLet'] = apps[['Recommender 1 Rating', 'Recommender 2 Rating', 'Recommender 3 Rating', 'Recommender 4 Rating']].mean(axis=1)
#print(apps['AvgRecLet'])
x=apps['AvgRecLet'].dropna()
n, bins, patches = plt.hist(x, 20, range=[0,50], linewidth=3, facecolor='g', alpha=0.75, histtype='stepfilled')
# alpha is the transparency of the data points (patch)
#plt.axis([0, 400, 0, 0.01]) # sets the ranges for the x and y axis. This command overrides the range inside hist
plt.title("RecLetters: AB=1, 5%=5, 10%=10, TopQt=25, Avg=50")
plt.xlabel("Average of recommendation letters scores per student")
plt.ylabel("Students")
plt.grid()
RLmean = np.mean(x)
RLmedi = np.median(x)
RLmode = stats.mode(x)[0][0]
plt.text(35,0.85*max(n),'%-7s %4i\n%-7s %4.2f \n%-7s %4.2f\n%-7s %4.2f'%('Entries',len(x),'Mean',RLmean,'Median',RLmedi,'Mode',RLmode),fontsize=20)
#plt.xscale('log')
plt.savefig("10GAC-RecLettAvgScore.png") 
