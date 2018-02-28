
# coding: utf-8
#get_ipython().run_line_magic('matplotlib', 'inline')

import pandas
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rc('font', family='sans-serif', size=14)

Data = pandas.read_excel('GACHistory.xlsx')
plt.plot(Data.Year, Data.Domestic+Data.International,linewidth=2.0, linestyle='--', color='orange')
plt.plot(Data.Year, Data.International,linewidth=2.0, linestyle='-', color='blue', marker='^', markersize=5.2)
plt.plot(Data.Year, Data.Domestic, linewidth=2.0, linestyle='-', color='red', marker='o', markersize=5.2)
plt.plot(Data.Year, Data.DomWom+Data.IntlWom, linewidth=2.0, linestyle='-', color='green', marker='>', markersize=5.2)
plt.plot(Data.Year, Data.DomURM+Data.IntlURM,linewidth=2.0, linestyle='-', color='black', marker='*', markersize=5.2)
plt.legend( ('Total','Intl','Domestic','Women','URM') , loc='upper right', frameon=False)
plt.title("Number of applications")
plt.ylabel("Number of applicants")
plt.xlabel("Year")
plt.grid()
plt.xlim(2004.5,2018.5)
plt.savefig('Trends01-NumberPerYear.png')

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
plt.legend( ('Domestic','Intl','Women','URM') , loc='upper right', frameon=False)
plt.title("Composition of offers made")
plt.ylabel("% of offers")
plt.xlabel("Year")
plt.grid()
plt.xlim(2004.5,2018.5)
plt.savefig('Trends02-OfferComositionPerYear.png')

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
plt.legend( ('Domestic','Intl','Women','URM') , loc='upper right', frameon=False)
plt.title("Composition of each cohort")
plt.ylabel("% of those accepted")
plt.xlabel("Year")
plt.grid()
plt.savefig('Trends03-AcceptComositionPerYear.png')

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
plt.legend( ('Total','Domestic','Intl','Women','URM') , loc='upper right', frameon=False)
plt.title("Yield: accepted/offered")
plt.ylabel("% accept of offers in that group")
plt.xlabel("Year")
plt.grid()
plt.savefig('Trends04-YieldsPerYear.png')

# Number of offers and accepts
plt.figure()
plt.plot(Data.Year, totaloff, linewidth=2.0, linestyle='-', color='black', marker='o', markersize=5.2)
plt.plot(Data.Year, totalacc,linewidth=2.0, linestyle='-', color='red', marker='*', markersize=5.2)
plt.plot(Data.Year, accperc,linewidth=2.0, linestyle='--', color='orange')
plt.legend( ('Number offered','Number accepted','% accepted/offered'), loc='upper right', frameon=False)
plt.title("Total numbers of accepted, offered")
plt.ylabel("Number of students / %")
plt.xlabel("Year")
plt.grid()
plt.savefig('Trends05-NumAccOffYieldPerYear.png')

