"""
Tool to parse the annotations file, and store it in
convenient transformations.
"""
import re
import pandas as pd
from collections import Counter

def get_ids_from_annotation(frame):
    id_list = list()
    # get kegg ids
    if 'ko_id' in frame:
        id_list += [j.strip()
                    for i in frame['ko_id'].dropna() for j in i.split(',')]
    # get kegg ids
    if 'kegg_id' in frame:
        id_list += [j.strip()
                    for i in frame.kegg_id.dropna() for j in i.split(',')]
    # get kegg ec numbers
    if 'kegg_hit' in frame:
       id_list += [i[1:-1]
                   for kegg_hit in frame.kegg_hit.dropna()
                   for i in re.findall(r'\[EC:[\d\.]+[\d\.\-]\]', kegg_hit)]
    # get merops ids
    if 'peptidase_family' in frame:
        id_list += [j.strip()
                    for i in frame.peptidase_family.dropna() for j in i.split(';')]
    # get cazy ids
    if 'cazy_hits' in frame:
        # get cazy ec numbers
        [i[1:-1].replace(' ', ':')
         for cazy_hit in frame.cazy_hits.dropna()
         for i in re.findall(r'\(EC [\d\.]+[\d\.\-]\)', cazy_hit)]
    # get pfam ids
    if 'pfam_hits' in frame:
        id_list += [j[1:-1].split('.')[0]
                    for i in frame.pfam_hits.dropna()
                    for j in re.findall(r'\[PF\d\d\d\d\d.\d*\]', i)]
    return Counter(id_list)


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
        annot_fasta_ids = annot_fasta_ids.apply(get_ids_from_annotation)
        annot_fasta_ids = pd.DataFrame(annot_fasta_ids,
                                       columns=['annotations'])
        self.ids_by_fasta = annot_fasta_ids


    def set_annotation_ids_by_row(self):
        # self.raw_annotations = anno_data
        print("generating IDs by index, this may take some time")
        data = self.data.copy()
        data.set_index(['fasta', data.index], inplace=True)
        annot_ids = self.data.apply(
            lambda x: get_ids_from_annotation(pd.DataFrame(x).T),
            axis=1
        )
        annot_ids = pd.DataFrame(annot_ids, columns=['annotations'])
        self.ids_by_row = annot_ids

