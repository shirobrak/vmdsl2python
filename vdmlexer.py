# -*- coding: utf-8 -*-

# VDM-SLの字句解析器

# ライブラリの読み込み
import ply.lex as lex

# トークンリスト
tokens = (
    'IDENT',
    'NUMLTR',
    'TEXTLTR',
    'CHARLTR',
    'QUOTELTR',
    'COMMA',
    'COLON',
    'SEMI',
    'EQUAL',
    'LPAR',
    'RPAR',
    'VERTICAL',
    'MINUS',
    'LBRACK',
    'RBRACK',
    'LBRACE',
    'RBRACE',
    'PLUS',
    'SLASH',
    'LT',
    'GT',
    'LTEQ',
    'GTEQ',
    'LTGT',
    'DOT',
    'ASTER',
    'ARROW',
    'PARROW',
    'WEQARROW',
    'WVERTICAL',
    'EQARROW',
    'LTEQGT',
    'VERARROW',
    'LTCOL',
    'COLGT',
    'LARCOL',
    'RARCOL',
    'ANDOP',
    'WEQUAL',
    'WASTER',
    'MUL',
    'WPLUS',
)

# キーワードリスト
keyword = {
    'abs': 'ABS', 'all': 'ALL', 'always': 'ALWAYS', 'and': 'AND', 'as': 'AS', 'atomic': 'ATOMIC', 'be': 'BE', 'bool': 'BOOL', 'by': 'BY', 'card': 'CARD', 'cases': 'CASES', 'char': 'CHAR', 'comp': 'COMP', 'compose': 'COMPOSE', 'conc': 'CONC', 'dcl': 'DCL', 'def': 'DEF', 'definitions': 'DEFINITIONS', 'dinter': 'DINTER', 'div': 'DIV', 'dlmodule': 'DLMODULE', 'do': 'DO', 'dom': 'DOM', 'dunion': 'DUNION', 'elems': 'ELEMS', 'else': 'ELSE', 'elseif': 'ELSEIF', 'end': 'END', 'error': 'ERROR', 'errs': 'ERRS', 'exists': 'EXISTS', 'exists1': 'EXISTS1', 'exit': 'EXIT', 'exports': 'EXPORTS', 'ext': 'EXT', 'false': 'FALSE', 'floor': 'FLOOR', 'for': 'FOR', 'forall': 'FORALL', 'from': 'FROM', 'functions': 'FUNCTIONS', 'hd': 'HD', 'if': 'IF', 'imports': 'IMPORTS', 'in': 'IN', 'inds': 'INDS', 'init': 'INIT', 'inmap': 'INMAP', 'int': 'INT', 'inter': 'INTER', 'inv': 'INV', 'inverse': 'INVERSE', 'iota': 'IOTA', 'is_': 'IS_', 'lambda': 'LAMBDA', 'len': 'LEN', 'let': 'LET', 'make_': 'MAKE_', 'map': 'MAP', 'narrow_': 'NARROW_', 'measure': 'MEASURE', 'merge': 'MERGE', 'mod': 'MOD', 'module': 'MODULE', 'mu_': 'MU_', 'munion': 'MUNION', 'nat': 'NAT', 'nat1': 'NAT1', 'nil': 'NIL', 'not': 'NOT', 'of': 'OF', 'operations': 'OPERATIONS', 'or': 'OR', 'others': 'OTHERS', 'post': 'POST', 'power': 'POWER', 'pre': 'PRE', 'psubset': 'PSUBSET', 'rat': 'RAT', 'rd': 'RD', 'real': 'REAL', 'rem': 'REM', 'renamed': 'RENAMED', 'return': 'RETURN', 'reverse': 'REVERSE', 'rng': 'RNG', 'seq': 'SEQ', 'seq1': 'SEQ1', 'set': 'SET', 'skip': 'SKIP', 'specified': 'SPECIFIED', 'st': 'ST', 'state': 'STATE', 'struct': 'STRUCT', 'subset': 'SUBSET', 'then': 'THEN', 'tixe': 'TIXE', 'tl': 'TL', 'to': 'TO', 'token': 'TOKEN', 'trap': 'TRAP', 'true': 'TRUE', 'types': 'TYPES', 'undefined': 'UNDEFINED', 'union': 'UNION', 'uselib': 'USELIB', 'values': 'VALUES', 'while': 'WHILE', 'with': 'WITH', 'wr': 'WR', 'yet': 'YET', 'RESULT': 'RESULT'
    }

# キーワードを追加
tokens += tuple(keyword.values())

# その他の文字を設定
literals = r'_‘’\"@~#'

# 境界文字
t_COMMA = r','
t_COLON = r':'
t_SEMI = r';'
t_EQUAL = r'='
t_LPAR = r'\('
t_RPAR = r'\)'
t_VERTICAL = r'\|'
t_MINUS = r'-'
t_LBRACK = r'\['
t_RBRACK = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_PLUS = r'\+'
t_SLASH = r'/'
t_LT = r'<'
t_GT = r'>'
t_LTEQ = r'<='
t_GTEQ = r'>='
t_LTGT = r'<>'
t_DOT = r'\.'
t_ASTER = r'\*'
t_ARROW = r'->'
t_PARROW = r'\+>'
t_WEQARROW = r'==>'
t_WVERTICAL = r'\|\|'
t_EQARROW = r'=>'
t_LTEQGT = r'<=>'
t_VERARROW = r'\|->'
t_LTCOL = r'<:'
t_COLGT = r':>'
t_LARCOL = r'<-:'
t_RARCOL = r':->'
t_ANDOP = r'&'
t_WEQUAL = r'=='
t_WASTER = r'\*\*'
t_MUL = r'\^'
t_WPLUS = r'\+\+'


# 識別子
def t_IDENT(t):
    r'[a-zA-Z][a-zA-Z_’0-9]*'
    # キーワードのチェック
    t.type = keyword.get(t.value, 'IDENT')
    return t

"""
リテラルの実装について
とりあえず先に動くものを作りたいので, 文字は英数字限定. 
ギリシャ文字や日本語, ハングル語についてはあとで追加実装する.
"""

# 数字リテラル
def t_NUMLTR(t):
    r'((0x|0X)[0-9a-fA-F]+)|(\d+(\.\d)?((E|e)(\+|\-)?\d)?)'
    return t

# テキストリテラル
def t_TEXTLTR(t):
    r'\"((\"\")|([a-zA-Z0-9])|\s)*\"'
    return t

#　文字リテラル（多文字対応後回し）
def t_CHARLTR(t):
    r'’[a-zA-Z0-9]’'
    return t

# 引用リテラル
def t_QUOTELTR(t):
    r'<[a-zA-Z](_|\w)*>'
    return t

# 行番号を辿れるように
def t_new_line(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# スペース及びタブは無視
t_ignore = ' \t'

# エラーハンドリングルール
def t_error(t):
    print("不正な文字：'%s" %t.value)

# lexer を構築
lexer = lex.lex()

if __name__ == '__main__':
    pass

    # ここからテスト記述
    # print("program test...\n")
    # data = '''
    #   cases e :
    #    p11, p12,...,p1n -> e1,
    #     ...
    #    pm1, pm2,...,pmn -> em,
    #    others -> e(m+1)
    #   end]
    # '''
    # lexer.input(data)
    # while True:
    #     tok = lexer.token()
    #     if not tok:  
    #         print("これ以上トークンはない")
    #         break
    #     print(tok)
