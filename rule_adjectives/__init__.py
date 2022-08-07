"""Contains main entry point to the program and helper functions"""
import os
import click

import pandas as pd

from rule_adjectives.rule_graph import RuleParser, get_positive_genes
from rule_adjectives.annotations import Annotations



__version__ = '0.0.3'


class PythonLiteralOption(click.Option):

    def type_cast_value(self, ctx, value):
        try:
            return ast.literal_eval(value)
        except:
            raise click.BadParameter(value)


def get_package_path(local_path):
    """
    Locate the package data or non python files

    :param local_path:
    :returns:
    """
    abs_snake_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)),
        local_path)
    return abs_snake_path


@click.command()
@click.version_option(__version__)
@click.argument('annotations_tsv', type=click.Path(exists=True), required=1)
@click.argument('adjectives_tsv', type=click.Path(), required=1)
@click.option('-a', '--adjectives', multiple=True, default=[])
@click.option('-p', '--plot_adjectives', multiple=True, default=[])
@click.option('-g', '--plot_genomes', multiple=True,
              default=[])
@click.option('--plot_path', type=click.Path(exists=False),
              default=None)
@click.option('--strainer_tsv', type=click.Path(exists=False), default=None)
@click.option('--strainer_type', type=click.Path(exists=False), default=None)
@click.option('--rules_tsv', type=click.Path(exists=True),
              default=get_package_path('rules.tsv'),
              help='The path that will become a folder of output plots, no path no plots.') # , help='The rules file which adhere to strict formating' )
# @click.argument('-p', type=click.Path(exists=True))
def evaluate(annotations_tsv:str, adjectives_tsv:str,
             rules_tsv:str=get_package_path('rules.tsv'),
             adjectives:list=None, plot_adjectives:list=None,
             plot_genomes:list=None,plot_path:str=None,
             strainer_tsv:str=None, strainer_type='pgtb'):
    """
    Using a DRAM annotations file make a table of adjectives.

    :param annotations_tsv: Path to a DRAM annotations file.
    :param adjectives_tsv: Path for the output true false table.
    :param rules_tsv: Path to a rules file with strict formating, this is optional.
    :param adjectives: Adjectives to evaluate.
    :param plot_adjectives: Adjectives to plot
    :param plot_genomes: Genomes to plot.
    :param plot_path: The path that will become a folder of output plots, no path no plots.
    :param strainer_tsv: The path for a tsv that will pass to strainer to filter genes.
    :param strainer_type: The type of proccess that should make the strainer file.
        the only option at this time is pgtb for positive genes that are on true bugs.
    """
    rules = RuleParser(rules_tsv, verbose=False, adjectives=adjectives)
    annotations = Annotations(annotations_tsv)
    adjectives = rules.check_genomes(annotations)
    adjectives.to_csv(adjectives_tsv, sep='\t')
    # annotations.ids_by_fasta.iloc[1]['annotations']
    if plot_path is not None:
        rules.plot_cause(plot_path, adjectives=plot_adjectives,
                         genomes=plot_genomes, show_steps=False)
    if strainer_tsv is not None:
        strainer_data = get_positive_genes(rules, annotations, adjectives)
        strainer_data.to_csv(strainer_tsv, sep='\t')


@click.command()
@click.version_option(__version__)
@click.argument('plot_path', type=click.Path(exists=False),
              default=None)
@click.option('-a', '--adjectives', multiple=True, default=[])
@click.option('--rules_tsv', type=click.Path(exists=True),
              default=get_package_path('rules.tsv'),
              help='The path that will become a folder of output plots, no path no plots.') # , help='The rules file which adhere to strict formating' )
# @click.argument('-p', type=click.Path(exists=True))
def rule_plot(rules_tsv:str=get_package_path('rules.tsv'),
               adjectives:list=None, plot_path:str=None):
    """
    Using a DRAM annotations file make a table of adjectives.

    :param annotations_tsv: Path to a DRAM annotations file.
    :param adjectives_tsv: Path for the output true false table.
    :param rules_tsv: Path to a rules file with strict formating, this is optional.
    :param adjectives: Adjectives to evaluate.
    :param plot_adjectives: Adjectives to plot
    :param plot_genomes: Genomes to plot.
    :param plot_path: The path that will become a folder of output plots, no path no plots.
    :param strainer_tsv: The path for a tsv that will pass to strainer to filter genes.
    :param strainer_type: The type of proccess that should make the strainer file.
        the only option at this time is pgtb for positive genes that are on true bugs.
    """
    rules = RuleParser(rules_tsv, verbose=False, adjectives=adjectives)
    rules.plot_rule(plot_path, adjectives)
