import pandas

unames = pandas.read_csv('UniversitiesbyResearchTier.csv',names=['R1','R2','R3','Top100LiberalArts'])
#f1=pandas.read_excel('18_data_all.xlsx')
f1=pandas.read_excel('2020_scores_all.xlsx')
#f2=pandas.read_excel('190125_data_allapps.xlsx')
# merge all names:
#d=pandas.concat([f1['Institution 1 Name'],f2['Institution 1 Name']]).dropna()
d=f1['Institution 1 Name']
print(d)
#for u in d:
#	print(u)
#	for l in unames['R1'].dropna():
#		if u in l:
#			print('Match!: ',u,l)
x=d.isin(unames['R1']) # <-- this checks for all characters to match
y=d.isin(unames['R2'])
z=d.isin(unames['R3'])
t=d.isin(unames['Top100LiberalArts'])
#print(x)
newd=pandas.concat([d,x,y,z,t], axis=1)
newd.to_csv('checu.csv')
# Fix in UniversitiesbyResearchTier.csv
#Brigham Young University-Provo --> Brigham Young University
#University Of Washington-Seattle Campus --> University Of Washington
#University Of Illinois at Urbana-Champaign --> University Of Illinois at Urbana
#University Of Pittsburgh-Pittsburgh Campus --> University Of Pittsburgh-Main Campus
#University Of Nebraska-Lincoln --> University Of Nebraska At Lincoln
#University Of Texas-Austin --> The University Of Texas At Austin  <-- this needs checking in our data
#Auburn University --> Auburn University Main Campus
#Stony Brook University --> Suny Center Stony Brook <-- check in our data
#Saint Mary's College --> Saint Marys College Of Maryland
#St John's University-New York --> St Johns University-New York
#University Of Maryland-College Park --> University Of Maryland College Park
#CUNY City College --> Cuny City College
#University Of Colorado Boulder --> University Of Colorado At Boulder
#Virginia Polytechnic Institute and State University --> Virginia Polytech Institute And State Univ
#University Of Kansas --> University Of Kansas Main Campus
#SUNY at Buffalo --> University At Buffalo  <-- check in our data
#Binghamton University --> Suny Binghamton
#Georgia Institute Of Technology-Main Campus --> Georgia Institute Of Technology Main Campus
#Towson University --> Towson State University
#University Of California, Santa Barbara --> University Of California-Santa Barbara <-- check also in our data
#Franklin and Marshall College --> Franklin And Marshall College
#Bowling Green State University-Main Campus <-- check in our data
#University Of South Florida-Main Campus --> University Of South Florida
#University Of Oklahoma-Norman Campus --> University Of Oklahoma Norman Campus
#University Of Minnesota-Twin Cities --> University Of Minnesota Twin Cities
#SUNY At Albany --> Suny Center Albany
#College Of William and Mary --> College Of William And Mary
#Louisiana State University and Agricultural & Mechanical College --> Louisiana St Univ & Agrl & Mech & Hebert Laws Ctr
#University Of California-Merced <-- Check out in our data
#Cornell University <-- remove Endowed Colleges Check out in our data
#of --> Of , at --> At, in --> In, the --> The
