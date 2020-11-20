configfile: 'airbending_config.yaml'

rule all:
    input: 'talon_filter.done'


rule reformat_genome:
    input: config['genome_fasta']
    output: 'genome/reformatted_genome.fa'
    shell: 
        '''
        {reformat_fasta} {{input}} {{output}}
        ''' .format(reformat_fasta = 'reformat_fasta.py')

rule generate_minimap_index:
    input: rules.reformat_genome.output[0]
    output: 'genome/minimap_index.mmi'
    shell:
        '''
        minimap2 -d {output} {input}
        '''

rule reformat_sam:
    input: config['input_aligns']
    output: 'alignments/reformatted_input_aligns.sam'
    shell:
        '''
        {reformat_filter_sam} -i {{input}} -o {{output}}
        ''' .format(reformat_filter_sam = 'reformat_filter_sam.py')

rule reformat_gtf:
    input: config['gtf']
    output: 'annots/reformatted_gtf.gtf'
    shell:
        '''
        {reformat_gtf} -i {{input}} -o {{output}}
        ''' .format(reformat_gtf = 'reformat_gtf.py')

rule clean_transcripts:
    input: 
        samin = rules.reformat_sam.output[0],
        genome = rules.reformat_genome.output[0],
        sjtsv = config['splice_junctions'],
    output: touch('tx_clean.done')
    params: 
        outprefix = 'clean'
    threads: 16 
    shell:
        '''
        {run_txclean} \
          -i {{input.samin}} \
          -o {{params.outprefix}} \
          -g {{input.genome}} \
          -j {{input.sjtsv}} \
          -t {{threads}}
        ''' .format(run_txclean = 'run_txclean.sh')

rule label_reads:
    input: 
        tx_clean = rules.clean_transcripts.output[0],
        samin = '/Users/computercraftmac/GCA_000146045.2_R64_feature_table.txt',
        genome = rules.reformat_genome.output[0],
    output: touch('talon_labels.done')
    params:
        outprefix = 'label',
        range_size = '9999',
    threads: 16
    shell:
        '''
        {run_talon_label_reads} \
          -i {{input.samin}} \
          -o {{params.outprefix}} \
          -g {{input.genome}} \
          -r {{params.range_size}} \
          -t {{threads}}
        ''' .format(run_talon_label_reads = 'run_talon_label_reads.sh')

rule create_talondb:
    input: 
        gtf = rules.reformat_gtf.output[0]
    output: touch('talondb.done')
    params:
        outprefix = 'talondb',
        genome = 'GRCh38',
        annot_name = 'RefSeq'
    shell:
        '''
        {run_talon_initialize_database} \
          -i {{input.gtf}} \
          -o {{params.outprefix}} \
          -g {{params.genome}} \
          -a {{params.annot_name}}
        '''

rule talon_collapse:
    input: 
        talon_labels = rules.label_reads.output[0],
        config_file = '/Users/computercraftmac/GCA_000146045.2_R64_feature_table.txt',
        talondb = rules.create_talondb.output[0],
    output: touch('talon_collapse.done')
    params:
        outprefix = 'talon',
        genome = 'GRCh38'
    threads: 16
    shell:
        '''
        {run_talon} \
          -i {{input.config_file}} \
          -o {{params.outprefix}} \
          -d {{input.talondb}} \
          -g {{params.genome}} \
          -t {{threads}}
        ''' .format(run_talon = 'run_talon.sh')

rule filter_talon_tx:
    input: 
        talon_collapse = rules.talon_collapse.output[0],
        talondb = rules.create_talondb.output[0],
    output: touch('talon_filter.done')
    params:
        outprefix = 'talon_filter',
        annot_name = 'RefSeq'
    shell:
        '''
        {run_talon_filter_tx} \
          -d {{input.talondb}} \
          -o {{params.outprefix}} \
          -a {{params.annot_name}}
        ''' .format(run_talon_filter_tx = 'run_talon_filter_transcripts.sh')

    