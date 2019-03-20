
# coding: utf-8
#get_ipython().run_line_magic('matplotlib', 'inline')

import pandas
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy import optimize
import uncertainties as unc
import uncertainties.unumpy as unp

mpl.rc('font', family='sans-serif', size=14)
plt.rcParams.update({'mathtext.default':  'regular' })
Data = pandas.read_excel('GACHistory.xlsx')

# Plot number of applicants
plt.plot(Data.Year, Data.Domestic+Data.International,linewidth=2.0, linestyle='--', color='orange')
plt.plot(Data.Year, Data.International,linewidth=2.0, linestyle='-', color='blue', marker='^', markersize=5.2)
plt.plot(Data.Year, Data.Domestic, linewidth=2.0, linestyle='-', color='red', marker='o', markersize=5.2)
plt.plot(Data.Year, Data.DomWom+Data.IntlWom, linewidth=2.0, linestyle='-', color='green', marker='>', markersize=5.2)
plt.plot(Data.Year, Data.DomURM+Data.IntlURM,linewidth=2.0, linestyle='-', color='black', marker='*', markersize=5.2)
plt.legend( ('Total','Intl','Domestic','Women','URM') , loc='upper right', frameon=False,numpoints=1)
plt.title("Number of applications")
plt.ylabel("Number of applicants")
plt.xlabel("Year")
plt.grid()
plt.xlim(2004.5,2019.5)
plt.savefig('Trends01-NumberPerYear.png')

# Plot composition of applicants:
plt.figure()
totalapp=Data.Domestic+Data.International
domperc=100.*(Data.Domestic/totalapp)
intlperc=100.*(Data.International/totalapp)
womenperc=100*((Data.DomWom+Data.IntlWom)/totalapp)
urmperc=100*((Data.DomURM+Data.IntlURM)/totalapp)
plt.plot(Data.Year, domperc, linewidth=2.0, linestyle='-', color='red', marker='o', markersize=5.2)
plt.plot(Data.Year, intlperc,linewidth=2.0, linestyle='-', color='blue', marker='^', markersize=5.2)
plt.plot(Data.Year, womenperc, linewidth=2.0, linestyle='-', color='green', marker='>', markersize=5.2)
plt.plot(Data.Year, urmperc,linewidth=2.0, linestyle='-', color='black', marker='*', markersize=5.2)
plt.legend( ('Domestic','Intl','Women','URM') , loc='upper right', frameon=False,numpoints=1)
plt.title("Composition of applicants")
plt.ylabel("% of applicants")
plt.xlabel("Year")
plt.grid()
plt.xlim(2004.5,2019.5)
plt.savefig('Trends01-ApplicantCompositionPerYear.png')

# Plot composition of offers
plt.figure()
totaloff=Data.DomOff+Data.IntlOff
domperc=100.*(Data.DomOff/totaloff)
intlperc=100.*(Data.IntlOff/totaloff)
womenperc=100*((Data.DomOffWom+Data.IntlOffWom)/totaloff)
urmperc=100*((Data.DomOffURM+Data.IntlOffURM)/totaloff)
plt.plot(Data.Year, domperc, linewidth=2.0, linestyle='-', color='red', marker='o', markersize=5.2)
plt.plot(Data.Year, intlperc,linewidth=2.0, linestyle='-', color='blue', marker='^', markersize=5.2)
plt.plot(Data.Year, womenperc, linewidth=2.0, linestyle='-', color='green', marker='>', markersize=5.2)
plt.plot(Data.Year, urmperc,linewidth=2.0, linestyle='-', color='black', marker='*', markersize=5.2)
plt.legend( ('Domestic','Intl','Women','URM') , loc='upper right', frameon=False,numpoints=1)
plt.title("Composition of offers made")
plt.ylabel("% of offers")
plt.xlabel("Year")
plt.grid()
plt.xlim(2004.5,2019.5)
plt.savefig('Trends02-OfferCompositionPerYear.png')

# Plot composition of each entering cohort
plt.figure()
totalacc=Data.DomAcc+Data.IntlAcc
domperc=100.*(Data.DomAcc/totalacc)
intlperc=100.*(Data.IntlAcc/totalacc)
womenperc=100*((Data.DomAccWom+Data.IntlAccWom)/totalacc)
urmperc=100*((Data.DomAccURM+Data.IntlAccURM)/totalacc)
plt.plot(Data.Year, domperc, linewidth=2.0, linestyle='-', color='red', marker='o', markersize=5.2)
plt.plot(Data.Year, intlperc,linewidth=2.0, linestyle='-', color='blue', marker='^', markersize=5.2)
plt.plot(Data.Year, womenperc, linewidth=2.0, linestyle='-', color='green', marker='>', markersize=5.2)
plt.plot(Data.Year, urmperc,linewidth=2.0, linestyle='-', color='black', marker='*', markersize=5.2)
plt.legend( ('Domestic','Intl','Women','URM') , loc='upper right', frameon=False,numpoints=1)
plt.title("Composition of each cohort")
plt.ylabel("% of those accepted")
plt.xlabel("Year")
plt.grid()
plt.xlim(2004.5,2019.5)
plt.savefig('Trends03-AcceptCompositionPerYear.png')

# Plot acceptance rates
plt.figure()
domperc=100.*(Data.DomAcc/Data.DomOff)
intlperc=100.*(Data.IntlAcc/Data.IntlOff)
womenperc=100*((Data.DomAccWom+Data.IntlAccWom)/(Data.DomOffWom+Data.IntlOffWom))
urmperc=100*((Data.DomAccURM+Data.IntlAccURM)/(Data.DomOffURM+Data.IntlOffURM))
accperc=100*(totalacc/totaloff)
plt.plot(Data.Year, accperc,linewidth=2.0, linestyle='--', color='orange')
plt.plot(Data.Year, domperc, linewidth=2.0, linestyle='-', color='red', marker='o', markersize=5.2)
plt.plot(Data.Year, intlperc,linewidth=2.0, linestyle='-', color='blue', marker='^', markersize=5.2)
plt.plot(Data.Year, womenperc, linewidth=2.0, linestyle='-', color='green', marker='>', markersize=5.2)
plt.plot(Data.Year, urmperc,linewidth=2.0, linestyle='-', color='black', marker='*', markersize=5.2)
plt.legend( ('Total','Domestic','Intl','Women','URM') , loc='upper right', frameon=False,numpoints=1)
plt.title("Yield: accepted/offered")
plt.ylabel("% accept of offers in that group")
plt.xlabel("Year")
plt.grid()
plt.xlim(2004.5,2019.5)
plt.savefig('Trends04-YieldsPerYear.png')

# Number of offers and accepts
plt.figure()
plt.plot(Data.Year, totaloff, linewidth=2.0, linestyle='-', color='black', marker='o', markersize=5.2)
plt.plot(Data.Year, totalacc,linewidth=2.0, linestyle='-', color='red', marker='*', markersize=5.2)
plt.plot(Data.Year, accperc,linewidth=2.0, linestyle='--', color='orange')
plt.legend( ('Number offered','Number accepted','% accepted/offered'), loc='upper right', frameon=False,numpoints=1)
plt.title("Total numbers of accepted, offered")
plt.ylabel("Number of students / %")
plt.xlabel("Year")
plt.grid()
plt.xlim(2004.5,2019.5)
plt.savefig('Trends05-NumAccOffYieldPerYear.png')


# # Plot acceptance rates for US and FN
# #domperc=100.*(Data.DomAcc/Data.DomOff)
# #intlperc=100.*(Data.IntlAcc/Data.IntlOff)
# import uncertainties
# eff,eff_errlo,eff_errhi
# plt.errorbar(Data.Year, eff, [eff_errlo,eff_errhi], linestyle='None', marker='o', markerfacecolor='blue', markersize=5.2)
# plt.xlim(2004.5,2019.5)
# plt.title("")
# plt.xlabel("Year")
# plt.ylabel("Yield: accepted/offered")
# plt.grid()

# plt.savefig('Trends06-YieldPerYearErroBarsFit.png')


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
