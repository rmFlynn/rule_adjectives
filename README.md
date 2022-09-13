# Rule based adjectives

The script is currently a blunt implement but there is more in there.

## Install

Download the git repo, and change your directory to its root.
```
git clone https://github.com/rmFlynn/rule_adjectives.git
cd rule_adjectives
```

Install the conda environment:

```
conda env create -f environment.yaml
conda activate rule_adjectives # Don't forget this step
```

Install the packages:

```
pip3 install -e ./ # yes you need the -e for now
```

This is a temporary method of installation while the program is in beta, but a better method will be created after that.

## Use

Currently you can annotate genomes and print out cause plots.
The options are probably best explained by example.

First use `--help` to see all options. That will provide context.

```
rule_adjectives --help
Usage: rule_adjectives ANNOTATIONS_TSV OUT_TSV [OPTIONS]

  Using a DRAM annotations file make a table of adjectives.

  annotations_tsv: Path to a DRAM annotations file. 
  out_tsv: Path for the output adjectives true / false table. 

Options:
  -a, --adjectives TEXT         #Takes a string of text which equal specific adjectives in the out_tsv adjectives true / false table to report.
  -p, --plot_adjectives TEXT    #Takes a string of text which equal specific adjectives in the out_tsv adjectives true / false table to plot.
  -g, --plot_genomes TEXT       #Takes a string of text which equal the name of a specific (or subset) of genome(s) in the out_tsv adjectives true / false table to plot.
  --plot_path PATH              #The path that will become a folder of output plots. No path - no plots.
  --rules_tsv PATH              #A path of alternative rules that will overwrite the defaults when calling adjectives. 
  --help                        #Show this message and exit.

```

Here is an example that will make a table for all adjectives together:

```
rule_adjectives ./annotations.tsv ./adjectives.tsv
```

Here is an example that will make a table for all adjectives as well as plots for each genome of for each adjective:

```
rule_adjectives ./annotations.tsv ./adjectives.tsv --plot_path ./path_for_plots
```

Here is how you would evaluate just 3 adjective:

```
rule_adjectives ./annotations.tsv ./adjectives.tsv \
        -a "Autotroph" \
        -a "Heterotroph" \
        -a "sulfatereducer"
```

Here is how you would evaluate just 3 adjectives and plot 2 of them for 2 genomes:

```
rule_adjectives ./annotations.tsv ./adjectives.tsv \
        -a "Autotroph" \
        -a "Heterotroph" \
        -a "sulfatereducer" \
        --plot_path 'plots_dec1_3' \
        -p "Autotroph" \
        -p "sulfatereducer" \
        -g bin1.scaffold1 \
        -g bin1.scaffold2
```

DRAM can also help you extract the gene sequences for the adjectives of your choice. This can help for things like making phylogenetic trees of Nar/Nxr/Nap genes.

First, run DRAM Adjectives using the --strainer_tsv argument.
```
rule_adjectives ./annotations.tsv ./adjectives.tsv --strainer_tsv strainer_output.tsv
```
Then, using DRAM strainer, filter out the genes for each of the positive hits. 
Note: You can filter out the table for any specific genes you want to pull out before you run these next commands.
```
DRAM.py strainer -f genes_strainer_out.fna -i strainer_output.tsv
```
# Notes
 * You must annotate with DRAM.1.4 or newer using the **FeGenie** database, for iron annotations to work correctly. 
 * If you are in Wrighton lab using zenith you can access annotations in the scripts' environment, contact Rory Flynn if you have trouble accessing the scripts' environment. 
 * Tree based improvements are in the works. 
