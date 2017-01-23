# gb_downloader.py

Script used to retrieve .gb files from NCBI using eutils.

**'-in'**,**'--input'**, dest='inputfile', help='Provide the input fasta files to parse')

**'-l'**,**'--list'**, dest='listfile', help='instead of providing a fasta to parse, provide a txt file in which each row is a unique GI. One can parse the list provided of the GIs not found to try again... since NCBI rejects some connections.')

**'-out'**,**'--output'**, dest='outputfile', required=True, help='Provide the output directory')
