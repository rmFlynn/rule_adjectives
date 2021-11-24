# Rule based adjectives

The script is currently a blunt implement but there is more in there.

## Install

Download the git repo, and change your directory to its root.

Install the conda environment:

```
conda env create enviroment.yml
conda activate rule_adjectives
```

Install the packeg:

```
pip install -e ./
```

## Use

Here is an example:

```
rule_adjectives\
        ./rules.tsv \
        ./annotations.tsv\
        ./adjectives.tsv\
        -a "Autotroph" \
        -a "Heterotroph" \
        -a "sulfatereducer" \
        -a "homoacetogen" \
        -a "methanogen" \
        -a "Denitrifier(Not ETC)" \
        -a "AerobicAmmoniaOxidizer" \
        -a "comammox" \
        -a "annamox" \
        -a "Nitrogenfixer" \
        -a "Phototroph" \
        -a "Fermenter" \
        -a "Aerobe" \
        -a "Microaerophillic" \
        -a "Non ETC Oxidase" \
        -a "Denitrifier"

```
