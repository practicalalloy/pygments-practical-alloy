# -*- coding: utf-8 -*-
"""
    Pygments lexer for the Alloy modeling language
"""
from pygments.lexers.web import HtmlLexer
from pygments.lexer import bygroups, DelegatingLexer, RegexLexer
from pygments.lexers.agile import RubyLexer
from pygments.lexers.templates import ErbLexer
from pygments.token import Token, Text, Keyword, Name, Comment, String, Error, Number, Operator, Generic, Literal, Punctuation

import sys
import collections


"""
PracticalAlloy Lexer class.

This lexer outputs several different Keyword, Name, and Operator tokens:

  * Keyword.Namespace:   'module'
  * Keyword.Declaration: 'sig'
  * Keyword.Constant:    'iden', 'univ', 'none'
  * Keyword.Type:        'int', 'Int', 'Time'
  * Keyword:             'this', 'abstract', 'extends', 'set', 'seq', 'one', 'lone', 'let',
                         'all', 'some', 'no', 'sum', 'disj', 'when', 'else',
                         'var',
                         'run', 'check', 'for', 'but', 'exactly',
                         'fun', 'pred', 'fact', 'assert'

  * Name.Class:          signature declaration names
  * Name.Namespace:      module declaration names
  * Name.Function:       function (fun/pred/fact/assert) declaration names
  * Name:                all other identifiers

  * Operator.Word:       'not', 'and', 'or', 'implies', 'iff', 'in'
                         'always','eventually','after', 'until', 'releases' 
                         'historically', 'once', 'before', 'since', 'triggered'
  * Operator:            '!', '#', '&&', '++', '<<', '>>', '>=', '<=', '<=>', '.', '->',
                         '-', '+', '/', '*', '%', '=', '<', '>', '&', '!', '^', '|', '~',
                         '{', '}', '[', ']', '(', ')','\''

Other outputed tokens are

  * Punctuation:         ',', ':'
  * Comment.Single:      single-line comments starting with '--' or '//'
  * Comment.Multiline:   comments starting with '/*' or '/**' and ending with '*/'
  * Number.Integer       integer literals
  * String:              string literals
  * Text:                whitespace
  * Name:                all identifiers (in Alloy, identifiers are like in Java, except
                         that the single quotation mark may appear anywhere except at the
                         beginning)
"""
class PracticalAlloyLexer(RegexLexer):
    name = 'PracticalAlloy'
    aliases = ['practicalalloy']
    filenames = ['*.als']

    iden_rex = r'[\$@]?[a-zA-Z_…][a-zA-Z0-9_]*[₀-₋ₐ-ₜ\$]*'
    text_tuple = (r'[^\S\n]+', Text)

    tokens = {
        'sig': [
            (r'(extends)\b', Keyword),
            (r'(in)\b', Keyword),
            (r'=', Operator),
            (r'\+', Operator),
            (iden_rex, Name.Class),
            (r'(Int|String)\b', Keyword.Type),
            text_tuple,
            (r',', Punctuation),
            (r'\{', Operator, '#pop'),
        ],
        'module': [
            text_tuple,
            (r'(as)\b', Keyword),
            (iden_rex, Name.Namespace, '#pop'),
        ],
        'fun': [
            text_tuple,
            (r'\{', Operator, '#pop'),
            (iden_rex, Name.Function, '#pop'),
        ],
        'root': [
            (r'--.*?$', Comment.Single),
            (r'//.*?$', Comment.Single),
            (r'/\*(.|\n)*?\*/', Comment.Multiline),
            (r'{-(.|\n)*?-}', Comment.Multiline),
            (r'(sig|enum)(\s+)', bygroups(Keyword.Declaration, Text), 'sig'),
            text_tuple,
            (r'(module|open)(\s+)', bygroups(Keyword.Namespace, Text), 'module'),
            (r'(as)(\s+)', Keyword),
            (r'(iden|univ|none)\b', Keyword.Constant),
            (r'(int|Int|String)\b', Keyword.Type),
            (r'(this|abstract|extends|set|seq|one|lone|as|private)\b', Keyword),
            (r'(all|some|no|sum|disj|when|else|let)\b', Keyword),
            (r'(var)(\s+)', Keyword),
            (r'(run|check|for|but|exactly|steps|expect)\b', Keyword),
            (r'(not|and|or|implies|iff|in)\b', Operator.Word),
            (r'(always|eventually|after|until|releases)\b', Operator.Word),
            (r'(historically|once|before|since|triggered)\b', Operator.Word),
            (r'(fun|pred|fact|assert)(\s+)', bygroups(Keyword, Text), 'fun'),
            (r'!|#|&&|\+\+|<<|>>|>=|<=|<=>|\.|->|:>|<:', Operator),
            (r'[:,]', Punctuation),
            (r'[-+/*%=<>&!^|~\{\}\[\]\(\)\.\';]', Operator),
            (iden_rex, Name),
            (r'[0-9]+', Number.Integer),
            (r'"(\\\\|\\"|[^"])*"', String),
            (r'\n', Text),
        ]
    }

    def process_one(self, curr):
        return curr

############################################################################


from pygments.style import Style
from pygments.styles import get_style_by_name


"""
Style class for the color theme used by the Alloy Analyzer IDE.

This theme does not define different colors for all different tokens
outputed by the lexer; instead it uses one color for all keywords,
another for all comments, and another for all identifiers, just like
the Alloy Analyzer.  The only differences are:

  * this style prints operators in bold
  * in this style, multiline doc comments (starting with '/**') are not bold
    (because the lexer outputs the same token for both kinds of multiline comments)
"""
class PracticalAlloyStyle(Style):
    default_style = ""

    styles = {}
    base = get_style_by_name("tango")
    for token in base.styles.keys():
        styles[token] = base.styles[token]

    styles[Keyword]  = '#1F1FA8 bold'
    styles[Comment]  = '#429E24 italic'
    styles[Operator] = '#000000 bold'
    styles[Literal]  = '#940000'


    styles[Keyword.Constant]    = styles[Keyword]
    styles[Keyword.Declaration] = styles[Keyword]
    styles[Keyword.Namespace]   = styles[Keyword]
    styles[Keyword.Pseudo]      = styles[Keyword]
    styles[Keyword.Reserved]    = styles[Keyword]
    styles[Keyword.Type]        = styles[Keyword]

    styles[Comment.Multiline] = styles[Comment]
    styles[Comment.Preproc]   = styles[Comment]
    styles[Comment.Single]    = styles[Comment]
    styles[Comment.Special]   = styles[Comment]

    styles[Literal.Number.Integer] = styles[Literal]
    styles[Literal.String]         = styles[Literal]

    styles[Operator.Word] = styles[Keyword]
