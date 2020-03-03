#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='pygments-electrum',
    version='0.1',
    description='Pygments lexer for Electrum.',
    keywords='pygments electrum alloy lexer',
    license='GPL v2.0',

    author='Alcio Cunha',
    author_email='alcino@di.uminho.pt',

    url='https://github.com/alcinocunha/pygments-electrum.git',

    packages=find_packages(),
    install_requires=['pygments >= 1.4'],

    entry_points='''[pygments.lexers]
                    electrum=src:ElectrumLexer
    
                    [pygments.styles]
                    electrum=src:ElectrumStyle''',

    classifiers=[],
)
