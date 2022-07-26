"""
Tool to parse the annotations file, and store it in
convenient transformations.
"""
import re
import pandas as pd
import numpy as np
from collections import Counter
from itertools import chain
import dask.dataframe as dd

FUNCTION_DICT = { 
    'camper_id': lambda x: [x],
    'fegenie_id': lambda x: [x],
    'sulfur_id': lambda x: [x],
    'kegg_genes_id': lambda x: [x],
    'ko_id': lambda x: [j for j in x.split(',')],
    'kegg_id': lambda x: [j for j in x.split(',')],
    'kegg_hit': lambda x: [i[1:-1] for i in 
                           re.findall(r'\[EC:\d*.\d*.\d*.\d*\]', x)],
    'peptidase_family': lambda x: [j for j in x.split(';')],
    'cazy_id': lambda x: [i.split('_')[0] for i in x.split('; ')],
    'cazy_hits': lambda x: [f"{i[1:3]}:{i[4:-1]}" for i in 
                            re.findall(r'\(EC [\d+\.]+[\d-]\)', x)],
    'cazy_subfam_ec': lambda x: [f"EC:{i}" for i in 
                                 re.findall(r'[\d+\.]+[\d-]', x)],
    'pfam_hits': lambda x: [j[1:-1].split('.')[0]
                            for j in re.findall(r'\[PF\d\d\d\d\d.\d*\]', x)]
}


def get_ids_from_annotations_by_row(data):
    functions = {i:j for i,j in FUNCTION_DICT.items() if i in data.columns}
    out = data.apply(lambda x: {i for k, v in functions.items() if not pd.isna(x[k])
                          for i in v(str(x[k])) if not pd.isna(i)}, axis=1)
    return out


def get_ids_from_annotations_all(data):
    data =  get_ids_from_annotations_by_row(data)
    data.apply(list)
    out = Counter(chain(*data.values))
    return out


def get_ids_from_annotation(frame):
    return Counter(chain(*frame.apply(get_ids_from_row, axis=1).values))


class Annotations():

    def __init__(self, annotations_tsv:str):
        self.data = None
        self.ids_by_fasta = None
        self.ids_by_row = None
        self.set_annotations(annotations_tsv)

    def set_annotations(self, annotations_tsv:str):
        self.data = pd.read_csv(annotations_tsv, sep='\t', index_col=0, low_memory=False)
        # anno_data['dram_index'] = anno_data.index
        #TODO, make less lame
        self.data.set_index(['fasta', self.data.index], inplace=True)
        #TODO split
        annot_fasta_ids =self.data.groupby('fasta')
        annot_fasta_ids = annot_fasta_ids.apply(get_ids_from_annotations_all)
        annot_fasta_ids = pd.DataFrame(annot_fasta_ids,
                                       columns=['annotations'])
        self.ids_by_fasta = annot_fasta_ids

    def set_annotation_ids_by_row(self):
        # self.raw_annotations = anno_data
        print("generating IDs by index, this may take some time")
        data = self.data.copy()
        # data.set_index(['fasta', data.index], inplace=True)
        annot_ids = get_ids_from_annotations_by_row(self.data)
        annot_ids = pd.DataFrame(annot_ids, columns=['annotations'])
        self.ids_by_row = annot_ids

