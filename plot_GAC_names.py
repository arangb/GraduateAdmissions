import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
# This macro will read in the csv file produced by parse_GAC_names.py and make a histogram of the number of applications that mention each name. 

fig, ax = plt.subplots(1,1, figsize=(17,6))

# I've found that pandas is better at dealing with string columns, np.genfromtxt is pretty bad! 
table = pd.read_csv('grep_list.csv', sep=',', header=None, names=['Names','Count'])
sortedtable=table.sort_values('Count',ascending=False) # or sort_values. sort() is deprecated after 0.17
sortedtable = sortedtable.reset_index(drop=True) # For some stupid reason, pandas keeps the old index in the new sorted frame!!!! 
print(sortedtable)
names = sortedtable['Names']
count = sortedtable['Count']

#names=['Boyd', 'Bigelow', 'Howell', 'Collins', 'Nichol', 'Gourdain', 'BenZvi', 'Bocko', 'Shapir', 'Manly', 'Agrawal', 'Teitel', 'Douglass', 'Froula', 'Sobolewski', 'McFarland', 'Gao', 'Frank', 'Jordan', 'Stroud', 'Rygg', 'Eberly', 'Guo', 'Vamivakas', 'Wolfs', 'Alonso', 'Lin', 'Rothberg', 'Journe', 'Demina']
#count=['6', '5', '5', '3', '3', '3', '3', '3', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1']
idx = 5 + 10*np.arange(len(names))

plt.bar(idx, count, width=5, align='center', fc='royalblue')
plt.xticks(idx, names)
plt.ylabel('count')
plt.title('Interest by Personal Statement')
plt.xlim(1,idx[-1]+4)
plt.xticks(rotation=80)
fig.tight_layout()
fig.show()
fig.savefig('faculty_names_histo.png')

# ## Faculty Interest Word Cloud
# This is eye candy which is kind of fun to show at faculty meetings. In 2017 I wanted to show the key areas of interest (mainly LLE + various QO faculty).
from wordcloud import WordCloud, STOPWORDS

fac_count_dict = dict(zip(names, count))
wordcloud = WordCloud(stopwords=STOPWORDS,
                      background_color='black',
                      width=1200,
                      height=1000,
                      prefer_horizontal=0.8,
                      relative_scaling=1.,
                      max_font_size=300,
                      ).generate_from_frequencies(fac_count_dict)

fig, ax = plt.subplots(1,1, figsize=(12,10))
ax.imshow(wordcloud)
plt.axis('off')
fig.tight_layout()
fig.savefig("faculty_wordcloud.png", dpi=300)
