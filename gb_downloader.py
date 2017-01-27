#!/usr/bin/env python

## Last update: 27/1/2017
## Author: T.F. Jesus
## This script downloads gb files given a fasta file and retrieves all gb files corresponding to the Accession numbers present in fasta
## Uses NCBI eutils

import argparse
import os
from os.path import isfile, join
import urllib
import time
import shutil

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

def downloader_from_list(list_file):
	if_handle=open(list_file,'r')
	gi_list = []
	for line in if_handle:
		gi_list.append(line.strip("\n"))
	return gi_list	

def downloader(gi_list, output_path , tag):
	time_control = 1
	counter = 0
	for gi in gi_list:
		if time_control%5 == 0:	#from 5 to 5 gi's the script pauses for 5 seconds in order to avoid ban from NCBI.
			time.sleep(5) #time in seconds
			time_control += 1
			print "pausing..." + str(time_control-1) + " GIs already processed!"
		else:
			gi_file = gi + ".gb"
			gbfile = urllib.URLopener()
			gbfile.retrieve("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id="+gi+"&rettype=gb&retmode=text", os.path.join(output_path, gi_file))
			time_control += 1
	## Check output directory and retrieves a list of missing GI's
	out_file_name=tag + ".txt"
	if os.path.isfile(out_file_name):
		shutil.move(out_file_name, out_file_name + ".backup")
	output_checker = open(out_file_name, 'a')
	for gi in gi_list:
		if gi + ".gb" not in os.listdir(output_path):
			output_checker.write(gi + "\n")
		else:
			counter=+1
	return counter, gi_list

def main():
	parser = argparse.ArgumentParser(description="Retrieves all gb files given an input fasta")
	parser.add_argument('-in','--input', dest='inputfile', nargs='+', help='Provide the input fasta files to parse')
	parser.add_argument('-l','--list', dest='listfile', help='instead of providing a fasta to parse, provide a txt file in which each row is a unique GI. One can parse the list provided of the GIs not found to try again... since NCBI rejects some connections.')
	parser.add_argument('-out','--output', dest='outputfile', required=True, help='Provide the output directory')
	args = parser.parse_args()
	if args.inputfile:
		list_fastas = args.inputfile
		for infile in list_fastas:
			output_path = os.path.join(os.path.dirname(os.path.abspath(infile.strip())), args.outputfile)
			if not os.path.exists(output_path):
				os.makedirs(output_path)
			counter, gi_list, file_check=downloader(fastaparser(infile.strip()), output_path, infile.split(".")[0])
#		print counter
#		print len(gi_list)
#		while counter < len(gi_list):
#			output_path = os.path.join(os.path.dirname(os.path.abspath("List_of_GI_not_retrieved.txt")), args.outputfile)
#			downloader(downloader_from_list("List_of_GI_not_retrieved.txt"), output_path)

	elif args.listfile:
		list_file = args.listfile
		output_path = os.path.join(os.path.dirname(os.path.abspath(args.listfile.strip())), args.outputfile)
		if not os.path.exists(output_path):
			os.makedirs(output_path)
		downloader(downloader_from_list(args.listfile), output_path, args.listfile.split(".")[0])
	else:
		print "Did you provide any input file type? Or did you provided more than one type?"

if __name__ == "__main__":
	main()