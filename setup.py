"""Setup file for package"""
from setuptools import setup, find_packages
# from some_python_init_file import __version__ as version
from os import path
from rule_adjectives import __version__

__author__ = 'rmflynn'

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="rule_adjectives",
    version=__version__,
    packages=['rule_adjectives/'],
    entry_points={
        "console_scripts": [
            "rule_adjectives = rule_adjectives:evaluate"# ,
            # "snakemake-bash-completion = snakemake:bash_completion",
        ]
    },
    include_package_data=True,  # include all files in MANIFEST.in
    data_files=[],
    description="Get rule based adjective, plot rules, and plot decisions",
    long_description=long_description,
    long_description_content_type='text/markdown',  # Optional (see note above)
    python_requires='>=3',
    install_requires=['pandas', 'numpy', 'pytest'],
    #TODO add mmseqs
    author="Rory Flynn",
    author_email='Rory.Flynn@colostate.edu',
    url="",  # this will change
)

