import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
from BinomialEfficiency import BinomialEfficiency 
plt.rc('font', family='sans-serif', size=16)

header_list=['Name','YearEntered','GraduationTime', 'WithdrawalTime','TA_semesters','LOA_terms','PreSummer','Advisor']
df=pd.read_csv('placement_04-11.csv',names=header_list)

# Let's use only the years for which we have most data:
df=df[df['YearEntered']<2012]
#print(df['GraduationTime'])

Ntot=len(df['YearEntered'])
gtime=df['GraduationTime'].dropna()
wtime=df['WithdrawalTime'].dropna()
avg_gradtime=np.mean(gtime)
avg_wdrwtime=np.mean(wtime)
print('Total students analyzed = %3i'%Ntot)
print('Students Graduated/Withdrawn/StillEnrolled=%-3i/%-3i/%-3i'%(len(gtime),len(wtime),Ntot-len(gtime)-len(wtime)))
print('AvgGradTime = %2.1f years\nAvgWithdrawalTime = %2.1f years \nSuccess rate = %3.2f'
       %(avg_gradtime,avg_wdrwtime,len(gtime)/(len(gtime)+len(wtime))))
#
# Plot histograms of PhD completion and withdrawal time in years
#
plt.figure()
xmax=12
xbins=np.arange(0, xmax, 0.5)
plt.hist(gtime, bins=xbins,label='Completed PhD\nN=%2i; Mean=%2.1f'%(len(gtime),avg_gradtime))
plt.hist(wtime, bins=xbins,label='Withdraw\nN=%2i; Mean=%2.1f'%(len(wtime),avg_wdrwtime),color='red', lw=3, histtype='step',ls='--')
plt.xlabel("Time after enrollment [years]")
plt.ylabel("Students")
plt.title('URPAS 2004-2011 Cohorts')
#plt.ylim(3.3,4.02)
plt.xlim(0,xmax)
plt.xticks(range(0,xmax+1)) # otherwise the ticks appear every 2 years
plt.grid()
plt.legend(fontsize=xmax, loc=2)
plt.tight_layout()
plt.savefig('GAC00-GradTimeYears.png')
#
# Plot Percentage of completed PhDs vs years
#
'''
To do the three line plots of success rate for intl, non-URM and URM, you need to pass the
gtime for FN and the Ntot_FN:
gtime_FN=df[(df['Citizenship']=='FN')]['GraduationTime'].dropna()
Ntot_FN=len(df[(df['Citizenship']=='FN')]) # all Foreign National enrollees
gtime_nonURM=
Ntot_nonURM
gtime_URM=
Ntot_URM= # this includes all enrollees that are URM (those who complete and those who withdraw)
If there is not a lot of URM students, you can make the histogram with less bins.
'''
plt.figure()
ghist, xbase = np.histogram(gtime, bins=xbins)
#whist, xbase = np.histogram(wtime, bins=xbins)
shist = 100.*ghist/(len(gtime)+len(wtime))
e,errorlo,errorhi=BinomialEfficiency(ghist,len(gtime)+len(wtime),method='bayes')
plt.fill_between(xbase[:-1], e-errorlo, e+errorhi, facecolor='b', alpha=0.3)
plt.savefig('caca.png')
#evaluate the cumulative https://stackoverflow.com/questions/15408371/cumulative-distribution-plots-python
shist_cumulative = np.cumsum(shist)
# plot the cumulative function
plt.plot(xbase[:-1], shist_cumulative, c='blue', label='Cumulative rate = %3.1f%%'%shist_cumulative[-1])
plt.xlabel("Time after enrollment [years]")
plt.ylabel("% completed PhD")
plt.title('URPAS 2004-2011 Cohorts')
plt.ylim(0,100)
plt.xlim(0,11)
plt.xticks(range(0,11+1)) # otherwise the ticks appear every 2 years
plt.grid()
plt.legend(fontsize=12, loc=2)
plt.tight_layout()
plt.savefig('GAC01-CompletePhDFraction_vs_years.png')

#
# Field
#
# For 2020:
#fac_names=["Agrawal","BenZvi","Bergstralh","Betti","Bigelow","Blackman","Blok","Bocko","Bodek","Boyd","Cardenas","Cline","Collins","Das","Demina","Dery","Dias","Douglass","Eberly","Ferbel","Forrest","Foster","Franco","Frank","Froula","Gao","Bellido","Ghoshal","Gourdain","Guo","Haefner","Hagen","Helfer","Howell","Jordan","Knight","Knox","Mamajek","Manly","McCrory","McFarland","Melissinos","Milonni","Murray","Nakajima","Nichol","Oakes","Orr","Pipher","Quillen","Rajeev","Ren","Rothberg","Rygg","Savedoff","Schroeder","Sefkow","Seyler","Shapir","Slattery","Sobolewski","Stroud","Tarduno","Teitel","Thomas","Thorndike","Vamivakas","Van Horn","Visser","Watson","Wolfs","Wu","Zhang","Zhong"]

fields_fac={'HEP': ['BenZvi','Bodek','Demina','Ferbel','Garcia-Bellido','Manly','McFarland','Slattery','Wolfs','Orr','Das','Rajeev','Thorndike','Hagen'],
'QO': ['Wolf', 'Bigelow', 'Boyd', 'Eberly','Jordan','Howell','Blok','Nichol'],
'LLE': ['Froula','Gourdain','Rygg','Tzeferacos'],
'CM': ['Gao','Goshal','Shapir','Teitel','Jordan','Nichol'],
'AA': ['Blackman','Quillen', 'Forrest', 'Frank', 'Pipher', 'Watson', 'Mamajek', 'Nakajima','Goshal']
}

# We can invert this dictionary:
fac_fields = {}
for kfield, vnames in fields_fac.items():
    for name in vnames:
        fac_fields.setdefault(name, []).append(kfield)
print(fac_fields)
