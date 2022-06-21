"""
Tool to quickly merge relative abundances and adjective data by summing the abundances for all genomes for which a give adjective is true.

So for a quick example is adjective a is true for for genomes 1, and 2 but not three the abundances of adjective a would simply be the sum of the abundances of genomes 1 and 2.

"""

input_adjectives_path = 'abundances.csv'
input_abundances_path = 'adjectives.tsv'
output_path = 'adjectives_abundances.csv'

import pandas as pd

adjs = pd.read_csv(input_abundances_path, sep='\t', index_col=0)
abunds = pd.read_csv(input_abundances_path, index_col=0)

if len(set(adjs.index) & set(abunds.index)) == 0 and len(set(adjs.index) & set(abunds.columns)) > 0:
    abunds = abunds.T

both = pd.merge(adjs, abunds, left_index=True, right_index=True, how='inner')
print(f"Matched {len(both)} genomes")
both.columns
adj_abunds = both[adjs.columns].apply(lambda x: both.loc[x, abunds.columns].sum())

adj_abunds.to_csv(output_path)
