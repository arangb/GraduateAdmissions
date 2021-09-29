import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
''' 
Aran Garcia-Bellido June 2020. 
Use this script to read the placement history spreadsheet from Laura and
 make a dataframe (and csv file) for each year with the columns:
'Name', 'YearEntered', 'GraduationTime', 'WithdrawalTime','TA_semesters','LOA_terms','PreSummer','Advisor'

-Make sure that in each input sheet the first three columns are: Name, Pre-Start Summer, Fall 1, ... 
 We rely on only having one column between the Name and the entry Fall 
 year to count terms until graduation. And there has to be a Spring, Summer, Fall for each year. 
- We may need to remove the Summary sheet. Now the script just fails when it gets to that sheet. 
'''

file_name='GACdata_PlacementHistory_2004-17.xlsx'
xls = pd.ExcelFile(file_name,engine='openpyxl')
#xls.sheet_names # lists sheets in the file

def get_rowcol_indeces_of_cell_containing(dataframe,substring):
    ''' Find the row and column indeces of any cell in the frame that contains the substring
        You can match several substrings with the OR operand |: "X|x"
        Inputs: dataframe we are looking over, substring to match'''
    d = dict(zip(dataframe.columns, range(len(dataframe.columns))))
    s = dataframe.rename(columns=d).stack()
    # return tuple of indeces of matches: [(row1,col1), (row2,col2),...] 
    return s[(s.str.contains(substring,na=False))].index.tolist()

def calculate_years_from_col_index(dim,rowcol_indeces):
    ''' inputs: dimension of list to be returned
        rowcol_indeces: the list of row and column indeces that (max index)'''
    tyears=[]
    if len(rowcol_indeces)>0:
        t_row,t_col=zip(*rowcol_indeces) # transform list of tuples to two lists: (0, 5) , (16, 29)
        match=0
        for row in range(dim):
            ''' For example: idx=14  15  16  17 
                        term=F5  S5  Su5 F6    <- if spring or summer, subtract 0.5
                idx//3,idx%3=4,2 5,0 5,1 5,2   <- if Fall, the new year starts
                       tgrad=4   4.5 4.5 5   
            '''
            if row in t_row:
                tyears.append( t_col[match]//3-0.5 if t_col[match]%3 < 2 else t_col[match]//3)
                match=match+1
            else:
                tyears.append(np.nan)
    else: # in case there were no matches
        tyears=[np.nan]*dim
    return tyears

# Loop over sheets in order by year, 2004-2017:
for sheet_name in sorted(xls.sheet_names): #['2004']:
    print('Reading sheet: ',sheet_name)
    df=pd.read_excel(file_name, sheet_name=sheet_name,engine='openpyxl')
    # for some reason the first cell A1 with the year is a float and not a string... 
    df=df[df[float(sheet_name)].str.contains(r',',na=False)].reset_index(drop = True)
    # This removed the summary lines below the names: only keep rows whose first cell contains a comma
    df=df.loc[:,~df.columns.duplicated()] # remove unwanted columns
    df=df.drop(['Unnamed','Yrs. To Grad','Yrs to Grad','Unnamed:'],axis=1,errors='ignore')
    print(df)
    name=[x for x in df[float(sheet_name)]]
    cohort=[str(sheet_name)]*len(name) # a column with the year for each student
    # Find the column index of "/Grad" or "/grad" to calculate years to graduation:
    a=get_rowcol_indeces_of_cell_containing(df,'/Grad|/grad') # [(0, 16), (5, 29)]
    tgrad=calculate_years_from_col_index(len(name),a)
    # Do the same for the withdrawals:
    b=get_rowcol_indeces_of_cell_containing(df,'Withdr|withdr')
    tout=calculate_years_from_col_index(len(name),b)
    # Find advisor:
    dfadvisor=df.iloc[:,2:].copy() # only look at the columns starting in Fall1, and before the cumulative number 'Yrs. To Grad'
    c=get_rowcol_indeces_of_cell_containing(dfadvisor,'TA|LOA|Grad|grad|Withd|withd')
    advisor=[]
    if len(c)>1:
        for i,j in c:
            #For those left in the Fall of first year without any advisor 
            # or those that never got an advisor (only TA'ed or had LOA)
            if ( ((j<=2) and ('ithdr' in str(dfadvisor.iat[i,j]))) or (any(x in dfadvisor.iat[i,j] for x in 'TA|LOA')) ):
                dfadvisor.iat[i,j]='-'
            else:
                dfadvisor.iat[i,j]=np.nan # if they match, we set them to nan
    dfadvisor=dfadvisor.stack().groupby(level=0).apply(lambda x: x.unique().tolist()) # This returns a Series with lists as entries
    advisor=[','.join(x) for x in dfadvisor] # just make each list a single string with commas separating
    # We have many cases of '-,Frank' or 'Frank,-' this will remove the hyphen:
    advisor=[x.replace('-,','').replace(',-','') for x in advisor]
    # Find how many semesters they TA'ed:
    TAsem=[df.iloc[row,1:-1].str.count('TA').sum() for row in range(len(name))]
    # Find how many terms they were in Leave Of Absence:
    LOA=[df.iloc[row,1:-1].str.count('LOA').sum() for row in range(len(name))]
    # Find if they attended the summer before they attended courses:
    PreSummer=[x for x in df.iloc[:,1]] # this is the column with index 1 (label = "Pre-Summer Start")
    
    #Create new dataframe to export:
    # columns=('Name', 'YearEntered', 'GraduationTime', 'WithdrawalTime','TA_semesters','LOA_terms','PreSummer','Advisor')
    data={'Name':name, 'YearEntered':cohort,'GraduationTime':tgrad, 
        'WithdrawalTime':tout,'TA_semesters':TAsem,'LOA_terms':LOA,'PreSummer':PreSummer,'Advisor':advisor}
    #for key, value in data.items():
    #    print(key,len(value))
    
    newdf=pd.DataFrame(data)
    newdf.to_csv(sheet_name+'_placement.csv',index=False,header=False)

print("You can now concatenate the csv files: cat 20*_placement.csv > placement_04-11.csv")

# We can easily concatenate all years into one: 
# cat 20*_placement.csv > placement_04-11.csv
# You can then order by name and remove the extra column-name rows.
