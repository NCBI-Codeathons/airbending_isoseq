#!/usr/bin/env python3 

import sys
import csv
import os
import argparse

def parse_args():
    desc = 'Generate a GTF file using input data from t_df and loc_df files'
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('-t', '--txfile', 
        help="input file with transcript and gene info")
    parser.add_argument('-l', '--locfile', 
        help="input file with exon location info")
    parser.add_argument('-o', '--outfile', 
        help="output gtf file; default STDOUT")

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    if not args.txfile and args.locfile:
        print('ERROR! Need both txfile and locfile', file = sys.stderr)
        parser.print_help(sys.stderr)
        sys.exit(1)

    return args


def read_loc_file(loc_file):
    loc_dict = {}
    with open(loc_file, 'rt') as f:
        tbl = csv.reader(f, delimiter = ',')
        for line in tbl:
            if not line[0].startswith('vertex'):
                try:
                    vertex_id, chrom, coord, strand = line[:4]
                except:
                    print('Error parsing loc_file')
                    sys.exit(1)
                try:
                    vertex_id = int(vertex_id) 
                    coord = int(coord)
                except:
                    print('Error! coordinates can only be integers')
                    sys.exit(1)
                if strand not in ['+', '-']:
                    print('Error! strand can only be + or -')
                    sys.exit(1)
                loc_dict[vertex_id] = [chrom, coord, strand]
    return loc_dict

def create_gene_dict(tx_file, loc_dict):
    gene_dict = {}
    with open(tx_file, 'rt') as f:
        tbl = csv.reader(f, delimiter = ',')
        for line in tbl:
            if not line[0].startswith('tid'):
                tid, gid, gname, path = line[:4]
                path = path.strip('[').strip(']').split(',')
                path = set(map(int, path))
                coords = []
                for i in path:
                    coords.append(loc_dict[i][1])
                tx_left = min(coords)
                tx_right = max(coords)
                if gene_dict.get(gid, None):
                    gene = gene_dict[gid]
                    if gene[0] > tx_left:
                        gene[0] = tx_left
                    if gene[1] < tx_right:
                        gene[1] = tx_right
                    gene_dict[gid] = gene
                else:
                    gene_dict[gid] = [tx_left, tx_right]
    return gene_dict


if __name__ == '__main__':

    ## process arguments
    args = parse_args()

    if args.outfile:
        outgtf = open(args.outfile, 'wt')
    else:
        outgtf = sys.stdout

    print('Parsing the loc_file...', file = sys.stderr)
    loc_dict = read_loc_file(args.locfile)

    print('Creating gene dictionary...', file = sys.stderr)
    gene_dict = create_gene_dict(args.txfile, loc_dict)

    print('Parsing tx_file and writing gtf...', file = sys.stderr)
    with open(args.txfile, 'rt') as f:
        genes_done = set()
        tbl = csv.reader(f, delimiter = ',')
        for line in tbl:
            if not line[0].startswith('tid'):
                try:
                    tid, gid, gname, path = line[:4]
                except:
                    print('Error parsing tx_file')
                    sys.exit(1)
                path = path.strip('[').strip(']').split(',')
                path = list(map(int, path))
                coords = []
                for i in path:
                    try:
                        coords.append(loc_dict[i])
                    except:
                        print('Error! cannot find the vertex_id')
                        sys.exit(1)
                chrom = coords[0][0]
                strand = coords[0][2]
                exons = [(coords[i], coords[i+1]) for i in range(len(coords)-1)][::2]
                tx_left = min([i[1] for i in coords])
                tx_right = max([i[1] for i in coords])

                tid_attrib = 'transcript_id "' + tid + '"'
                gid_attrib = 'gene_id "' + gid + '"'
                gname_attrib = 'gene "' + gname + '"'

                if gid not in genes_done: 
                    gx_left, gx_right = gene_dict[gid]
                    attribs = ' '.join([gid_attrib, gname_attrib])
                    print(chrom, 'air_temple', 'gene', gx_left, gx_right, 
                        '.', strand, '.', attribs, sep = '\t', file = outgtf)
                    genes_done.add(gid)

                attribs = ' '.join([gid_attrib, gname_attrib, tid_attrib])
                print(chrom, 'air_temple', 'transcript', tx_left, tx_right, 
                    '.', strand, '.', attribs, sep = '\t', file = outgtf)
                if strand == '+':
                    for e in exons:
                        print(chrom, 'air_temple', 'exon', e[0][1], e[1][1], 
                            '.', strand, '.', attribs, sep = '\t', file = outgtf)
                elif strand == '-':
                    for e in exons:
                        print(chrom, 'air_temple', 'exon', e[1][1], e[0][1], 
                            '.', strand, '.', attribs, sep = '\t', file = outgtf)
