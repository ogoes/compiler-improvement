
from ply import lex

import lexer.rules as rules

lexer = lex.lex(module=rules)
