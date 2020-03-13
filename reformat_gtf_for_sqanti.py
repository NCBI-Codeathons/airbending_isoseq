import argparse

def parse_args():
	# argument parse config stuff
	parser = argparse.ArgumentParser(description=\
	    'Replaces the gene_id field in a TALON gtf with an id of style PB.X.Y '
	    'where X = gene identifier, Y = transcript identifier, ',
	    'removes gene entries')
	parser.add_argument('-gtf', help='gtf file')

def get_field_value(key, fields):
    if key not in fields:
        return None
    else:
        return fields.split(key+' "')[1].split()[0].replace('";','')

def make_ofile_name(matfile, prefix=None):
	fname = matfile.split('.gtf')[0]
	if prefix:
		fname += '_'
		fname += prefix
	fname += '_reformatted.gtf'
	return fname

def remake_attr(fields, new_gid, new_tid):
	x = fields.strip().split('"; ')
	x = [i.strip(';') for i in x]
	attr_dict = {i.split(' "')[0]: i.split(' "')[1] for i in x}

	attr_dict['gene_id'] = new_gid
	attr_dict['transcript_id'] = new_tid

	attr = ''.join(["""{} "{}"; """.format(key, attr_dict[key]) for key in attr_dict.keys()])

	return attr

def main():

	args = parse_args()


	outfile = open(make_ofile_name(args.gtf), 'w')
	infile = open(args.gtf, 'r')

	for line in infile: 
		line = line.strip().split('\t')
		fields = line[-1]

		# remove gene entries
		if line[2] == 'gene': continue

		talon_gid = get_field_value('talon_gene', fields)
		talon_tid = get_field_value('talon_transcript', fields)

		new_gid = 'PB.{}'.format(talon_gid)
		new_tid = 'PB.{}.{}'.format(talon_gid, talon_tid)

		line[-1] = remake_attr(fields, new_gid, new_tid)

		outfile.write('\t'.join(line)+'\n')

	outfile.close()
	infile.close()



if __name__ == '__main__': main()