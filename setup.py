#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='pygments-practicalalloy',
    version='0.2',
    description='Pygments lexer for Practical Alloy book.',
    keywords='pygments alloy lexer',
    license='GPL v2.0',

    author='Alcio Cunha',
    author_email='alcino@di.uminho.pt',

    url='https://github.com/practicalalloy/pygments-practical-alloy',

    packages=find_packages(),
    install_requires=['pygments >= 1.4'],

    entry_points='''[pygments.lexers]
                    practicalalloy=src:PracticalAlloyLexer
    
                    [pygments.styles]
                    practicalalloy=src:PracticalAlloyStyle''',

    classifiers=[],
)
