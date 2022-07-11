"""Contains main entry point to the program and helper functions"""
import os
import click
from rule_adjectives.rule_graph import RuleParser
from rule_adjectives.annotations import Annotations

__version__ = '0.0.2'


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
@click.argument('out_tsv', type=click.Path(exists=False), required=1)
@click.option('-a', '--adjectives', multiple=True, default=[])
@click.option('-p', '--plot_adjectives', multiple=True, default=[])
@click.option('-g', '--plot_genomes', multiple=True, default=[])
@click.option('--plot_path', type=click.Path(exists=False),
              default=None)
@click.option('--rules_tsv', type=click.Path(exists=True),
              default=get_package_path('rules.tsv'),
              help='The path that will become a folder of output plots, no path no plots.') # , help='The rules file which adhere to strict formating' )
# @click.argument('-p', type=click.Path(exists=True))
def evaluate(annotations_tsv:str, out_tsv:str,
             rules_tsv:str=get_package_path('rules.tsv'),
             adjectives:list=None, plot_adjectives:list=None,
             plot_genomes:list=None,plot_path:str=None):
    """
    Using a DRAM annotations file make a table of adjectives.

    :param annotations_tsv: Path to a DRAM annotations file.
    :param out_tsv: Path for the output true false table.
    :param rules_tsv: Path to a rules file with strict formating, this is optional.
    :param adjectives: Adjectives to evaluate.
    :param plot_adjectives: Adjectives to plot
    :param plot_genomes: Genomes to plot.
    :param plot_path: The path that will become a folder of output plots, no path no plots.
    """
    rules = RuleParser(rules_tsv, verbose=False,
                       adjectives=adjectives)
    annotations = Annotations(annotations_tsv)
    # annotations.ids_by_fasta.iloc[1]['annotations']
    output = rules.check_genomes(annotations)
    if plot_path is not None :
        rules.plot_cause(plot_path, adjectives=plot_adjectives,
                                genomes=plot_genomes, show_steps=False)
    output.to_csv(out_tsv, sep='\t')



