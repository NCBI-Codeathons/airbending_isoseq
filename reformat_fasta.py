import argparse
import os

parser = argparse.ArgumentParser(description='Reformats a fasta file '
	'to only contain the chromosome name in the header.')

parser.add_argument("-f", dest = "fasta_file",
    help = "FASTA file", type = str)
args = parser.parse_args()


ofile = open(args.fasta_file+'_back', 'w')
with open(args.fasta_file, 'r') as fafile:
	for line in fafile: 
		if line[0] == '>':
			line = line.split('|')[0]
		if '\n' not in line:
			line += '\n'
		ofile.write(line)
ofile.close()

os.rename(args.fasta_file+'_back', args.fasta_file)