#!/usr/bin/env python

## Last update: 20/1/2017
## Author: T.F. Jesus
## This script downloads gb files given a fasta file and retrieves all gb files corresponding to the Accession numbers present in fasta
## Uses NCBI eutils

import argparse
from subprocess import Popen, PIPE, call
import os
import urllib
import time

def fastaparser(fasta_file):
	if_handle=open(fasta_file,'r')
	gi_list = []
	for line in if_handle:
			if len(line) > 0: 
				line = line.splitlines()[0]
			if line.startswith(">"):
				gi = line.split("|")[1]
				gi_list.append(gi)
	return gi_list

def downloader(gi_list, output_path):
	time_control = 1
	for gi in gi_list:
		if time_control%5 == 0:	#from 5 to 5 gi's the script pauses for 5 seconds in order to avoid ban from NCBI.
			time.sleep(5) #time in seconds
			time_control += 1
			print "pausing..." + str(time_control-1) + " sequences downloaded already!"
		else:
			gi_file = gi + ".gb"
			gbfile = urllib.URLopener()
			gbfile.retrieve("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id="+gi+"&rettype=gb&retmode=text", os.path.join(output_path, gi_file))
			time_control += 1

def main():
	parser = argparse.ArgumentParser(description="Retrieves all gb files given an input fasta")
	parser.add_argument('-in','--input', dest='inputfile', required=True, help='Provide the input fasta files to parse')
	parser.add_argument('-out','--output', dest='outputfile', required=True, help='Provide the output directory')
	args = parser.parse_args()
	list_fastas = args.inputfile.split(" ")
	for infile in list_fastas:
		output_path = os.path.join(os.path.dirname(os.path.abspath(infile.strip())), args.outputfile)
		if not os.path.exists(output_path):		
			os.makedirs(output_path)		
		downloader(fastaparser(infile.strip()), output_path)


if __name__ == "__main__":
	main()