# -*- coding: utf-8 -*-
"""
Decisions.py 
Analyzes the results of a slate query to find out when students make their
decisions and how many admits are expected this year. This relies on using the most up to date date, so be sure to rerun the query before anaylzing the data.
"""

import pandas
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from datetime import datetime
import tkinter as tk
import tkinter.filedialog as fd

root = tk.Tk()
root.lift()
root.attributes("-topmost", True)
root.withdraw()
filetypes=[("Excel files", ".xlsx .xls")]
file_name= fd.askopenfilename(
    parent=root,
    title='Open a file',
    initialdir='/',
    filetypes=filetypes)

plt.rc('font', family='sans-serif', size=16)

#The data file should be an exported query with at least following fields:
# Name,Decision 1 Confirmed Date,Decision 1,Institution 1 GPA (4.0 Scale),Period Year
df= pandas.read_excel(file_name)

#Alternatively, you can specify the file explicitly, as below.
#df= pandas.read_excel(r'C:\Users\Nichol\Downloads\Decision date 20210325-100623.xlsx')

#find the days before the due date the decision was made. The actual "deadline" is 4/16
d={'year':df['Period Year'],'month':np.linspace(4,4,len(df['Period Year'])),
   'day':np.linspace(16,16,len(df['Period Year']))}
due_date=pandas.DataFrame(d)

df['due_date']=pandas.to_datetime(due_date)
df['delta_T']=df['due_date']-df['Decision 1 Confirmed Date']
df['days_before']=df['delta_T'].dt.days+df['delta_T'].dt.seconds/(60*60*24)

#Remove instances where something happened after the admissions deadline, but keep the deferrals
#This potentially introduces some bias into the predictions, but I'm not exactly sure how to handle it.
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
accepts_years=np.empty([0]);
declines_days=np.empty([0]);
total_declines=np.empty([0]);
declines_years=np.empty([0]);
for year in years:
    #TODO: make sure we don't count people from the wait list here. We should filter based on the initial offer date.
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
        accepts_years=np.append(accepts_years,np.linspace(year,year,len(accepts)))
    
        total_declines=np.append(total_declines,declines)
        declines_days=np.append(declines_days,np.sort(df_declines.days_before))
        declines_years=np.append(declines_years,np.linspace(year,year,len(declines)))

    else:
        current_accepts=len(df_accepts)
        current_declines=len(df_declines)

#Fitting function        
def func(x, a, b, c):
    return a * np.exp(-b * x) +c

#Double exponential fitting function. This seems to give a more unbiased estimate.
def func2(x, a, b, c):
    return a * np.exp(-x/b) +(1-a)*np.exp(-x/c)

#Fit accepts
xdata=accepts_days
ydata=total_accepts
inds=np.argsort(xdata)
xdata=xdata[inds]
ydata=ydata[inds]
#Lower and upper bounds for fitting. 
lb=[0,0,0]
ub=[1,50,5]
popt_accept,pcov= curve_fit(func2, xdata, ydata,bounds=(lb,ub))
 
plt.figure(5,figsize=(10,10))    
plt.clf()
plt.scatter(xdata,ydata,label='2015-2020 data',s=6)
plt.xlabel("Days before 4/16")
plt.ylabel("Normalized cumulative accepts")
plt.title("Accepts")
plt.plot(xdata, func2(xdata, *popt_accept), 'r-',
         label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt_accept))
plt.show()

#Fitting function for the current year's data. Uses the fitted parameters above but this time fits the scaling.
def func_accept(x, a):
    return a * np.exp(-popt_accept[1] * x) + popt_accept[2]

def func_accept2(x, a):
    return a * func2(x,*popt_accept)

#Fit the data from the current year to predict the number of accepts
xdata=np.sort(df_accepts.days_before)
ydata=np.linspace(len(df_accepts),1,len(df_accepts))
popt_accept_current,pcov=curve_fit(func_accept2, xdata, ydata)

plt.plot(xdata,ydata/popt_accept_current[0],'-o',
         label=('%d, %d accepts' % (current_year,np.round(popt_accept_current[0]))),
         color='C2')
plt.legend()
plt.show()

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

print("Calculated accepts from fitting: %3.3f and direct calculation: %3.3f" %
      (popt_accept_current[0],
      current_accepts/func2(days_to_deadline,*popt_accept)))

#Fit declines
xdata=declines_days
ydata=total_declines
inds=np.argsort(xdata)
xdata=xdata[inds]
ydata=ydata[inds]
popt_decline,pcov = curve_fit(func2, xdata, ydata,bounds=(lb,ub))
 
plt.figure(6,figsize=(10,10))    
plt.clf()
plt.scatter(xdata,ydata,label='2015-2020 data',s=6)
plt.xlabel("Days before 4/16")
plt.ylabel("Normalized cumulative declines")
plt.title("Declines")
plt.plot(xdata, func2(xdata, *popt_decline), 'r-',
         label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt_decline))
plt.show()
plt.legend()

#Same as above. Now only fit the scaling.
def func_decline(x, a):
    return a * np.exp(-popt_decline[1] * x) + popt_decline[2]

def func_decline2(x, a):
    return a * func2(x,*popt_decline)


#Fit the data from the current year to predict the number of decliens
xdata=np.sort(df_declines.days_before)
ydata=np.linspace(len(df_declines),1,len(df_declines))
popt_decline_current,pcov=curve_fit(func_decline2, xdata, ydata)

plt.plot(xdata,ydata/popt_decline_current[0],'-o',
         label=('%d, %d declines' % (current_year,np.round(popt_decline_current[0]))),
         color='C2')
plt.legend()


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

print("Calculated declines from fitting: %3.3f and direct calculation: %3.3f" %
      (popt_decline_current[0],
      current_declines/func2(days_to_deadline,*popt_decline)))


#Find out how good our prediction for accepts is
plt.figure(9,figsize=(10,10))    
plt.clf()
color_ind=0
aa=np.empty([0]);
dd=np.empty([0]);
for year in years[0:len(years)-1]:
    xdata=accepts_days[accepts_years==year]
    ydata=total_accepts[accepts_years==year]
    ydata=np.divide(ydata,ydata[len(ydata)-1]) 
    #Convert back to actual numbers of accepts from fractional accepts
    n_accepts=len(ydata)
    
    #One way to predict the number of accepts 
    #is the (total number of accepts at that day)/func2(day,pop_accept).
    predicted_accepts=np.divide(ydata,func2(xdata, *popt_accept))
    accept_error=np.divide(predicted_accepts,n_accepts)
    plt.plot(xdata, accept_error,label=('%d' % year))
    
    inds=np.flipud(np.argsort(xdata)) #Short in descending order
    xdata=xdata[inds]
    ydata=ydata[inds]
    
    #Another way to predict the number of accepts is to fit the data from that year
    for i in np.linspace(2,len(xdata),len(xdata)):
        #Loop through accepts, and generate incomplete data sets as each new accept comes int
        ind=int(i)
        xv=xdata[0:ind]
        yv=ydata[0:ind]

        #Fit the incomplete dataset to extract a predicted number of accepts.
        popt,pcov=curve_fit(func_accept2, xv, yv)
        
        #Based on the incomplete dataset, predicted the number of accepts. 
        predicted_accepts=popt[0]
        accept_error=predicted_accepts/n_accepts
        plt.scatter(xv[ind-1], accept_error,color=('C%d' % color_ind))
        aa=np.append(aa,accept_error)
        dd=np.append(dd,xv[ind-1])

    color_ind=color_ind+1
    
    
#Now see how the trend for this year has changed
#Sort both days and accepts in decending order
xdata=np.flipud(np.sort(df_accepts.days_before))
ydata=np.flipud(np.linspace(len(df_accepts),1,len(df_accepts)))

for i in np.linspace(2,len(xdata),len(xdata)):
    ind=int(i)
    xv=xdata[0:ind]
    yv=ydata[0:ind]
    popt,pcov=curve_fit(func_accept2, xv, yv)
    predicted_accepts=popt[0]
    accept_error=predicted_accepts/popt_accept_current[0]
    plt.scatter(xv[ind-1], accept_error, color=('C%d' % color_ind))

plt.xlabel("Days before 4/16")
plt.ylabel("Predicted/actual")
plt.title("Accept prediction accuracy")
plt.ylim(0,2)
plt.show()
plt.legend()

#Find out how accurate historical fitting would be on this day.
inds=(dd<(days_to_deadline+2)) & (dd>(days_to_deadline-2))
print("Historical accept prediction accuracy is %3.3f +/- %3.3f" % (np.mean(aa[inds]),np.std(aa[inds])))

#Find out how good our prediction for declines is
plt.figure(10,figsize=(10,10))    
plt.clf()
color_ind=0;
aa=np.empty([0]);
dd=np.empty([0]);
for year in years[0:len(years)-1]:
    xdata=declines_days[declines_years==year]
    ydata=total_declines[declines_years==year]
    ydata=np.divide(ydata,ydata[len(ydata)-1]) #Convert back to actual numbers
    n_declines=len(ydata)
    
    #The expected number of declines at any give time is the 
    # is the total number of declines at that day/func2(day,pop_declines).
    predicted_declines=np.divide(ydata,func2(xdata, *popt_decline))
    declines_error=np.divide(predicted_declines,n_declines)
    plt.plot(xdata, declines_error,label=('%d' % year))    
    
    inds=np.flipud(np.argsort(xdata))
    xdata=xdata[inds]
    ydata=ydata[inds]
    
    for i in np.linspace(2,len(xdata),len(xdata)):
        ind=int(i)
        xv=xdata[0:ind]
        yv=ydata[0:ind]
        
        #Fit the incomplete dataset to extract a predicted number of accepts.
        popt,pcov=curve_fit(func_decline2, xv, yv)
        
        #Based on the limited dataset, predicted the number of accepts. 
        predicted_declines=popt[0]
        decline_error=predicted_declines/n_declines
        plt.scatter(xv[ind-1], decline_error,color=('C%d' % color_ind))
        aa=np.append(aa,decline_error)
        dd=np.append(dd,xv[ind-1])

    color_ind=color_ind+1;
    
#Now see how the trend for this year has changed
#Sort both days and declines in decending order
xdata=np.flipud(np.sort(df_declines.days_before))
ydata=np.flipud(np.linspace(len(df_declines),1,len(df_declines)))

for i in np.linspace(2,len(xdata),len(xdata)):
    ind=int(i)
    xv=xdata[0:ind]
    yv=ydata[0:ind]
    popt,pcov=curve_fit(func_decline2, xv, yv)
    predicted_declines=popt[0]
    decline_error=predicted_declines/popt_decline_current[0]
    plt.scatter(xv[ind-1], decline_error, color=('C%d' % color_ind))

plt.xlabel("Days before 4/16")
plt.ylabel("Predicted/actual")
plt.title("Decline prediction accuracy based on calculation")
plt.ylim(0,2)
plt.show()
plt.legend()

#Find out how accurate historical fitting would be on this day.
inds=(dd<(days_to_deadline+2)) & (dd>(days_to_deadline-2))
print("Historical decline prediction accuracy is %3.3f +/- %3.3f" % (np.mean(aa[inds]),np.std(aa[inds])))

#Analyze decision times according to GPA to find out how to use the wait list.
gpa_bins=np.linspace(3,4,11)
gpa_diff=np.diff(gpa_bins)[0]/2
gpa_accepts_norm=np.empty([0])
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
        gpa_days_accept=np.append(gpa_days_accept,df_accepts.days_before.median());
        gpa_days_decline=np.append(gpa_days_decline,df_declines.days_before.median());


plt.figure(7,figsize=(10,10))    
plt.clf()
plt.plot(gpa_bins[1:11]-gpa_diff,gpa_days_accept,'o-',label='Accepts')
plt.plot(gpa_bins[1:11]-gpa_diff,gpa_days_decline,'o-',label='Declines')
plt.xlabel("GPA")
plt.ylabel("Median days before 4/16 decision was made")
plt.show()
plt.legend()     

plt.figure(8,figsize=(10,10))    
plt.clf()
plt.plot(gpa_bins[1:11]-gpa_diff,gpa_accepts_norm,'o-',label='Probability to accept')
plt.plot(gpa_bins[1:11]-gpa_diff,np.divide(gpa_accepts,np.sum(gpa_accepts)),'o-',label='Fraction of overall UR PAS students')
plt.xlabel("GPA")
plt.show()
plt.legend()     

