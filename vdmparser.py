# -*- coding: utf-8 -*-

# VDM-SLの構文解析器

# ライブラリの読み込み
import ply.yacc as yacc

# VDM-SLの字句解析器をインポート
from vdmlexer import tokens

# 式構文
def p_expression(p):
    """expression : bracket_expr
                  | let_expr
                  | name
                  | oldname 
                  | symbol_ltr"""
    print("p_expression")
    p[0] = p[1]
    
# 括弧式
def p_bracket_expr(p):
    'bracket_expr : LPAR expression RPAR'
    p[0] = [p[1],p[2],p[3]]

# let式
def p_let_expr(p):
    'let_expr : LET local_definition let_expr_part IN expression'
    if p[3] != None:
        p[0] = p[1:]
    else:
        p[0] = p[1:3] + p[4:]

# let式　繰り返し構文
def p_let_expr_part(p):
    """let_expr_part : COMMA local_definition
                     | empty """
    if p[1] == ',':
        p[0] = [p[1],[p2]]

# ローカル定義
def p_local_definition(p):
    'local_definition :'
    p[0] = ["local_definition"]


# 名称
def p_name(p):
    'name : IDENT part_name'
    if p[2] != None:
        print(p[1])
        print(p[2])
        p[0] = [p[1]+p[2]]
    else:
        p[0] = [p[1]]

# 名称のパーツ
def p_part_name(p):
    """part_name : '‘' IDENT 
                 | empty"""
    print("part_name")
    if p[1]=='‘' :
        p[0] = p[1]+p[2]
    
# 旧名称
def p_oldname(p):
    """oldname : IDENT '~'"""
    print("oldname")
    p[0] = [p[1]+p[2]]

# 記号リテラル
def p_symbol_ltr(p):
    """symbol_ltr : NUMLTR
                  | TRUE
                  | FALSE
                  | NIL
                  | CHARLTR
                  | TEXTLTR
                  | QUOTELTR """
    p[0] = [p[1]]

# 空（繰り返し対策）
def p_empty(p):
    'empty :'
    pass

# 構文エラー
def p_error(p):
    print("Syntax error in input")
 
# 構文解析器の構築
parser = yacc.yacc()

# デバッグ
if __name__ == '__main__':  
    while True:
        try:
            s = input('vdmsl > ')
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s)
        print(result)

