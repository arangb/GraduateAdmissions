import os
# This script will convert the pdf of the PersonalStatement of each student into a text file, and look for the names of UR professors (we obtain these first from the webpage). 
# To download the PS from SLATE: Go to the Browser, click on any Bin, then on Build Query, then remove the Bin Filter and add a new Filter, search for Bin and select all except "Awaiting Submission". By clicking on the names of the bins it calculates how many entries are selected so you can add bins until you get what you want. Once you have the filter, go to Run Query>Output PDF Document Export > click on Export and in Format select "Export as individual PDFs within a zip archive" and then in INsert Part just select the Personal Statement.
    
# This script will grep each pdf file, print out each match with context, and add the counter which is saved as a two column file in StudentFacnames.csv
# Since many names are ambiguous, this process needs to be corrected manually on a second run. For example, John Nichol matches "Nichol" as Bigelow, and Adam Frank, matches Frank Wolfs, etc.... 

# This needs to be run in the same folder as gac_dir where all the pdfs are: python ../GraduateAdmissions/parse_GAC_names.py > log
gac_dir='/home/aran/GAC20/ALLPS' 

#Download faculty page:
#wget http://www.pas.rochester.edu/people/faculty/index.html
#sed 's/\/h4/\/h4\n/g ; s/a href=/\n/g' index.html  | /bin/grep "\/h4" | sed 's/.*\">\(.*\)\,.*/\1/' | tr '\n' ',' | sed 's/\,/\"\,\"/g' 
# First, adds newlines in every /h4 and "a href=" matches, then grep those lines only with /h4, and finally, remove everything outside of > and , (after the comma comes the first names). So this leaves us with only surnames. Then change the \n to a comma, and add the quotes so that we can make a list.

fac_names=["Agrawal","BenZvi","Bergstralh","Betti","Bigelow","Blackman","Blok","Bocko","Bodek","Boyd","Cardenas","Cline","Collins","Das","Demina","Dery","Dias","Douglass","Eberly","Ferbel","Forrest","Foster","Franco","Frank","Froula","Gao","Bellido","Ghoshal","Gourdain","Guo","Haefner","Hagen","Helfer","Howell","Jordan","Knight","Knox","Mamajek","Manly","McCrory","McFarland","Melissinos","Milonni","Murray","Nakajima","Nichol","Oakes","Orr","Pipher","Quillen","Rajeev","Ren","Rothberg","Rygg","Savedoff","Schroeder","Sefkow","Seyler","Shapir","Slattery","Sobolewski","Stroud","Tarduno","Teitel","Thomas","Thorndike","Vamivakas","Van Horn","Visser","Watson","Wolfs","Wu","Zhang","Zhong"]

fac_names = sorted(set(fac_names)) # remove duplicates and keep alphabetical order. We had Douglass twice.

# Removed 'Thomas', it gives too many false positives 
# Removed 'Wolf', overlaps with Wolfs and Wolf Udo-Schroeder

fac_count = {} # Dictionary where the key is the faculty name as above, and the item is the total count of students that mention the faculty
for fac in fac_names:
	fac_count[fac]=0

student_foundfac={}
os.system('rm -f ' + gac_dir + '/*.txt')
for filename in sorted(os.listdir(gac_dir)): # order the pdf files alphabetically
    if filename.endswith(".pdf"):
    #if "920823152" in filename:
        print(os.path.join(gac_dir, filename))
        student_name=filename.split(" (")[0].strip() # just remove the App# and extension from the filename 
        foundfac=''
        # convert pdf to text:
        os.system('pdftotext \"' + filename + '\"') # Add quotes to avoid complaints about parenthesis, etc... 
        filename_txt=filename.replace('.pdf','.txt')
        for fac in fac_names:
			grep_cmd = '/bin/grep \"' + fac + '\" \"' + filename_txt + '\"'
			grep_result = os.popen(grep_cmd).read()
			if (fac == 'Nichol' and ('Nicholas' in grep_result)) or (fac == 'Frank' and ('Wolfs' in grep_result)) or (fac == 'Wu' and ('Wuhan' in grep_result)) or (fac in student_name):
			    continue
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
# Corrections for GAC20 folder
fac_count['Frank']-=9
fac_count['Ren']-=10
fac_count['Nichol']+=1
# fac_count['Franco']-=1
# fac_count['Guo']-=4
fac_count['Zhang']-=7
# fac_count['Jordan']-=2
# fac_count['Watson']-=1
#fac_count['Duke']-=4
fac_count['Wu']-=5
fac_count['Das']-=4
fac_count['Zhong']-=2
# fac_count['BenZvi']+=1
# fac_count['McFarland']+=1
fac_count['Gao']+=1
fac_count['Murray']-=2
# fac_count['Douglass']-=4
fac_count['Rajeev']-=1
fac_count['Knox']-=1
fac_count['Schroeder']-=1
fac_count['Knight']-=2
# fac_count['Hagen']-=1
# fac_count['Foster']-=1
# fac_count['Boyd']-=1
# fac_count['Wolfs']-=1

# Save to csv file with counts:
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
