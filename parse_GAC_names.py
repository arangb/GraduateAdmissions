import os
# This script will convert the pdf of the PersonalStatement of each student into a text file, and look for the names of UR professors (we obtain these first from the webpage). 
# It will grep each file, print out each match with context, and add the counter which is saved as a two column file in StudentFacnames.csv
# Since many names are ambiguous, this process needs to be corrected manually on a second run. For example, John Nichol matches "Nichol"as Bigelow, and Adam Frank, matches Frank Wolfs, etc.... 

# This needs to be run in the same folder as gac_dir where all the pdfs are. 
gac_dir='/scratch/aran/GAC18/Intl47-28-49' # Remember to include the / at the end

#Download faculty page:
#wget http://www.pas.rochester.edu/people/faculty/index.html
#sed 's/\/h4/\/h4\n/g ; s/a href=/\n/g' index.html  | /bin/grep "\/h4" | sed 's/.*\">\(.*\)\,.*/\1/'
# First, adds newlines in every /h4 and "a href=" matches, then grep those lines only with /h4, and finally, remove everything outside of > and , (after the comma comes the first names). So this leaves us with only surnames. 

fac_names=['Agrawal','BenZvi','Bergstralh','Betti','Bigelow','Blackman','Bocko','Bodek','Boyd','Cline','Collins','Das','Demina','Dery','Douglass','Duke','Eberly','Ferbel','Forrest','Foster','Franco','Frank','Froula','Gao','Garcia-Bellido','Ghoshal','Gourdain','Guo','Haefner','Hagen','Helfer','Howell','Jordan','Knight','Knox','Mamajek','Manly','McCrory','McFarland','Melissinos','Milonni','Nakajima','Nichol','Oakes','Orr','Pipher','Quillen','Rajeev','Ren','Rothberg','Rygg','Savedoff','Schroeder','Seyler','Shapir','Slattery','Sobolewski','Stroud','Tarduno','Teitel','Thorndike','Vamivakas','Van Horn','Visser','Watson','Wolfs','Wu','Zhang','Zhong']

# Removed 'Thomas', it gives too many false positives 
# Removed 'Wolf', overlaps with Wolfs and Wolf Udo-Schroeder

fac_count = {} # Dictionary where the key is the faculty name as above, and the item is the total count of students that mention the faculty
for fac in fac_names:
	fac_count[fac]=0

student_foundfac={}
os.system('rm -f ' + gac_dir + '/*.txt')
for filename in os.listdir(gac_dir):
    if filename.endswith(".pdf"):
    #if "948404071" in filename:
        print(os.path.join(gac_dir, filename))
        student_name=filename.split(" (")[0].strip() # just remove the App# and extension from the filename 
        foundfac=''
        # convert pdf to text:
        os.system('pdftotext \"' + filename + '\"') # Add quotes to avoid complaints about parenthesis, etc... 
        filename_txt=filename.replace('.pdf','.txt')
        for fac in fac_names:
			grep_cmd = '/bin/grep \"' + fac + '\" \"' + filename_txt + '\"'
			grep_result = os.popen(grep_cmd).read()
			if not grep_result == "": 
				print(grep_cmd)
				print(grep_result)
				fac_count[fac]+=1
				if foundfac == '':  
					foundfac=fac
				else:
					foundfac=foundfac+', '+fac
		
			student_foundfac[student_name]=foundfac
#print student_foundfac		

import csv
with open('StudentFacnames.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile,delimiter=';')
    for key, value in student_foundfac.items():
       writer.writerow([key, value])
print("Wrote file StudentFacnames.csv with two rows: StudentName FoundFacultyNames")

# We can correct here wrong entries (once we have inspected the output of grep and see any errors):
# Corrections for GAC18 folder
#fac_count['Frank']-=3
#fac_count['Ren']-=1
#fac_count['Nichol']-=7
#fac_count['Franco']-=1
#fac_count['Guo']-=2
#fac_count['Zhang']-=3
#fac_count['Jordan']-=1
#fac_count['Wu']-=-1
# Corrections for AdmittedDomestic
#fac_count['Frank']-=2
#fac_count['Nichol']-=6
#fac_count['Guo']-=1
#fac_count['Wu']-=-1
# Corrections for Intl47-28-49
fac_count['Frank']-=3
fac_count['Ren']-=3
fac_count['Nichol']-=5
fac_count['Franco']-=1
fac_count['Guo']-=1
fac_count['Zhang']-=7
fac_count['Foster']-=1
fac_count['Wu']-=-2
fac_count['Duke']-=-1
fac_count['Das']-=-1
fac_count['Zhong']-=-1

# Save to csv file wit counts:
with open('grep_list.csv', 'w') as f:
    [f.write('{0},{1}\n'.format(key, value)) for key, value in sorted(fac_count.iteritems(), key=lambda (k,v): (v,k), reverse=True)]
print("Wrote grep_list.csv with two rows: FacultyName Count")
#fac_count_alphabetical=sorted(fac_count.items())
#for key, value in sorted(fac_count.items()):
#	print(key,value)
#print(fac_count_alphabetical)

#for key, value in sorted(fac_count.iteritems(), key=lambda (k,v): (v,k), reverse=True):
#    f.write(key, value)
#fac_count_ordered=sorted(fac_count.iteritems(), key=lambda (k,v): (v,k), reverse=True)
#print(fac_count_ordered)
