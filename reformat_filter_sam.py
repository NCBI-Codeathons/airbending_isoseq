
import re
import os
import sys
import csv
import traceback
import argparse

x = csv.field_size_limit(sys.maxsize)

def process_args():
    parser = argparse.ArgumentParser(
        description="""This script parses an input sam file, replaces all
        instances of X and = in the CIGAR string to M and collapses adjacent
        M operations.""")

    parser.add_argument('-i', '--infile', help='input sam file; default STDIN')
    parser.add_argument('-o', '--outfile', help='output sam file; default STDOUT')

    args = parser.parse_args()
    if args.infile:
        samin = open(args.infile, 'rt')
    else:
        samin = sys.stdin

    if args.outfile:
        samout = open(args.outfile, 'wt')
    else:
        samout = sys.stdout

    return samin, samout

def process_sam(samin, samout):
    tblin = csv.reader(samin, delimiter = '\t')
    tblout = csv.writer(samout, delimiter = '\t',
                        quotechar = "\xb6",
                        lineterminator=os.linesep)
    try:
        for aln in tblin:
            if not aln[0].startswith('@') and aln[2].startswith('NC_0'):
                aln_cig = re.sub(r'[X=]', 'M', aln[5])
                aln_cig = re.findall(r'\d+[A-Z]', aln_cig)
                newcig = ''
                oldi = None
                for i in aln_cig:
                    if not oldi:
                        oldi = i
                    elif i.endswith('M') and oldi.endswith('M'):
                        i = int(i.rstrip('M'))
                        oldi = int(oldi.rstrip('M'))
                        oldi = str(i+oldi) + 'M'
                    else:
                        newcig += oldi
                        oldi = i
                aln[5] = newcig + oldi 
                tblout.writerow(aln)
            if aln[0].startswith('@'):
                tblout.writerow(aln)
    except:
        print('ERROR converting {}' .format(aln[0]))
        print(traceback.format_exc(), file=sys.stderr)
        sys.exit(1)
#         print(aln[5], newcig, oldi)

    samin.close()
    samout.close()

if __name__ == '__main__':
    i, o = process_args()
    process_sam(i, o)
