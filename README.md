# gb_downloader.py

Script used to retrieve .gb files from NCBI using eutils.

Note: Given that I am having some problems with bad requests from NCBI, the script generates a list file (.txt) that can be used to run this script again using the '-l' option in order to retrieve the remaining sequences that were not retrieved in the first instance. Users are encoraged to check the output directory for the number of files using something like "ls | wc -l" (assuming that the directory has only .gb files). However, if an output .txt file contain entries, then you should run the script again in order to retrieve the remaining sequences. 

**'-in'**,**'--input'**, dest='inputfile', help='Provide the input fasta files to parse')

**'-l'**,**'--list'**, dest='listfile', help='instead of providing a fasta to parse, provide a txt file in which each row is a unique GI. One can parse the list provided of the GIs not found to try again... since NCBI rejects some connections.')

**'-out'**,**'--output'**, dest='outputfile', required=True, help='Provide the output directory')
