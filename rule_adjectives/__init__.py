"""Contains main entry point to the program and helper functions"""
import os
import click
import ast
from rule_adjectives.rule_graph import RuleParser
from rule_adjectives.annotations import Annotations

class PythonLiteralOption(click.Option):

    def type_cast_value(self, ctx, value):
        try:
            return ast.literal_eval(value)
        except:
            raise click.BadParameter(value)

@click.command()
@click.argument('rules_tsv', type=click.Path(exists=True), required=1) # , help='The rules file which adhere to strict formating' )
@click.argument('annotations_tsv', type=click.Path(exists=True), required=1)
@click.argument('out_tsv', type=click.Path(exists=False), required=1)
@click.option('-a', '--adjectives', multiple=True, default=[])
# @click.argument('-p', type=click.Path(exists=True))
def evaluate(rules_tsv:str, annotations_tsv:str, out_tsv:str,
             adjectives:list=None, plot_path:str=None):
    rules = RuleParser(rules_tsv, verbose=True,
                       adjectives=adjectives)
    annotations = Annotations(annotations_tsv)
    annotations.ids_by_fasta.iloc[1]['annotations']
    output = rules.check_genomes(annotations)
    if plot_path is not None:
        rules.plot_all_adj_all_genome(plot_path)
    output.to_csv(out_tsv, sep='\t')

