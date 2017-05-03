#!/usr/bin/env python

## Last update: 17/4/2017
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

def downloader(gi_list, output_path , tag, file_type, db_type, export_type):
	time_control = 1
	counter = 0
	for gi in gi_list:
		gi_file = gi + "." + export_type
		gbfile = urllib.URLopener()
		## if gi does not have an accession append a .1 to version
		if file_type=="acc":
			if "." not in gi:
				gi+=".1"
		url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db" \
			 "="+db_type+"&id="+gi+"&rettype="+export_type+"&retmode=text"
		try:
			gbfile.retrieve(url, os.path.join(output_path, gi_file))
		except IOError:
			print "Error: url "+url+" does not exist"
		time_control += 1
	## Check output directory and retrieves a list of missing GI's
	
	for x,gi in enumerate(gi_list):
		if gi_file not in os.listdir(output_path):
			if x==0:
				output_checker = open(tag + "_missing.txt", 'w')

			output_checker.write(gi + "\n")
		else:
			counter=+1
	return counter, gi_list

def main():
	parser = argparse.ArgumentParser(description="Retrieves all gb files given an input fasta")
	parser.add_argument('-in','--input', dest='inputfile', nargs='+', help='Provide the input fasta files to parse')
	parser.add_argument('-l','--list', dest='listfile', help='instead of providing a fasta to parse, provide a txt file in which each row is a unique GI. One can parse the list provided of the GIs not found to try again... since NCBI rejects some connections.')
	parser.add_argument('-out','--output', dest='outputfile', required=True, help='Provide the output directory')
	parser.add_argument('-ft','--filetype', dest='filetype',
						choices=['acc','gi'], required=True, help='Provide ' \
																 'file ' \
														   'type. ' \
												   'Options acc and gi.')
	parser.add_argument('-db','--dbtype', dest='dbtype', required=True, help='Provide database type. Options e.g. nuccore and protein.')
	parser.add_argument('-et','--exporttype', dest='exporttype', required=True, help='Provide export file type. Options e.g. fasta and gb.')

	args = parser.parse_args()
	file_type = args.filetype
	db_type = args.dbtype
	export_type = args.exporttype

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
		downloader(downloader_from_list(args.listfile), output_path, args.listfile.split(".")[0],file_type, db_type, export_type)
	else:
		print "Did you provide any input file type? Or did you provided more than one type?"

if __name__ == "__main__":
	main()