
## Uncomment for Jupyter notebook:
## %matplotlib inline 
import pandas
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

mpl.rc('font', family='sans-serif', size=14)

#apps = pandas.read_excel('180108_data.xlsx')
apps = pandas.read_excel('admitted18_stats.xlsx')
# 
## Uncomment to view the entire input table.
# apps


# # GPA and GRE Breakdowns
# 
# ### Total Scores

# Plot correlation between GRE and GPA:
gres=apps['GRE Subject Total Score %'].fillna(0.)
gpas=apps['Institution 1 GPA Score'].fillna(0.)
normgpas=[]
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
plt.figure(1, figsize=(5,5))

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
axScatter.set_ylim((2.75, 4))
#print(lim)

axHistx.hist(gres.dropna(), bins=np.arange(0, lim + 10, 10))
axHistx.axes.xaxis.set_ticklabels([]) # remove x axis labels on top plot
axHisty.hist(gpas.dropna(), bins=np.arange(0, lim + 0.2, 0.2), orientation='horizontal')
axHisty.axes.yaxis.set_ticklabels([]) # remove y axis labels on right plot

axHistx.set_xlim(axScatter.get_xlim())
axHisty.set_ylim(axScatter.get_ylim())

plt.savefig('00GAC-GPAGREcorr-projections.png')


plt.figure() # New figure
fig, ax = plt.subplots(figsize=(10, 10))
# Plot correlation between GRE and GPA:
gres=apps['GRE Subject Total Score %'] # .fillna(-1) just in case there are empty values
gpas=apps['Normalized GPA']   # idem
universities=apps['Institution 1 Name']
#print(gres[1],gpas[1])
plt.scatter(gres,gpas,color='blue',s=5,edgecolor='none')
for i, txt in enumerate(universities):
    ax.annotate(txt, (gres[i+1],gpas[i+1]), size='x-small')

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
print(pandas.crosstab(apps.Sex,apps.Race.fillna('N/R'),margins=True))

gres = ['GRE Analytical Writing Percentile',
        'GRE Quantitative Percentile',
        'GRE Subject Total Score %',
        'GRE Verbal Percentile']
fig, axes = plt.subplots(2, 2, figsize=(10,7), sharex=True, sharey=True)

for ax, gre in zip(axes.flatten(), gres):
    scores = apps.dropna(subset=[gre])
    men = scores['Sex'] == 'M'
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
    ax.hist(scores[gre][urm],
            bins=np.linspace(0, 100, 11),
            histtype='stepfilled',
            label='URM',
            alpha=0.5)
    ax.hist(scores[gre][rep],
            bins=np.linspace(0, 100, 11),
            histtype='stepfilled',
            label='Not URM',
            alpha=0.5)
    
    ax.set(title=gre)
    ax.grid()
    
    leg=ax.legend(fontsize=12, loc=2)

fig.tight_layout()
fig.savefig("03GAC-URMBreakdown.png")


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

def infoByTopic(dframe, topic, topicSorted):
    frame = dframe.dropna(subset=[topic, 'Interest narrowed from PS'])
    infoByInt = {x:[] for x in topicSorted[:,0]}
    for info, top in zip(frame[topic], frame['Interest narrowed from PS']):
        for t in topicSorted[:,0]:
            if t in top:
                infoByInt[t].append(info)

    alldat = []
    for i, t in enumerate(topicSorted[:,0]):
        data = infoByInt[t]
        alldat.append(data)
        
    return alldat


# In[80]:

fig, ax = plt.subplots(1,1, figsize=(8,5))
ax.boxplot(infoByTopic(apps, 'Normalized GPA', topicSorted), 0, whis=[2.5, 97.5], sym='')
ax.set_xticklabels(topicSorted[:,0], rotation=45)
ax.set(title='Institution 1 GPA (4.0 Scale)',
       ylim=(2.4,4.2),
       ylabel='GPA')
fig.tight_layout()
fig.savefig("05GAC-GPAUndergrad.png")

fig, ax = plt.subplots(1,1, figsize=(8,5))
ax.boxplot(infoByTopic(apps, 'GRE Subject Total Score %', topicSorted), 0, whis=[2.5, 97.5], sym='')
ax.set_xticklabels(topicSorted[:,0], rotation=45)
ax.set(title='GRE Subject (Physics) Total Score %',
       ylabel='percentile',
       ylim=(0,100))
fig.tight_layout()
fig.savefig("06GAC-GREPhysicsPercentile.png")

fig, ax = plt.subplots(1,1, figsize=(8,5))
ax.boxplot(infoByTopic(apps, 'GRE Quantitative Percentile', topicSorted), 0, whis=[2.5, 97.5], sym='')
ax.set_xticklabels(topicSorted[:,0], rotation=45)
ax.set(title='GRE Quantitative Percentile',
       ylabel='percentile',
       ylim=(0,100))
fig.tight_layout()
fig.savefig("07GAC-GREQuantitativePercentile.png")

fig, ax = plt.subplots(1,1, figsize=(8,5))
ax.boxplot(infoByTopic(apps, 'GRE Analytical Writing Percentile', topicSorted), whis=[2.5, 97.5], sym='')
ax.set_xticklabels(topicSorted[:,0], rotation=45)
ax.set(title='GRE Analytical Writing Percentile',
       ylabel='percentile',
       ylim=(0,100))
fig.tight_layout()
fig.savefig("08GAC-GREAnalyticalWritingPercentile.png")


fig, ax = plt.subplots(1,1, figsize=(8,5))
ax.boxplot(infoByTopic(apps, 'GRE Verbal Percentile', topicSorted), 0, whis=[50, 50], sym='')
ax.set_xticklabels(topicSorted[:,0], rotation=45)
ax.set(title='GRE Verbal Percentile',
       ylabel='percentile',
       ylim=(0,100))
fig.tight_layout()
fig.savefig("09GAC-GREAnalyticalWritingPercentile.png")


# # Faculty Named in Applications
## This doesn't really work very nicely, see other macro

from collections import Counter

# Grab a full table of faculty named from personal statements, dropping empty values
fframe = apps.dropna(subset=['Faculty Named in PS'])
faculty = fframe['Faculty Named in PS']

faculty = []
for f in fframe['Faculty Named in PS']:
    names = f.split(",")
    for n in names:
        n = n.strip()
        if len(n) > 2 and n[0].isupper():
            name = 'Garcia-Bellido' if n == 'Garcia-Bellido' else n 
            faculty.append(name)
        
nameCount = Counter(faculty)
nameCount = np.asarray(sorted(nameCount.items(),
                       key=operator.itemgetter(1),
                       reverse=True))

names = []
count = []
for n, c in nameCount:
    names.append(n)
    count.append(c)

print(names)
print(count)
print(len(names))
#caca=np.arange(-1,int(count[0])) + 1
#print(caca)
fig, ax = plt.subplots(1,1, figsize=(17,6))
idx = 5 + 10*np.arange(len(names))
plt.bar(idx, count, width=5, align='center', fc='royalblue')
plt.xticks(idx, names)
plt.ylabel('count')
plt.title('Interest by Personal Statement')
plt.xlim(1,idx[-1]+4)
#ax.set(xlim=(idx[0], idx[-1]+5),
#       xticks=idx+2.5,
#       xticklabels=names,
       #ylim=(-1,int(count[0])+0.5),
#       yticks=np.arange(0,int(count[0])) + 1,
#       ylabel='count',
#       title='Interest by Personal Statement')
#ax.grid()
plt.xticks(rotation=80)
fig.tight_layout();


from collections import Counter

# Grab a full table of faculty named from personal statements, dropping empty values
fframe = apps.dropna(subset=['Faculty Named in PS'])
faculty = fframe['Faculty Named in PS']

faculty = []
for f in fframe['Faculty Named in PS']:
    names = f.split(",")
    for n in names:
        n = n.strip()
        if len(n) > 2 and n[0].isupper():
            name = 'Garcia-Bellido' if n == 'Garcia-Bellido' else n 
            faculty.append(name)
        
nameCount = Counter(faculty)
nameCount = np.asarray(sorted(nameCount.items(),
                       key=operator.itemgetter(1),
                       reverse=True))

names = []
count = []
for n, c in nameCount:
    names.append(n)
    count.append(c)

print(names,count)
caca=np.arange(-1,int(count[0])) + 1
print(caca)
fig, ax = plt.subplots(1,1, figsize=(17,6))
idx = 5 + 10*np.arange(len(names))
ax.bar(idx, count, width=5, fc='royalblue')
ax.set(xlim=(idx[0], idx[-1]+5),
       xticks=idx+2.5,
       xticklabels=names,
       #ylim=(-1,int(count[0])+0.5),
       yticks=np.arange(0,int(count[0])) + 1,
       ylabel='count',
       title='Interest by Personal Statement')
ax.grid()
plt.xticks(rotation=80)
fig.tight_layout();


# ## Faculty Interest Word Cloud
# 
# This is eye candy which is kind of fun to show at faculty meetings. In 2017 I wanted to show the key areas of interest (mainly LLE + various QO faculty).
# 
# Note that in one spot below I manually loaded a font file from my local installation of X. This will vary on other systems so change the path or comment out the font_path keyword argument as needed and it should work on your system.

faculty = []
for f in fframe['Faculty Named in PS']:
    names = f.split(",")
    for n in names:
        n = n.strip()
        if len(n) > 2 and not n[0].islower():
            name = 'Garcia_Bellido' if n == 'Garcia-Bellido' else n 
            faculty.append(name)
            
wordcloud = WordCloud(font_path='/opt/X11/share/fonts/TTF/VeraMono.ttf',
                      stopwords=STOPWORDS,
                      background_color='black',
                      width=1200,
                      height=1000,
                      prefer_horizontal=0.8,
                      relative_scaling=1.,
                      max_font_size=300,
                      ).generate(" ".join(faculty))

fig, ax = plt.subplots(1,1, figsize=(12,10))
ax.imshow(wordcloud)
plt.axis('off')
fig.tight_layout()
fig.savefig("faculty.png", dpi=300)

