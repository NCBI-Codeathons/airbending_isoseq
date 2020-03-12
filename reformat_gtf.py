import argparse
import pandas as pd
from collections import defaultdict

def get_args():

	desc = 'Fixes a GTF with no genes'
	parser = argparse.ArgumentParser(description=desc)

	parser.add_argument('-gtf', '-g', dest='gtf',
		help='gtf to fix')
	args = parser.parse_args()

	return args

# get value associated with keyword in the 9th column of gtf
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

def format_to_write(line): 
	return ''.join('\t'.join([str(i) for i in line])+'\n')

def construct_new_entry(entry, entry_type, min_coord, max_coord):

	entry.type = entry_type
	fields = ''
	gid = entry.gid.tolist()[0]
	gname = entry.gname.tolist()[0]

	entry.start = min_coord
	entry.stop = max_coord

	if entry_type == 'gene' or entry_type == 'transcript':
		fields += 'gene_id "{}";'.format(gid)
		fields += ' gene_name "{}";'.format(gname)
	if entry_type == 'transcript':
		tid = entry.tid.tolist()[0]
		fields += ' transcript_id "{}";'.format(tid)
	entry.fields = fields

	return entry

def main():
	args = get_args()
	gtffile = args.gtf

	outfile = make_ofile_name(gtffile)

	df = pd.read_csv(gtffile, sep='\t',
		names=['chr', 'source', 'type', 'start', 'stop',
		'score', 'strand', 'phase', 'fields'],
		comment='#')

	print(df)

	df['tid'] = df.apply(lambda x: get_field_value('transcript_id', x.fields), axis=1)
	df['gid'] = df.apply(lambda x: get_field_value('gene_id', x.fields), axis=1)
	df['gname'] = df.apply(lambda x: get_field_value('db_xref', x.fields), axis=1)

	gene_mins = df[['gid', 'start']].groupby(by='gid').min().copy(deep=True)
	gene_maxes = df[['gid', 'stop']].groupby(by='gid').max().copy(deep=True)

	transcript_mins = df[['tid', 'start']].groupby(by='tid').min().copy(deep=True)
	transcript_maxes = df[['tid', 'stop']].groupby(by='tid').max().copy(deep=True)

	for gid in df.gid.unique():

		if gid == None:
			continue

		# if there's already an entry
		if len(df.loc[(df.gid == gid) & (df.type == 'gene')].index) != 0:
			pass

		# construct gene entry from its exons
		else: 
			g_min = gene_mins.loc[gid, 'start'].tolist()[0]
			g_max = gene_maxes.loc[gid, 'stop'].tolist()[0]

			# pull info out of constituent transcripts
			g_entry = df.loc[df.gid == gid].head(1).copy(deep=True)
			g_entry = construct_new_entry(g_entry, 'gene', g_min, g_max)

			# and add new entry into the df
			new_loc = entry.index.tolist()[0]
			df_new = pd.concat([df.iloc[:new_loc], t_entry, df.iloc[new_loc:]]).reset_index(drop=True)
			df = df_new

		for tid in df.tid.unique():

			if gid == None or tid == None: 
				continue

			# if there's already an entry 
			if len(df.loc[(df.tid == tid) & (df.type == 'transcript')].index) != 0:
				pass

			# construct transcript entry from its exons
			else:

				t_min = transcript_mins.loc[tid].tolist()[0]
				t_max = transcript_maxes.loc[tid].tolist()[0]

				# pull info out of constituent exons
				t_entry = df.loc[df.tid == tid].head(1).copy(deep=True)
				t_entry = construct_new_entry(t_entry, 'transcript', t_min, t_max)

				# and add new entry into the df
				new_loc = t_entry.index.tolist()[0]
				df_new = pd.concat([df.iloc[:new_loc], t_entry, df.iloc[new_loc:]]).reset_index(drop=True)
				df = df_new

	df.to_csv(outfile, sep='\t', header=False)

if __name__ == '__main__': main()

			
