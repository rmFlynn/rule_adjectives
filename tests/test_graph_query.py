"""test the ability to parse the rules graph"""
import os
import click
from rule_adjectives.rule_graph import RuleParser
from rule_adjectives.annotations import Annotations, get_ids_from_annotation
import pytest
import pandas as pd
import numpy

TEST_RULES_FILE = "tests/input_data/small_rules.tsv"
TEST_ANNOTATIONS_FILE = "tests/input_data/test_annotations.tsv"

def test_find_positve_leaves():
    rules = RuleParser(TEST_RULES_FILE, 
                       verbose=False, adjectives=None)
    # rules.plot_rule("tests/output_data/plot_rules")
    exp_out = {'K00001', 'K00002', 'K00003', 'K00004', 
               'columnvalue:gt:1:heme_regulatory_motif_count', 
               'K00005'}
    assert exp_out == rules.find_positve_leaves('funcs'), \
        ('Rules are not being parsed for positive correctly')
    # rules.plot_rule("tests/output_data/plot_rules")
    exp_out = {'K00000', 'EC1.1.1.11', '1', 'D0001', 'sulfur1'}
    assert exp_out == rules.find_positve_leaves('ids'), \
        ('Rules are not being parsed for positive correctly')


def test_rules():
    rules = RuleParser(TEST_RULES_FILE, verbose=False)
    annotations = Annotations(TEST_ANNOTATIONS_FILE)
    adjectives_dat = rules.check_genomes(annotations)
    rules.plot_rule("tests/output_data/plot_rules")
    rules.plot_cause("./tests/output_data/plot_cause")
    exp_out = {'K00001', 'K00002', 'K00003', 'K00004', 'K00005', 'K00000'}




# gene_adj.set_index([gene_adj['fasta'], gene_adj.index], inplace=True)
# pd.merge(gene_adj, anno_data, how='left')



""".
rules = RuleParser(TEST_RULES_FILE, verbose=False)
annotations = Annotations(TEST_ANNOTATIONS_FILE)
adjectives_dat = rules.check_genomes(annotations)
get_positive_genes(rules, annotations, adjectives_dat)

import os
os.system('rule_adjectives data/annotations_pw_drepped_with_cf.tsv results/adjectives_pw_drepped_with_cf.tsv')
"""
