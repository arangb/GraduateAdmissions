# -*- coding: utf-8 -*-
"""
Decisions.py 
Analyzes the results of a slate query to find out when students make their
decisions and how many admits are expected this year.
"""

import pandas
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from datetime import datetime


plt.rc('font', family='sans-serif', size=16)

#The data file should be an exported query with the following fields:
# Name,Received,Decision 1 Confirmed Date,Decision 1,Institution 1 GPA (4.0 Scale),Period Year
df= pandas.read_excel(r'C:\Users\Nichol\Downloads\Decision date 20210325-100623.xlsx')

#find the days before the due date the decision was made. The actual "deadline" is 4/16
d={'year':df['Period Year'],'month':np.linspace(4,4,len(df['Period Year'])),
   'day':np.linspace(16,16,len(df['Period Year']))}
due_date=pandas.DataFrame(d)

df['due_date']=pandas.to_datetime(due_date)
df['delta_T']=df['due_date']-df['Decision 1 Confirmed Date']
df['days_before']=df['delta_T'].dt.days+df['delta_T'].dt.seconds/(60*60*24)

#Remove instances where something happened after the admissions deadline, but keep the deferrals
criteria=(df.days_before>0) | (df['Decision 1']=="Admit/Defer")
df = df[criteria].reset_index(drop = True).dropna(how='all', axis=1)

#We will need to loop over years
years=np.sort(df['Period Year'].unique())
current_year=datetime.now().year
d=datetime(current_year,4,16)-datetime.now()
days_to_deadline=d.days+d.seconds/(60*60*24)

#Used to make sure we don't double count deferrals
d = {'Name': [""]}
df_deferrals=pandas.DataFrame(d);

#data storage
accepts_days=np.empty([0]);
total_accepts=np.empty([0]);
declines_days=np.empty([0]);
total_declines=np.empty([0]);
for year in years:
    criteria=(df['Period Year']==year) & (df['Decision 1']=="Admit/Accept Offer") & ~(df['Name'].isin(df_deferrals['Name']))
    df_accepts = df[criteria].reset_index(drop = True).dropna(how='all', axis=1)
    
    criteria=(df['Period Year']==year) & (df['Decision 1']=="Admit/Decline Offer")
    df_declines = df[criteria].reset_index(drop = True).dropna(how='all', axis=1)
    
    criteria=(df['Period Year']==year) & (df['Decision 1']=="Admit/Defer")
    df_deferrals = df[criteria].reset_index(drop = True).dropna(how='all', axis=1)
    
    if len(df_deferrals)==0:
        df_deferrals=pandas.DataFrame(d)
    
    
    if year < current_year:
        accepts=np.linspace(1,1/len(df_accepts),len(df_accepts));
        declines=np.linspace(1,1/len(df_declines),len(df_declines));
        
        total_accepts=np.append(total_accepts,accepts)
        accepts_days=np.append(accepts_days,np.sort(df_accepts.days_before))
    
        total_declines=np.append(total_declines,declines)
        declines_days=np.append(declines_days,np.sort(df_declines.days_before))
    else:
        current_accepts=len(df_accepts)
        current_declines=len(df_declines)
        
def func(x, a, b, c):
    return a * np.exp(-b * x) + c

#Fit accepts
xdata=accepts_days
ydata=total_accepts
inds=np.argsort(xdata)
xdata=xdata[inds]
ydata=ydata[inds]
lb=[1,0,0]
ub=[1+1e-5,100,1]
popt_accept,pcov= curve_fit(func, xdata, ydata,bounds=(lb,ub))
 
plt.figure(5,figsize=(10,10))    
plt.clf()
plt.scatter(xdata,ydata,label='Data')
plt.xlabel("Days before 4/6")
plt.ylabel("Normalized cumulative accepts")
plt.title("Accepts")
plt.plot(xdata, func(xdata, *popt_accept), 'r-',
         label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt_accept))

plt.show()
plt.legend()

def func_accept(x, a):
    return a * np.exp(-popt_accept[1] * x) + popt_accept[2]

#now fit the data from the current year
xdata=np.sort(df_accepts.days_before)
ydata=np.linspace(1,1/len(df_accepts),len(df_accepts))
popt_accept_current,pcov=curve_fit(func_accept, xdata, ydata)

# =============================================================================
# plt.figure(6,figsize=(10,10))    
# plt.clf()
# plt.scatter(xdata,ydata,label='Data')
# plt.xlabel("Days before 4/6")
# plt.ylabel("Normalized cumulative accepts")
# plt.title("Current accepts")
# plt.plot(xdata, func_accept(xdata, *popt_accept_current), 'r-',
#          label='fit: a=%5.3f' % tuple(popt_accept_current))
# plt.show()
# plt.legend()
# =============================================================================

print("Calculated accpets from fitting %3.3f and direct calculation %3.3f" %
      (popt_accept_current[0]*current_accepts,
      current_accepts/func(days_to_deadline,*popt_accept)))

#Fit declines
xdata=declines_days
ydata=total_declines
inds=np.argsort(xdata)
xdata=xdata[inds]
ydata=ydata[inds]
popt_decline,pcov = curve_fit(func, xdata, ydata,bounds=(lb,ub))
 
plt.figure(6,figsize=(10,10))    
plt.clf()
plt.scatter(xdata,ydata,label='Data')
plt.xlabel("Days before 4/6")
plt.ylabel("Normalized cumulative declines")
plt.title("Declines")
plt.plot(xdata, func(xdata, *popt_decline), 'r-',
         label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt_decline))
plt.show()
plt.legend()

def func_decline(x, a):
    return a * np.exp(-popt_decline[1] * x) + popt_decline[2]


#now fit the data from the current year
xdata=np.sort(df_declines.days_before)
ydata=np.linspace(1,1/len(df_declines),len(df_declines))
popt_decline_current,pcov=curve_fit(func_decline, xdata, ydata)

# =============================================================================
# plt.figure(8,figsize=(10,10))    
# plt.clf()
# plt.scatter(xdata,ydata,label='Data')
# plt.xlabel("Days before 4/6")
# plt.ylabel("Normalized cumulative declines")
# plt.title("Current declines")
# plt.plot(xdata, func_decline(xdata, *popt_decline_current), 'r-',
#          label='fit: a=%5.3f' % tuple(popt_decline_current))
# plt.show()
# plt.legend()
# =============================================================================

print("Calculated accpets from fitting %3.3f and direct calculation %3.3f" %
      (popt_decline_current[0]*current_declines,
      current_declines/func(days_to_deadline,*popt_decline)))

#TODO: bin the mean times to acceptanceby GPA

gpa_bins=np.linspace(3,4,11)
gpa_accepts_norm=np.empty([0]);
gpa_accepts=np.empty([0]);

gpa_days_accept=np.empty([0]);
gpa_days_decline=np.empty([0]);


for gpa in gpa_bins[0:10]:
        criteria=(df['Institution 1 GPA (4.0 Scale)'] > gpa) & (df['Institution 1 GPA (4.0 Scale)'] <= gpa+0.1) & (df['Decision 1']=="Admit/Accept Offer")   
        df_accepts = df[criteria].reset_index(drop = True).dropna(how='all', axis=1)
        
        
        criteria=(df['Institution 1 GPA (4.0 Scale)'] > gpa) & (df['Institution 1 GPA (4.0 Scale)'] <= gpa+0.1) & (df['Decision 1']=="Admit/Decline Offer")   
        df_declines = df[criteria].reset_index(drop = True).dropna(how='all', axis=1)
        
        gpa_accepts=np.append(gpa_accepts,len(df_accepts));
        gpa_accepts_norm=np.append(gpa_accepts_norm,len(df_accepts)/(len(df_accepts)+len(df_declines)));
        gpa_days_accept=np.append(gpa_days_accept,df_accepts.days_before.mean());
        gpa_days_decline=np.append(gpa_days_decline,df_declines.days_before.mean());


plt.figure(7,figsize=(10,10))    
plt.clf()
plt.scatter(gpa_bins[1:11],gpa_days_accept,label='Accepts')
plt.plot(gpa_bins[1:11],gpa_days_accept)
plt.scatter(gpa_bins[1:11],gpa_days_decline,label='Declines')
plt.plot(gpa_bins[1:11],gpa_days_decline)
plt.xlabel("GPA")
plt.ylabel("Days before 4/16 decision was made")
plt.show()
plt.legend()     

plt.figure(8,figsize=(10,10))    
plt.clf()
plt.scatter(gpa_bins[1:11],gpa_accepts_norm,label='Yield')
plt.plot(gpa_bins[1:11],gpa_accepts_norm)
plt.scatter(gpa_bins[1:11],np.divide(gpa_accepts,np.sum(gpa_accepts)),label='Weight')
plt.plot(gpa_bins[1:11],np.divide(gpa_accepts,np.sum(gpa_accepts)))
plt.xlabel("GPA")
plt.show()
plt.legend()     

