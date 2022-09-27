"""
test the ability to parse the rules graph
import os
os.system('python3 tests/test_graph_query.py')

"""
import os
import click
from rule_adjectives.rule_graph import RuleParser
from rule_adjectives.annotations import Annotations, get_ids_from_annotation
import pytest
import pandas as pd
import numpy
import networkx as nx

TEST_RULES_FILE = "tests/input_data/small_rules.tsv"
TEST_ANNOTATIONS_FILE = "tests/input_data/test_annotations.tsv"
TEST_NO_S_FE_ANNOTATIONS_FILE = "tests/input_data/test_annotations_no_s_no_f.tsv"


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
    exp_out = {'K00000', 'EC:1.1.1.11', '1', 'D0001', 'sulfur1'}
    assert exp_out == rules.find_positve_leaves('ids'), \
        ('Rules are not being parsed for positive correctly')


def test_curent_rules():
    """This is not the only test you need, you should actually look at the graph"""
    rules = RuleParser('../rule_adjectives//rule_adjectives//rules.tsv', verbose=False)
    nx.drawing.nx_pydot.write_dot(
        nx.relabel_nodes(
            rules.G, 
            {i: i.replace(':', '-') for i in rules.G.nodes}),
        'temp_dot.dot')
    os.system('dot -Tpdf temp_dot.dot -o temp_dot.pdf')


def test_rules():
    rules = RuleParser(TEST_RULES_FILE, verbose=False)
    annotations = Annotations(TEST_ANNOTATIONS_FILE)
    adjectives_dat = rules.check_genomes(annotations)
    nx.drawing.nx_pydot.write_dot(
        nx.relabel_nodes(
            rules.G, 
            {i: i.replace(':', '-') for i in rules.G.nodes}),
        'temp_dot.dot')
    os.system('dot -Tpdf temp_dot.dot -o temp_dot.pdf')
    # rules.plot_rule("tests/output_data/plot_rules")
    # rules.plot_cause("./tests/output_data/plot_cause")
    assert len(list(rules.G.successors('funcs-and-0'))) == 2


def test_key_remover():
    rules = RuleParser(TEST_RULES_FILE, verbose=False)
    annotations = Annotations(TEST_NO_S_FE_ANNOTATIONS_FILE)
    adjectives_dat = rules.check_genomes(annotations)
    assert 'Ids' not in adjectives_dat.columns
    assert 'Funcs' in adjectives_dat.columns





