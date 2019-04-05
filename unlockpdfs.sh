#!/usr/bin/env bash

# Before you run this make sure the names of the files don't have any weird spaces or characters:
# ~/core/Utils/rename.perl 's/\ //g ; s/\,//g' *pdf # remove spaces and commas

for file in `ls *pdf`; do 
	echo $file; 
	fileout=`echo $file | sed 's/\.pdf/\_u\.pdf/'`; # add _u to distinguish it
	qpdf --password=APSBP2019 --decrypt $file $fileout ;
	#pdftk $file input_pw APSBP2019 output $fileout ;
done
