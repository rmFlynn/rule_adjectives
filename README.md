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

Install the packeg:

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
```


Here is an example that will make a table for all adjectives together:

```
rule_adjectives ./annotations.tsv ./adjectives.tsv
```

Here is how you would evaluate just 3 adjective:

```
rule_adjectives ./annotations.tsv ./adjectives.tsv \
        -a "Autotroph" \
        -a "Heterotroph" \
        -a "sulfatereducer"
```

Here is how you would evaluate just 3 adjective and plot 2 of them for 2 genomes:

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

# Notes
Iron utilizer is not yet fully supported
