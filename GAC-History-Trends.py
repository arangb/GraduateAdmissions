
# coding: utf-8
#get_ipython().run_line_magic('matplotlib', 'inline')

import pandas
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy import optimize
import uncertainties as unc
import uncertainties.unumpy as unp
np.set_printoptions(precision=1)
mpl.rc('font', family='sans-serif', size=14)
plt.rcParams.update({'mathtext.default':  'regular' })
Data = pandas.read_excel('GACHistory.xlsx')

YearMin=2004.5
YearMax=2020.5

# Plot number of applicants
plt.plot(Data.Year, Data.Domestic+Data.International,linewidth=2.0, linestyle='--', color='orange')
plt.plot(Data.Year, Data.International,linewidth=2.0, linestyle='-', color='blue', marker='^', markersize=5.2)
plt.plot(Data.Year, Data.Domestic, linewidth=2.0, linestyle='-', color='red', marker='o', markersize=5.2)
plt.plot(Data.Year, Data.DomWom+Data.IntlWom, linewidth=2.0, linestyle='-', color='green', marker='>', markersize=5.2)
plt.plot(Data.Year, Data.DomURM+Data.IntlURM,linewidth=2.0, linestyle='-', color='black', marker='*', markersize=5.2)
plt.legend(('Total','Foreign','USA','Women','URM'), loc='upper center', frameon=False, numpoints=1,
			ncol=5, mode='expand', handlelength=1.5, handletextpad=0.20, columnspacing=0.5, borderaxespad=0.1)
plt.title("Number of applications")
plt.ylabel("Number of applicants")
plt.xlabel("Year")
plt.grid()
plt.xlim(YearMin,YearMax)
ax=plt.gca()
ymin, ymax = ax.get_ylim()
ax.set_ylim(ymin,ymax*1.05)
plt.savefig('Trends01-NumberPerYear.png')

# Plot composition of applicants:
plt.figure()
totalapp=Data.Domestic+Data.International
dompercapp=100.*(Data.Domestic/totalapp)
intlpercapp=100.*(Data.International/totalapp)
womenpercapp=100*((Data.DomWom+Data.IntlWom)/totalapp)
urmpercapp=100*((Data.DomURM+Data.IntlURM)/totalapp)
plt.plot(Data.Year, intlpercapp,linewidth=2.0, linestyle='-', color='blue', marker='^', markersize=5.2)
plt.plot(Data.Year, dompercapp, linewidth=2.0, linestyle='-', color='red', marker='o', markersize=5.2)
plt.plot(Data.Year, womenpercapp, linewidth=2.0, linestyle='-', color='green', marker='>', markersize=5.2)
plt.plot(Data.Year, urmpercapp,linewidth=2.0, linestyle='-', color='black', marker='*', markersize=5.2)
plt.legend(('FN','US','Women','URM'), loc='upper center', frameon=False, numpoints=1,
			  ncol=4, mode='expand', handletextpad=0.20, columnspacing=0.5, borderaxespad=0.1)
plt.title("Composition of applicants")
plt.ylabel("% of applicants")
plt.xlabel("Year")
plt.grid()
plt.xlim(YearMin,YearMax)
ax=plt.gca()
ymin, ymax = ax.get_ylim()
ax.set_ylim(ymin,ymax*1.05)
plt.savefig('Trends01-ApplicantCompositionPerYear.png')

# Plot composition of offers
plt.figure()
totaloff=Data.DomOff+Data.IntlOff
dompercoff=100.*(Data.DomOff/totaloff)
intlpercoff=100.*(Data.IntlOff/totaloff)
womenpercoff=100*((Data.DomOffWom+Data.IntlOffWom)/totaloff)
urmpercoff=100*((Data.DomOffURM+Data.IntlOffURM)/totaloff)
plt.plot(Data.Year, dompercoff, linewidth=2.0, linestyle='-', color='red', marker='o', markersize=5.2)
plt.plot(Data.Year, intlpercoff,linewidth=2.0, linestyle='-', color='blue', marker='^', markersize=5.2)
plt.plot(Data.Year, womenpercoff, linewidth=2.0, linestyle='-', color='green', marker='>', markersize=5.2)
plt.plot(Data.Year, urmpercoff,linewidth=2.0, linestyle='-', color='black', marker='*', markersize=5.2)
plt.legend( ('US','FN','Women','URM') , loc='upper right', frameon=False,numpoints=1,
			  ncol=4, mode='expand', handletextpad=0.20, columnspacing=0.5, borderaxespad=0.1)
plt.title("Composition of offers made")
plt.ylabel("% of offers")
plt.xlabel("Year")
plt.grid()
plt.xlim(YearMin,YearMax)
ax=plt.gca()
ymin, ymax = ax.get_ylim()
ax.set_ylim(ymin,ymax*1.05)
plt.savefig('Trends02-OfferCompositionPerYear.png')

# Plot composition of each entering cohort
plt.figure()
totalacc=Data.DomAcc+Data.IntlAcc
dompercacc=100.*(Data.DomAcc/totalacc)
intlpercacc=100.*(Data.IntlAcc/totalacc)
womenpercacc=100*((Data.DomAccWom+Data.IntlAccWom)/totalacc)
urmpercacc=100*((Data.DomAccURM+Data.IntlAccURM)/totalacc)
plt.plot(Data.Year, dompercacc, linewidth=2.0, linestyle='-', color='red', marker='o', markersize=5.2)
plt.plot(Data.Year, intlpercacc,linewidth=2.0, linestyle='-', color='blue', marker='^', markersize=5.2)
plt.plot(Data.Year, womenpercacc, linewidth=2.0, linestyle='-', color='green', marker='>', markersize=5.2)
plt.plot(Data.Year, urmpercacc,linewidth=2.0, linestyle='-', color='black', marker='*', markersize=5.2)
plt.legend( ('US','FN','Women','URM') , loc='upper right', frameon=False,numpoints=1,
			ncol=4, mode='expand', handletextpad=0.20, columnspacing=0.5, borderaxespad=0.1)
plt.title("Composition of each cohort")
plt.ylabel("% of those accepted")
plt.xlabel("Year")
plt.grid()
plt.xlim(YearMin,YearMax)
ax=plt.gca()
ymin, ymax = ax.get_ylim()
ax.set_ylim(ymin,ymax*1.05)
plt.savefig('Trends03-AcceptCompositionPerYear.png')

# Plot acceptance rates
plt.figure()
Adomperc=100.*(Data.DomAcc/Data.DomOff)
Aintlperc=100.*(Data.IntlAcc/Data.IntlOff)
Awomenperc=100*((Data.DomAccWom+Data.IntlAccWom)/(Data.DomOffWom+Data.IntlOffWom))
Aurmperc=100*((Data.DomAccURM+Data.IntlAccURM)/(Data.DomOffURM+Data.IntlOffURM))
Accperc=100*(totalacc/totaloff)
plt.plot(Data.Year, Accperc,linewidth=2.0, linestyle='--', color='orange')
plt.plot(Data.Year, Adomperc, linewidth=2.0, linestyle='-', color='red', marker='o', markersize=5.2)
plt.plot(Data.Year, Aintlperc,linewidth=2.0, linestyle='-', color='blue', marker='^', markersize=5.2)
plt.plot(Data.Year, Awomenperc, linewidth=2.0, linestyle='-', color='green', marker='>', markersize=5.2)
plt.plot(Data.Year, Aurmperc,linewidth=2.0, linestyle='-', color='black', marker='*', markersize=5.2)
plt.legend( ('Total','US','FN','Women','URM') , loc='upper right', frameon=False,numpoints=1,
			 ncol=5, mode='expand', handlelength=1.5, handletextpad=0.20, columnspacing=0.5, borderaxespad=0.1)
plt.title("Yield: accepted/offered")
plt.ylabel("% accept of offers in that group")
plt.xlabel("Year")
plt.grid()
plt.xlim(YearMin,YearMax)
ax=plt.gca()
ymin, ymax = ax.get_ylim()
ax.set_ylim(ymin,ymax*1.05)
plt.savefig('Trends04-YieldsPerYear.png')

# Number of offers and accepts
plt.figure()
plt.plot(Data.Year, totaloff, linewidth=2.0, linestyle='-', color='black', marker='o', markersize=5.2)
plt.plot(Data.Year, totalacc, linewidth=2.0, linestyle='-', color='red', marker='*', markersize=5.2)
plt.plot(Data.Year, Accperc,  linewidth=2.0, linestyle='--', color='orange')
plt.legend( ('Number offered','Number accepted','% accepted/offered'), loc='upper left', frameon=False,numpoints=1)
			 #ncol=3, mode='expand', handletextpad=0.20, columnspacing=0.5, borderaxespad=0.1)
plt.title("Total numbers of accepted, offered")
plt.ylabel("Number of students / %")
plt.xlabel("Year")
plt.grid()
plt.xlim(YearMin,YearMax)
ax=plt.gca()
ymin, ymax = ax.get_ylim()
ax.set_ylim(ymin,ymax*1.05)
plt.savefig('Trends05-NumAccOffYieldPerYear.png')

# Plot offer/appl percent ratios of US, FN, men, women and URM
# For example, for women: (N women offered/ TOT offers) / (N women applied/TOT applied)
plt.figure()
AccDom=dompercoff/dompercapp
AccIntl=intlpercoff/intlpercapp
AccWomen=womenpercoff/womenpercapp
AccMen=(100*(totaloff-(Data.DomOffWom+Data.IntlOffWom))/totaloff)/(100*(totalapp-(Data.DomWom+Data.IntlWom))/totalapp)
AccURM=urmpercoff/urmpercapp
avg=totaloff/totalapp
print('Women offer ratio ',AccWomen.values)
print('Avg Offer Ratio: Dom=%3.2f Intl=%3.2f Wom=%3.2f Men=%3.2f URM=%3.2f'%(np.mean(AccDom),np.mean(AccIntl),np.mean(AccWomen),np.mean(AccMen),np.mean(AccURM)))
plt.plot(Data.Year, AccDom, linewidth=2.0, linestyle='-', color='red', marker='o', markersize=5.2)
plt.plot(Data.Year, AccIntl,linewidth=2.0, linestyle='-', color='blue', marker='^', markersize=5.2)
plt.plot(Data.Year, AccMen,linewidth=2.0, linestyle='-', color='orange',marker='+', markersize=5.2)
plt.plot(Data.Year, AccWomen, linewidth=2.0, linestyle='-', color='green', marker='>', markersize=5.2)
plt.plot(Data.Year, AccURM, linewidth=2.0, linestyle='-', color='black', marker='*', markersize=5.2)
plt.legend(('US','FN','Men','Women','URM') , loc='upper right', frameon=False,numpoints=1)
			 #ncol=5, mode='expand', handlelength=1.5, handletextpad=0.20, columnspacing=0.5, borderaxespad=0.1)
plt.title("Offer Ratio: % offered / % applied")
plt.ylabel("Offer Ratio")
plt.xlabel("Year")
plt.grid()
plt.xlim(YearMin,YearMax)
#ax=plt.gca()
#ymin, ymax = ax.get_ylim()
#ax.set_ylim(ymin,ymax*1.05)
plt.savefig('Trends06-OffAppPercRatioUSFNMenWomURMPerYear.png')

# Plot off/app for US, FN, men, women and URM 
# For example, for women: N women offered/N women applied
plt.figure()
Dom=100*Data.DomOff/Data.Domestic
Intl=100*Data.IntlOff/Data.International
Women=100*(Data.DomOffWom+Data.IntlOffWom)/(Data.DomWom+Data.IntlWom)
Men=100*(totaloff-(Data.DomOffWom+Data.IntlOffWom))/(totalapp-(Data.DomWom+Data.IntlWom))
URM=100*(Data.DomOffURM+Data.IntlOffURM)/(Data.DomURM+Data.IntlURM)
avg=100*totaloff/totalapp
print('Avg off/app rate: Dom=%3.1f Intl=%3.1f Wom=%3.1f Men=%3.1f URM=%3.1f'%(np.mean(Dom),np.mean(Intl),np.mean(Women),np.mean(Men),np.mean(URM)))
print('Total rate: ', avg.values)
plt.plot(Data.Year, Dom, linewidth=2.0, linestyle='-', color='red', marker='o', markersize=5.2)
plt.plot(Data.Year, Intl,linewidth=2.0, linestyle='-', color='blue', marker='^', markersize=5.2)
plt.plot(Data.Year, Men,linewidth=2.0, linestyle='-', color='orange',marker='+', markersize=5.2)
plt.plot(Data.Year, Women, linewidth=2.0, linestyle='-', color='green', marker='>', markersize=5.2)
plt.plot(Data.Year, URM,linewidth=2.0, linestyle='-', color='black', marker='*', markersize=5.2)
plt.plot(Data.Year, avg, linewidth=2.0, linestyle='--', color='gray')
plt.legend(('US','FN','Men','Women','URM','All') , loc='upper right', frameon=False,numpoints=1)
			 #ncol=5, mode='expand', handlelength=1.5, handletextpad=0.20, columnspacing=0.5, borderaxespad=0.1)
plt.title("Offer rate: offered/applied")
plt.ylabel("Offer rate %")
plt.xlabel("Year")
plt.grid()
plt.xlim(YearMin,YearMax)
#ax=plt.gca()
#ymin, ymax = ax.get_ylim()
#ax.set_ylim(ymin,ymax*1.05)
plt.savefig('Trends07-OfferRateUSFNMenWomURMPerYear.png')

########################################################################

# Plot Offers vs Acceptances in each year, fit to power law
# The data is clearly non-linear: the first 40 offers yield around 5 accepts, and the last 40 offers yield around 20.
# We will need a power law function:
def func_powerlaw(x, a, b):
    return a * x**b

# Sort acc, off and years in order of acc
#x, y, d = zip(*sorted(zip(totalacc[2:],totaloff[2:],Data.Year[2:]),axis=0))
x,y,d = np.sort(np.array([totalacc,totaloff,Data.Year]),axis=0)
plt.figure()
plt.scatter(x, y, c='k', s=8)
for i in np.arange(len(d)): # print year for each marker
    plt.text(x[i], y[i], str(d[i]),fontsize=8)
fitres = optimize.curve_fit(func_powerlaw, x, y, sigma=np.sqrt(y), p0=[10.,0.5], full_output=True, absolute_sigma=True)
popt=fitres[0]; pcov=fitres[1]
# Need to use correlated errors to draw sigma bands
a, b = unc.correlated_values(popt, pcov)
print('Fit results: \na = {0:.3f} \nb = {1:.3f}'.format(a,b))
redchisq = (fitres[2]['fvec']**2).sum()/(len(fitres[2]['fvec'])-len(popt))
print("chi2/Ndof = %6.3f" % redchisq)
finex= np.arange(0,30,0.2)
plt.plot(finex, func_powerlaw(finex, *popt), 'b-',linewidth=2) # fit line
py = func_powerlaw(finex,a,b)
nom = unp.nominal_values(py)
std = unp.std_devs(py)
plt.fill_between(finex, nom-1*std, nom+1*std, facecolor='b',alpha=0.3,label='1$\sigma$ band of fit') # bands
plt.fill_between(finex, nom-2*std, nom+2*std, facecolor='b',alpha=0.2,label='2$\sigma$ band of fit') # bands
avgyield=np.mean(np.divide(x,y,dtype=float)) # this is the average yield
plt.plot(finex,finex*(1./avgyield),'k--',alpha=0.2,linewidth=2,label='mean acc/off={0:.2f}'.format(avgyield))
plt.legend(loc='lower right')
plt.title(r'Power law best fit o=${0:5.3f} \cdot a^{{{1:4.3f}}}$'.format(*popt),color='b')
plt.ylabel("Offers")
plt.xlabel("Acceptances")
plt.grid()
plt.axis([0, 30, 0, 90])
plt.savefig('OffersVSAcceptance-PowerLaw.png')
