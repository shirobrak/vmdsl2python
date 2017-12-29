# -*- coding: utf-8 -*-

# VDM-SLの構文解析器

# ライブラリの読み込み
import ply.yacc as yacc

# VDM-SLの字句解析器をインポート
from vdmlexer import tokens
from vdm_ast import VdmAstGenerator

ast = VdmAstGenerator()

# 定義ブロック = 型定義群 | 状態定義群 | 値定義群 | 関数定義群 | 操作定義群 ;
def p_definition_block(p):
    """ definition_block : type_definition_group
                         | state_definition
                         | value_definition_group
                         | function_definition_group
                         | operation_definition_group """
    p[0] = p[1]

# 型定義群
def p_type_definition_group(p):
    """ type_definition_group : TYPES optional_type_definition_group """
    p[0] = ast.make_type_definition_group(p)

def p_optional_type_definition_group(p):
    """ optional_type_definition_group : type_definition optional_type_definition_group_part option_semi_expression 
                                       | empty"""
    p[0] = ast.make_optional_type_definition_group(p)

def p_optional_type_definition_group_part(p):
    """ optional_type_definition_group_part : optional_type_definition_group_part SEMI type_definition
                                            | empty """
    if len(p) == 4:
        if p[1] != None:
            p[0] = p[1]+[p[3]]
        else:
            p[0] = [p[3]]

# 型定義
def p_type_definition(p):
    """ type_definition : IDENT EQUAL vdmsl_type inv_condition_option 
                        | IDENT COLON COLON item_list inv_condition_option """
    p[0] = ast.make_type_definition(p)

# 型
def p_vdmsl_type(p):
    """ vdmsl_type : brackets_type
                   | basic_type
                   | quotation_type 
                   | record_type 
                   | merger_type 
                   | tuple_type 
                   | selective_type 
                   | set_type 
                   | column_type 
                   | map_type 
                   | partial_function_type 
                   | type_name 
                   | type_variable """
    p[0] = p[1]

# is基本型
def p_is_basic_type(p):
    """ is_basic_type : IS_BOOL
                      | IS_NAT
                      | IS_NAT1
                      | IS_INT
                      | IS_RAT
                      | IS_REAL
                      | IS_CHAR
                      | IS_TOKEN """
    p[0] = ast.make_is_basic_type(p)

# 括弧型 = ‘(’, 型, ‘)’ ;
def p_brackets_type(p):
    """ brackets_type : LPAR vdmsl_type RPAR """

# 基本型 = ‘bool’ | ‘nat’ | ‘nat1’ | ‘int’ | ‘rat’ | ‘real’ | ‘char’ | ‘token’ ;
def p_basic_type(p):
    """ basic_type : BOOL
                   | NAT
                   | NAT1
                   | INT
                   | RAT
                   | REAL
                   | CHAR
                   | TOKEN """
    p[0] = ast.make_basic_type(p)

# 引用型 = ‘<’, 引用リテラル, ‘>’ ;
def p_quotation_type(p):
    """ quotation_type : LT QUOTELTR GT """
    p[0] = ast.make_quote_type(p)

# レコード型 = ‘compose’, 識別子, ‘of’, 項目リスト, ‘end’ ;
def p_record_type(p):
    """ record_type : COMPOSE IDENT OF item_list END """
    p[0] = ast.make_record_type(p)

# 項目リスト = { 項目 } ;
def p_item_list(p):
    """ item_list : item_list item
                  | empty """
    if len(p) == 3:
        if p[1] != None:
            p[0] = p[1:]
        else:
            p[0] = p[2]

# 項目 = [ 識別子, ‘:’ ], 型 | [ 識別子, ‘:-’ ], 型 ;
def p_item(p):
    """ item : IDENT COLON vdmsl_type
             | IDENT COLON MINUS vdmsl_type
             | vdmsl_type """
    p[0] = ast.make_item(p)

# 合併型 = 型, ‘|’, 型, { ‘|’, 型 } ;
def p_merger_type(p):
    """ merger_type : vdmsl_type VERTICAL vdmsl_type merger_type_part """
    p[0] = ast.make_merger_type(p)

# 合併型部品
def p_merger_type_part(p):
    """ merger_type_part : merger_type_part VERTICAL vdmsl_type
                         | empty """
    if len(p) == 4:
        if p[1] != None:
            p[0] = [p[1]+p[3]]
        else:
            p[0] = [p[3]]

# 組型 = 型, ‘*’, 型, { ‘*’, 型 } ;
def p_tuple_type(p):
    """ tuple_type : vdmsl_type ASTER vdmsl_type tuple_type_part """
    p[0] = ast.make_tuple_type(p)

# 組型部品
def p_tuple_type_part(p):
    """ tuple_type_part : tuple_type_part ASTER vdmsl_type
                        | empty """
    if len(p) == 4:
        if p[1] != None:
            p[0] = [p[1]+p[3]]
        else:
            p[0] = [p[3]]
            
# 選択型 = ‘[’, 型, ‘]’ ;
def p_selective_type(p):
    """ selective_type : LBRACK vdmsl_type RBRACK """
    p[0] = ast.make_selective_type(p)

# 集合型 = ‘set of’, 型 ;
def p_set_type(p):
    """ set_type : SET OF vdmsl_type """
    p[0] = ast.make_set_type(p)

# 列型 = 空列を含む列型 | 空列を含まない列型 ;
def p_column_type(p):
    """ column_type : seq_of_type 
                    | seq1_of_type """
    p[0] = p[1]

# 空列を含む列型 = ‘seq of’, 型 ;
def p_seq_of_type(p):
    """ seq_of_type : SEQ OF vdmsl_type """
    p[0] = ast.make_seq_type(p)

# 空列を含まない列型 = ‘seq1 of’, 型 ;
def p_seq1_of_type(p):
    """ seq1_of_type : SEQ1 OF vdmsl_type """
    p[0] = ast.make_seq1_type(p)

# 写像型 = 一般写像型 | 1 対 1 写像型 ;
def p_map_type(p):
    """ map_type : general_map_type
                 | inmap_type """
    p[0] = p[1]

# 一般写像型 = ‘map’, 型, ‘to’, 型 ;
def p_general_map_type(p):
    """ general_map_type : MAP vdmsl_type TO vdmsl_type """
    p[0] = ast.make_map_type(p)


# 1 対 1 写像型 = ‘inmap’, 型, ‘to’, 型 ;
def p_inmap_type(p):
    """ inmap_type : INMAP vdmsl_type TO vdmsl_type """
    p[0] = ast.make_inmap_type(p)

# 関数型 = 部分関数型 | 全関数型 ;
def p_function_type(p):
    """ function_type : partial_function_type 
                      | full_function_type """
    p[0] = p[1]

# 部分関数型 = 任意の型, ‘->’, 型
def p_partial_function_type(p):
    """ partial_function_type : any_type ARROW vdmsl_type """
    p[0] = ast.make_partial_function_type(p)

# 全関数型 = 任意の型, ‘+>’, 型
def p_full_function_type(p):
    """ full_function_type : any_type PARROW vdmsl_type """
    p[0] = ast.make_full_function_type(p)
    
# 任意の型 = 型 | ‘(’, ‘)’ ;
def p_any_type(p):
    """ any_type : vdmsl_type 
                 | LPAR RPAR """
    p[0] = ast.make_any_type(p)

# 型名称 = 名称 ;
def p_type_name(p):
    """ type_name : name """
    p[0] = ast.make_type_name(p)

# 型変数 = 型変数識別子 ;
def p_type_variable(p):
    """ type_variable : type_variable_ident """
    p[0] = ast.make_type_variable(p)

# 状態定義 = ‘state’, 識別子, ‘of’, 項目リスト, [ 不変条件 ], [ 初期化 ], ‘end’, [ ‘;’ ] ;
def p_state_definition(p):
    """ state_definition : STATE IDENT OF item_list inv_condition_option initialization_option END SEMI """
    p[0] = ast.make_state_definition(p)

# 不変条件 = ‘inv’, 不変条件初期関数 ;
def p_inv_condition(p):
    """ inv_condition : INV inv_condition_init_function """
    p[0] = ast.make_inv_condition(p)

# 不変条件オプション
def p_inv_condition_option(p):
    """ inv_condition_option : inv_condition 
                             | empty """
    p[0] = p[1]

# 初期化 = ‘init’, 不変条件初期関数 ;
def p_initialization(p):
    """ initialization : INIT inv_condition_init_function """
    p[0] = ast.make_initialization(p)

def p_initialization_option(p):
    """ initialization_option : initialization
                              | empty """
    p[0] = p[1]

# 不変条件初期関数 = パターン, ‘==’, 式 ;
def p_inv_condition_init_function(p):
    """ inv_condition_init_function : pattern WEQUAL expression """
    p[0] = ast.make_inv_cond_init_function(p)

# 値定義群 = ‘values’, [ 値定義, { ‘;’, 値定義 }, [ ‘;’ ] ] ;
def p_value_definition_group(p):
    """ value_definition_group : VALUES value_definition_group_option
                               | VALUES """

# 値定義群オプション構文
def p_value_definition_group_option(p):
    """value_definition_group_option : value_definition value_definition_group_option_part 
                                     | value_definition value_definition_group_option_part SEMI
                                     | empty"""

# 値定義群オプション構文 部品
def p_value_definition_group_option_part(p):
    """ value_definition_group_option_part : value_definition_group_option_part SEMI value_definition 
                                           | empty """

# 値定義 = パターン, [ ‘:’, 型 ], ‘=’, 式 ;
def p_value_definition(p):
    """ value_definition : pattern COLON vdmsl_type EQUAL expression 
                         | pattern EQUAL expression """

# 関数定義群 = ‘functions’, [ 関数定義, { ‘;’, 関数定義 }, [ ‘;’ ] ] ;
def p_function_definition_group(p):
    """ function_definition_group : FUNCTIONS function_definition_group_option
                                  | FUNCTIONS """

def p_function_definition_group_option(p):
    """ function_definition_group_option : function_definition function_definition_group_option_part SEMI """

def p_function_definition_group_option_part(p):
    """ function_definition_group_option_part : function_definition_group_option_part SEMI function_definition
                                              | empty """

# 関数定義 = 陽関数定義 | 陰関数定義 | 拡張陽関数定義 ;
def p_function_definition(p):
    """ function_definition : explicit_function_definition
                            | implicit_function_definition
                            | expanded_explicit_function_definition """

# 事前条件オプション
def p_pre_cond_option(p):
    """ pre_cond_option : PRE expression
                        | empty """

# 事後条件オプション
def p_post_cond_option(p):
    """ post_cond_option : POST expression
                         | empty """


# 型変数リスト = ‘[’, 型変数識別子, { ‘,’, 型変数識別子 }, ‘]’ ;
def p_type_variable_list(p):
    """ type_variable_list : LBRACK type_variable_ident type_variable_list_part RBRACK """

def p_type_variable_list_part(p):
    """ type_variable_list_part : type_variable_list_part COMMA type_variable_ident 
                                  | empty """

# 型変数リストオプション
def p_type_variable_list_option(p):
    """ type_variable_list_option : type_variable_list 
                                    | empty """

# 陽関数定義 = 識別子, [ 型変数リスト ], ‘:’, 関数型, 識別子, パラメーターリスト, ‘==’, 関数本体, [ ‘pre’, 式 ], [ ‘post’, 式 ], [ ‘measure’, 名称 ] ; 
def p_explicit_function_definition(p):
    """ explicit_function_definition : IDENT type_variable_list_option COLON function_type IDENT param_list WEQUAL function_body pre_cond_option post_cond_option explicit_function_definition_option1 """

def p_explicit_function_definition_option1(p):
    """ explicit_function_definition_option1 : MEASURE name
                                             | empty """

# 陰関数定義 = 識別子, [ 型変数リスト ], パラメーター型, 識別子型ペアリスト, [ ‘pre’, 式 ], ‘post’, 式 ;
def p_implicit_function_definition(p):
    """ implicit_function_definition : IDENT type_variable_list_option param_type ident_type_pair_list pre_cond_option POST expression """


# 拡張陽関数定義 = 識別子, [ 型変数リスト ],パラメーター型, 識別子型ペアリスト, ‘==’, 関数本体, [ ‘pre’, 式 ], [ ‘post’, 式 ] ;
def p_expanded_explicit_function_definition(p):
    """ expanded_explicit_function_definition : IDENT type_variable_list_option param_type ident_type_pair_list WEQUAL function_body pre_cond_option post_cond_option """


# 識別子型ペア = 識別子, ‘:’, 型 ;
def p_ident_type_pair(p):
    """ ident_type_pair : IDENT  COLON vdmsl_type """

# パラメーター型 = ‘(’, [ パターン型ペアリスト ], ‘)’ ;
def p_param_type(p):
    """ param_type : LPAR pattern_type_pair_list_option RPAR """

# 識別子型ペアリスト = 識別子, ‘:’, 型, { ‘,’, 識別子, ‘:’, 型 } ;
def p_ident_type_pair_list(p):
    """ ident_type_pair_list : IDENT COLON vdmsl_type ident_type_pair_list_part """

def p_ident_type_pair_list_part(p):
    """ ident_type_pair_list_part : ident_type_pair_list_part COMMA IDENT COLON vdmsl_type
                                  | empty """

# パターン型ペアリスト = パターンリスト, ‘:’, 型, { ‘,’, パターンリスト,‘:’, 型 } ;
def p_pattern_type_pair_list(p):
    """ pattern_type_pair_list : pattern_list COLON vdmsl_type pattern_type_pair_list_part """

def p_pattern_type_pair_list_part(p):
    """ pattern_type_pair_list_part : pattern_type_pair_list_part COMMA pattern_list COLON vdmsl_type 
                                    | empty """

def p_pattern_type_pair_list_option(p):
    """ pattern_type_pair_list_option : pattern_type_pair_list
                               | empty """

# パラメーターリスト = パラメーター群, { パラメーター群 } ;
def p_param_list(p):
    """ param_list : param_group param_list_part """

def p_param_list_part(p):
    """ param_list_part : param_list_part param_group
                        | empty """

# パターンリストオプション
def p_pattern_list_option(p):
    """ pattern_list_option : pattern_list
                            | empty """

# パラメーター群 = ‘(’, [ パターンリスト ], ‘)’ ;
def p_param_group(p):
    """ param_group : LPAR pattern_list_option RPAR """

# 関数本体 = 式 | ‘is not yet specified’ ;
def p_function_body(p):
    """ function_body : expression 
                      | IS_ NOT YET SPECIFIED """


# 操作定義群 = ‘operations’, [ 操作定義, { ‘;’, 操作定義 }, [ ‘;’ ] ] ;
def p_operation_definition_group(p):
    """ operation_definition_group : OPERATIONS operation_definition_group_option """

def p_operation_definition_group_option(p):
    """ operation_definition_group_option : operation_definition operation_definition_group_option_part
                                          | operation_definition operation_definition_group_option_part SEMI 
                                          | empty """

def p_operation_definition_group_option_part(p):
    """ operation_definition_group_option_part : operation_definition_group_option_part SEMI operation_definition 
                                               | empty """
    
    
# 操作定義 = 陽操作定義 | 陰操作定義 | 拡張陽操作定義 ;
def p_operation_definition(p):
    """ operation_definition : explicit_operation_definition
                             | implicit_operation_definition
                             | expanded_explicit_operation_definition """

# 陽操作定義 = 識別子, ‘:’, 操作型, 識別子, パラメーター群, ‘==’, 操作本体, [ ‘pre’, 式 ], [ ‘post’, 式 ] ;
def p_explicit_operation_definition(p):
    """ explicit_operation_definition : IDENT COLON operation_type IDENT param_group WEQUAL operation_body pre_cond_option post_cond_option """

# 陰操作定義 = 識別子, パラメーター型, [ 識別子型ペアリスト ], 陰操作本体 ;
def p_implicit_operation_definition(p):
    """ implicit_operation_definition : IDENT param_type ident_type_pair_list_option implicit_operation_body """

# 識別子型ペアリストオプション
def p_ident_type_pair_list_option(p):
    """ ident_type_pair_list_option : ident_type_pair_list 
                                    | empty """

# 陰操作本体 = [ 外部節 ], [ ‘pre’, 式 ], ‘post’, 式, [ 例外 ] ;
def p_implicit_operation_body(p):
    """ implicit_operation_body : ext_section_option pre_cond_option POST expression exception_option """

# 外部節オプション
def p_ext_section_option(p):
    """ ext_section_option : ext_section 
                           | empty """

def p_exception_option(p):
    """ exception_option : exception 
                         | empty """

# 拡張陽操作定義 = 識別子, パラメーター型, [ 識別子型ペアリスト ], ‘==’, 操作本体, [ 外部節 ], [ ‘pre’, 式 ], [ ‘post’, 式 ], [ 例外 ] ;
def p_expanded_explicit_operation_definition(p):
    """ expanded_explicit_operation_definition : IDENT param_type ident_type_pair_list_option WEQUAL operation_body ext_section_option pre_cond_option post_cond_option exception_option """

# 操作型 = 任意の型, ‘==>’, 任意の型 ;
def p_operation_type(p):
    """ operation_type : any_type WEQARROW any_type """

# 操作本体 = 文 | ‘is not yet specified’ ;
def p_operation_body(p):
    """ operation_body : statement 
                       | IS NOT YET SPECIFIED """

# 外部節 = ‘ext’, var 情報, { var 情報 } ;
def p_ext_section(p):
    """ ext_section : EXT var_infomation ext_section_part """

def p_ext_section_part(p):
    """ ext_section_part : ext_section_part var_infomation
                         | empty """

# var 情報 = モード, 名称リスト, [ ‘:’, 型 ] ;
def p_var_infomation(p):
    """ var_infomation : mode name_list COLON vdmsl_type 
                       | mode name_list """

# モード = ‘rd’ | ‘wr’ ;
def p_mode(p):
    """ mode : RD
             | WR """

# 名称リスト = 識別子, { ‘,’, 識別子 } ;
def p_name_list(p):
    """ name_list : IDENT name_list_part """

def p_name_list_part(p):
    """ name_list_part : name_list_part COMMA IDENT 
                       | empty """

# 例外 = ‘errs’, エラーリスト ;
def p_exception(p):
    """ exception : ERRS error_list """

# エラーリスト = エラー, { エラー } ;
def p_error_list(p):
    """ error_list : error_expr error_list_part """

def p_error_list_part(p):
    """ error_list_part : error_list_part error_expr
                        | empty """

# エラー = 識別子, ‘:’, 式, ‘->’, 式 ;
def p_error_expr(p):
    """ error_expr : IDENT COLON expression ARROW expression """

# 式リスト = 式 , {‘,’, 式}
def p_expression_list(p):
    """ expression_list : expression expression_list_part """

def p_expression_list_part(p):
    """ expression_list_part : expression_list_part COMMA expression 
                             | empty """

# 式
def p_expression(p):
    """ expression : brackets_expression
                   | let_expression
                   | let_be_expression
                   | def_expression
                   | if_expression
                   | cases_expression
                   | unary_expression
                   | binomial_expression
                   | limit_expression
                   | iota_expression
                   | set_enumeration
                   | set_comprehension
                   | set_range_expression
                   | column_enumeration
                   | column_comprehension
                   | subsequence
                   | map_comprehension
                   | map_enumeration
                   | tuple_constructor
                   | record_constructor
                   | record_modifier
                   | application
                   | item_choice
                   | tuple_choice
                   | functional_instantiation
                   | lambda_expression
                   | general_is_expression
                   | undefined_expression
                   | name
                   | oldname
                   | symbol_ltr """
    p[0] = ast.make_expression(p)


# 括弧式 = ‘(’, 式, ‘)’ ;
def p_brackets_expression(p):
    """ brackets_expression : LPAR expression RPAR """
    p[0] = ast.make_brackets_expression(p)

# let 式 = ‘let’, ローカル定義, { ‘,’, ローカル定義 }, ‘in’, 式 ;
def p_let_expression(p):
    """ let_expression : LET let_expression_part IN expression """

def p_let_expression_part(p):
    """ let_expression_part : let_expression_part COMMA local_definition 
                            | local_definition """

# let be 式 = ‘let’, 束縛, [ ‘be’, ‘st’, 式 ], ‘in’, 式 ;
def p_let_be_expression(p):
    """ let_be_expression : LET binding optional_be_st_expression IN expression """

# def 式 = ‘def’, パターン束縛, ‘=’, 式, { ‘;’, パターン束縛, ‘=’, 式 }, [ ‘;’ ], ‘in’, 式 ;
def p_def_expression(p):
    """ def_expression : DEF pattern_binding EQUAL expression def_expression_part option_semi_expression IN expression """

def p_def_expression_part(p):
    """ def_expression_part : def_expression_part SEMI pattern_binding EQUAL expression 
                            | empty """

# if 式 = ‘if’, 式, ‘then’, 式, { elseif 式 }, ‘else’, 式 ;
def p_if_expression(p):
    """ if_expression : IF expression THEN expression if_expression_part ELSE expression """

def p_if_expression_part(p):
    """ if_expression_part : if_expression_part elseif_expression 
                           | empty """

# elseif 式 = ‘elseif’, 式, ‘then’, 式 ;
def p_elseif_expression(p):
    """ elseif_expression : ELSEIF expression THEN expression """

# cases 式 = ‘cases’, 式, ‘:’, cases 式選択肢群, [ ‘,’, others 式 ], ‘end’ ;
def p_cases_expression(p):
    """ cases_expression : CASES expression COLON cases_expression_option_group optional_cases_expression END """

def p_optional_cases_expression(p):
    """ optional_cases_expression : COMMA others_expression
                                  | empty """

# cases 式選択肢群 = cases 式選択肢, { ‘,’, cases 式選択肢 } ;
def p_cases_expression_option_group(p):
    """ cases_expression_option_group : cases_expression_option cases_expression_option_group_part """

def p_cases_expression_option_group_part(p):
    """ cases_expression_option_group_part : cases_expression_option_group_part COMMA cases_expression_option 
                                           | empty"""

# cases 式選択肢 = パターンリスト, ‘->’, 式 ;
def p_cases_expression_option(p):
    """ cases_expression_option : pattern_list ARROW expression """

# others 式 = ‘others’, ‘->’, 式 ;
def p_others_expression(p):
    """ others_expression : OTHERS ARROW expression """

# 単項式 = 接頭辞式 | 逆写像 ;
def p_unary_expression(p):
    """ unary_expression : prefix_expression
                         | inverse_mapping  """

# 接頭辞式 = 単項演算子, 式 ;
def p_prefix_expression(p):
    """ prefix_expression : PLUS expression 
                          | MINUS expression
                          | ABS expression
                          | FLOOR expression
                          | NOT expression
                          | CARD expression 
                          | POWER expression 
                          | DUNION expression
                          | DINTER expression
                          | HD expression 
                          | TL expression
                          | LEN expression
                          | ELEMS expression
                          | INDS expression
                          | CONC expression
                          | DOM expression
                          | RNG expression
                          | MERGE expression """

# 逆写像 = ‘inverse’, 式 ;
def p_inverse_mapping(p):
    """ inverse_mapping : INVERSE expression """

# 2項式 = 式, 2 項演算子, 式 ;
def p_binomial_expression(p):
    """ binomial_expression : expression PLUS expression
                            | expression MINUS expression
                            | expression ASTER expression
                            | expression SLASH expression
                            | expression REM expression
                            | expression DIV expression
                            | expression MOD expression
                            | expression LT expression 
                            | expression LTEQ expression
                            | expression GT expression 
                            | expression GTEQ expression 
                            | expression EQUAL expression 
                            | expression OR expression 
                            | expression AND expression
                            | expression LTGT expression
                            | expression EQARROW expression 
                            | expression LTEQGT expression
                            | expression IN SET expression
                            | expression NOT IN SET expression
                            | expression SUBSET expression
                            | expression PSUBSET expression
                            | expression UNION expression
                            | expression BACKSLASH expression
                            | expression INTER expression
                            | expression MUL expression
                            | expression WPLUS expression
                            | expression MUNION expression
                            | expression LTCOL expression
                            | expression LARCOL expression 
                            | expression COLGT expression
                            | expression RARCOL expression
                            | expression COMP expression 
                            | expression WASTER expression
                             """


# 限量式 = 全称限量式 | 存在限量式 | 1存在限量式 ;
def p_limit_expression(p):
    """ limit_expression : forall_expression
                         | exists_expression
                         | exists1_expression """

# 全称限量式 = ‘forall’, 束縛リスト, ‘&’, 式 ;
def p_forall_expression(p):
    """ forall_expression : FORALL binding_list ANDOP expression """

# 存在限量式 = ‘exists’, 束縛リスト, ‘&’, 式 ;
def p_exists_expression(p):
    """ exists_expression : EXISTS binding_list ANDOP expression """

# 1存在限量式 = ‘exists1’, 束縛, ‘&’, 式 ;
def p_exists1_expression(p):
    """ exists1_expression : EXISTS1 binding ANDOP expression """

# iota 式 = ‘iota’, 束縛, ‘&’, 式 ;
def p_iota_expression(p):
    """ iota_expression : IOTA binding ANDOP expression """

# 集合列挙 = ‘{’, [ 式リスト ], ‘}’ ;
def p_set_enumeration(p):
    """ set_enumeration : LBRACE option_expression_list RBRACE """

# 集合内包 = ‘{’, 式, ‘|’, 束縛リスト, [ ‘&’, 式 ], ‘}’ ;
def p_set_comprehension(p):
    """ set_comprehension : LBRACE expression VERTICAL binding_list option_andop_expression RBRACE """

# 集合範囲式 = ‘{’, 式, ‘,’, ‘...’, ‘,’, 式, ‘}’ ;
def p_set_range_expression(p):
    """ set_range_expression : LBRACE expression COMMA TRIDOT COMMA expression RBRACE """

# 列列挙 = ‘[’, [ 式リスト ], ‘]’ ;
def p_column_enumeration(p):
    """ column_enumeration : LBRACK option_expression_list RBRACK """

# 列内包 = ‘[’, 式, ‘|’, 集合束縛, [ ‘&’, 式 ], ‘]’ ;
def p_column_comprehension(p):
    """ column_comprehension : LBRACK expression VERTICAL set_binding option_andop_expression RBRACK """

# 部分列 = 式, ‘(’, 式, ‘,’, ‘...’, ‘,’, 式, ‘)’ ;
def p_subsequence(p):
    """ subsequence : expression LPAR expression COMMA TRIDOT COMMA expression RPAR """


# 写像列挙 = ‘{’, 写, { ‘,’, 写 }, ‘}’ | ‘{’, ‘|->’, ‘}’ ;
def p_map_enumeration(p):
    """ map_enumeration : LBRACE copy map_enumeration_part RBRACE
                        | LBRACE VERARROW RBRACE """

def p_map_enumeration_part(p):
    """ map_enumeration_part : map_enumeration_part COMMA copy
                             | empty """

# 写 = 式, ‘|->’, 式 
def p_copy(p):
    """ copy : expression VERARROW expression """

# 写像内包 = ‘{’, 写, ‘|’, 束縛リスト, [ ‘&’, 式 ], ‘}’ ;
def p_map_comprehension(p):
    """ map_comprehension : LBRACE copy VERTICAL binding_list option_andop_expression RBRACE """

# 組構成子 = ‘mk_’, ‘(’, 式, ‘,’, 式リスト, ‘)’ ;
def p_tuple_constructor(p):
    """ tuple_constructor : MK_ LPAR expression COMMA expression_list RPAR """

# レコード構成子 = ‘mk_’, 名称, ‘(’, [ 式リスト ], ‘)’ ;
# 名称：境界文字は許されない
def p_record_constructor(p):
    """ record_constructor : MK_ name LPAR option_expression_list RPAR """

# レコード修正子 = ‘mu’, ‘(’, 式, ‘,’, レコード修正, { ‘,’, レコード修正 }, ‘)’ ;
def p_record_modifier(p):
    """ record_modifier : MU LPAR expression COMMA record_update record_modifier_part RPAR """

def p_record_modifier_part(p):
    """ record_modifier_part : record_modifier_part COMMA record_update
                             | empty """

# レコード修正 = 識別子, ‘|->’, 式 ;
def p_record_update(p):
    """ record_update :  IDENT VERARROW expression """

# 適用 = 式, ‘(’, [ 式リスト ], ‘)’
def p_application(p):
    """ application : expression LPAR option_expression_list RPAR """

# 項目選択 = 式, ‘.’, 識別子 ;
def p_item_choice(p):
    """ item_choice : expression DOT IDENT """

# 組選択 = 式, ‘.#’, 数字 ;
def p_tuple_choice(p):
    """ tuple_choice : expression DOTSHARP number """

# 関数型インスタンス化 = 名称, ‘[’, 型, { ‘,’, 型 }, ‘]’
def p_functional_instantiation(p):
    """ functional_instantiation : name LBRACK vdmsl_type functional_instantiation_part RBRACK """

def p_functional_instantiation_part(p):
    """ functional_instantiation_part : functional_instantiation_part COMMA vdmsl_type 
                                      | empty """

# ラムダ式 = ‘lambda’, 型束縛リスト, ‘&’, 式 ;
def p_lambda_expression(p):
    """ lambda_expression : LAMBDA type_binding_list ANDOP expression """

# 一般 is 式 = is 式 | 型判定 ;
def p_general_is_expression(p):
    """ general_is_expression : is_expression 
                              | type_judgment  """

# is 式 = ‘is_’,24 名称, ‘(’, 式, ‘)’ | is 基本型, ‘(’, 式, ‘)’ ;
# 24名称 : 境界文字は許されない
def p_is_expression(p):
    """ is_expression : IS_ name LPAR expression RPAR 
                      | is_basic_type LPAR expression RPAR """

# 型判定 = ‘is_’, ‘(’, 式, ‘,’, 型, ‘)’ ;
def p_type_judgment(p):
    """ type_judgment : IS_ LPAR expression COMMA vdmsl_type RPAR """

# 未定義式 = ‘undefined’ ;
def p_undefined_expression(p):
    """ undefined_expression : UNDEFINED """

# 名称
def p_name(p):
    """ name : IDENT """
    p[0] = ast.make_name(p)

# 旧名称
def p_oldname(p):
    """ oldname : IDENT '~' """
    p[0] = ast.make_oldname(p)
    
    

# 記号リテラル
def p_symbol_ltr(p):
    """symbol_ltr : NUMLTR
                  | TRUE
                  | FALSE
                  | NIL
                  | CHARLTR
                  | TEXTLTR
                  | QUOTELTR """
    p[0] = ast.make_symbol_literal(p)

# 文構文
def p_statement(p):
    """ statement : let_statement
                  | let_be_statement
                  | def_statement
                  | block_statement
                  | general_assignment_statement
                  | if_statement
                  | cases_statement
                  | column_for_statement
                  | set_for_statement
                  | index_for_statement
                  | while_statement
                  | non_determination_statement
                  | call_statement
                  | specification_description_statement
                  | return_statement
                  | always_statement
                  | trap_statement
                  | recursive_statement
                  | exit_statement
                  | error_statement
                  | identity_statement """

# let 文 = ‘let’, ローカル定義, { ‘,’, ローカル定義 }, ‘in’, 文 ;
def p_let_statement(p):
    """ let_statement : LET local_definition let_statement_part IN statement """

def p_let_statement_part(p):
    """ let_statement_part : let_statement_part COMMA local_definition
                           | empty """

# ローカル定義 = 値定義　| 関数定義 ;
def p_local_definition(p):
    """ local_definition : value_definition 
                         | function_definition """
    p[0] = make_local_definition(p)

# let be 文 = ‘let’, 束縛, [ ‘be’, ‘st’, 式 ], ‘in’, 文 ;
def p_let_be_statement(p):
    """ let_be_statement : LET binding optional_be_st_expression IN statement """

# def 文 = ‘def’, 相等定義, { ‘;’, 相等定義 }, [ ‘;’ ], ‘in’, 文 ;
def p_def_statement(p):
    """ def_statement : DEF equality_definition def_statement_part option_semi_expression IN statement """

def p_def_statement_part(p):
    """ def_statement_part : def_statement_part SEMI equality_definition
                           | empty """

# 相等定義 = パターン束縛, ‘=’, 式 ;
def p_equality_definition(p):
    """ equality_definition : pattern_binding EQUAL expression """

# ブロック文 = ‘(’, { dcl 文 }, 文, { ‘;’, 文 }, [ ‘;’ ], ‘)’ ;
def p_block_statement(p):
    """ block_statement : LPAR block_statement_part1 statement block_statement_part2 option_semi_expression RPAR """

def p_block_statement_part1(p):
    """ block_statement_part1 : block_statement_part1 dcl_statement
                              | empty """

def p_block_statement_part2(p):
    """ block_statement_part2 : block_statement_part2 SEMI statement 
                              | empty """


# dcl 文 = ‘dcl’, 代入定義, { ‘,’, 代入定義 }, ‘;’ ;
def p_dcl_statement(p):
    """ dcl_statement : DCL assignment_definition dcl_statement_part SEMI """

def p_dcl_statement_part(p):
    """ dcl_statement_part : dcl_statement_part COMMA assignment_definition 
                           | empty """

# 代入定義 = 識別子, ‘:’, 型, [ ‘:=’, 式 ] ;
def p_assignment_definition(p):
    """ assignment_definition : IDENT COLON vdmsl_type optional_coleqop_expression """

# 一般代入文 = 代入文 | 多重代入文 ;
def p_general_assignment_statement(p):
    """ general_assignment_statement : assignment_statement
                                     | multi_assignment_statement """

# 代入文 = 状態指示子, ‘:=’, 式 ;
def p_assignment_statement(p):
    """ assignment_statement : status_indicator COLEQUAL expression """

# 多重代入文 = ‘atomic’, ‘(’ 代入文, ‘;’, 代入文, { ‘;’, 代入文 }‘)’ ;
def p_multi_assignment_statement(p):
    """ multi_assignment_statement : ATOMIC LPAR assignment_statement SEMI assignment_statement multi_assignment_statement_part RPAR """

def p_multi_assignment_statement_part(p):
    """ multi_assignment_statement_part : multi_assignment_statement_part SEMI assignment_statement 
                                        | empty """

# if 文 = ‘if’, 式, ‘then’, 文, { elseif 文 }, [ ‘else’, 文 ] ;
def p_if_statement(p):
    """ if_statement : IF expression THEN statement if_statement_part optional_else_statement """

def p_if_statement_part(p):
    """ if_statement_part : if_statement_part elseif_statement
                          | empty """

# elseif 文 = ‘elseif’, 式, ‘then’, 文 ;
def p_elseif_statement(p):
    """ elseif_statement : ELSEIF expression THEN statement """

# cases 文 = ‘cases’, 式, ‘:’, cases 文選択肢群, [ ‘,’, others 文 ], ‘end’ ;
def p_cases_statement(p):
    """ cases_statement : CASES expression COLON cases_statement_option_group optional_commma_others_statement """

def p_optional_commma_others_statement(p):
    """ optional_commma_others_statement : COMMA others_statement 
                                         | empty """

# cases 文選択肢群 = cases 文選択肢, { ‘,’, cases 文選択肢 } ;
def p_cases_statement_option_group(p):
    """ cases_statement_option_group : cases_statement_option cases_statement_option_group_part """

def p_cases_statement_option_group_part(p):
    """ cases_statement_option_group_part : cases_statement_option_group_part COMMA cases_statement_option 
                                          | empty """

# cases 文選択肢 = パターンリスト, ‘->’, 文 ;
def p_cases_statement_option(p):
    """ cases_statement_option : pattern_list ARROW statement """

# others 文 = ‘others’, ‘->’, 文 ;
def p_others_statement(p):
    """ others_statement : OTHERS ARROW statement """

# 列 for ループ = ‘for’, パターン束縛, ‘in’, [ ‘reverse’ ], 式, ‘do’, 文 ;
def p_column_for_statement(p):
    """ column_for_statement : FOR pattern_binding IN optional_reverse expression DO statement """

# 集合 for ループ = ‘for’, ‘all’, パターン, ‘in set’, 式, ‘do’, 文 ;
def p_set_for_statement(p):
    """ set_for_statement : FOR ALL pattern IN SET expression DO statement """

# 索引 for ループ = ‘for’, 識別子, ‘=’, 式, ‘to’, 式, [ ‘by’, 式 ], ‘do’, 式 ;
def p_index_for_statement(p):
    """ index_for_statement : FOR IDENT EQUAL expression TO expression optional_byop_expression DO expression """

# while ループ = ‘while’, 式, ‘do’, 式 ;
def p_while_statement(p):
    """ while_statement : WHILE expression DO expression """

# 非決定文 = ‘||’, ‘(’, 文, { ‘,’, 文 }, ‘)’ ;
def p_non_determination_statement(p):
    """ non_determination_statement : WVERTICAL LPAR statement non_determination_statement_part RPAR """

def p_non_determination_statement_part(p):
    """ non_determination_statement_part : non_determination_statement_part COMMA statement 
                                         | empty """

# call 文 = 名称, ‘(’, [ 式リスト ], ‘)’ ;
def p_call_statement(p):
    """ call_statement : name LPAR option_expression_list RPAR """

# return 文 = ‘return’, [ 式 ] ;
def p_return_statement(p):
    """ return_statement : RETURN optional_expression """

# 仕様記述文 = ‘[’, 陰操作本体, ‘]’ ;
def p_specification_description_statement(p):
    """ specification_description_statement : LBRACK implicit_operation_body RBRACK """

# always 文 = ‘always’, 文, ‘in’, 文 ;
def p_always_statement(p):
    """ always_statement : ALWAYS statement IN statement """

# trap 文 = ‘trap’, パターン束縛, ‘with’, 文, ‘in’, 文 ;
def p_trap_statement(p):
    """ trap_statement : TRAP pattern_binding WITH statement statement IN statement """

# 再帰 trap 文 = ‘tixe’, trap 群, ‘in’, 文 ;
def p_recursive_statement(p):
    """ recursive_statement : TIXE trap_group IN statement """

# trap 群 = ‘{’, パターン束縛, ‘|->’, 文, { ‘,’, パターン束縛, ‘|->’, 文 }, ‘}’ ;
def p_trap_group(p):
    """ trap_group : LBRACE pattern_binding VERARROW statement trap_group_part LBRACE """

def p_trap_group_part(p):
    """ trap_group_part : trap_group_part COMMA pattern_binding VERARROW statement 
                        | empty """

# exit 文 = ‘exit’, [ 式 ] ;
def p_exit_statement(p):
    """ exit_statement : EXIT optional_expression """

# error 文 = ‘error’ ;
def p_error_statement(p):
    """ error_statement : ERROR """

# 恒等文 = ‘skip’ ;
def p_identity_statement(p):
    """ identity_statement : SKIP """

# 状態指示子 = 名称 | 項目参照 | 写像参照または列参照 ;
def p_status_indicator(p):
    """ status_indicator : name
                         | item_reference 
                         | map_or_column_reference """

# 項目参照 = 状態指示子, ‘.’, 識別子 ;
def p_item_reference(p):
    """ item_reference : status_indicator DOT IDENT """

# 写像参照または列参照 = 状態指示子, ‘(’, 式, ‘)’ ;
def p_map_or_column_reference(p):
    """ map_or_column_reference : status_indicator LPAR expression RPAR """

# パターン
def p_pattern(p):
    """ pattern : pattern_ident
                | match_value
                | set_enumeration_pattern
                | set_union_pattern
                | column_enumeration_pattern
                | column_link_pattern
                | map_enumeration_pattern
                | map_munion_pattern
                | tuple_pattern
                | record_pattern"""
    p[0] = p[1]          

# パターン識別子
def p_pattern_ident(p):
    """ pattern_ident : IDENT
                      | '-' """
    p[0] = p[1]

# 一致値
def p_match_value(p):
    """ match_value : LPAR expression RPAR
                    | symbol_ltr """
    
# 集合列挙パターン
def p_set_enumeration_pattern(p):
    """ set_enumeration_pattern : LBRACE pattern_list RBRACE
                                | LBRACE RBRACE """ 
    
# 集合合併パターン
def p_set_union_pattern(p):
    """ set_union_pattern : pattern UNION pattern """

# 列列挙パターン
def p_column_enumeration_pattern(p):
    """ column_enumeration_pattern : LBRACK pattern_list RBRACK
                                   | LBRACK RBRACK """
    
# 列連結パターン
def p_column_link_pattern(p):
    """ column_link_pattern : pattern MUL pattern """

# 写像列挙パターン
def p_map_enumeration_pattern(p):
    """ map_enumeration_pattern : LBRACE map_pattern_list RBRACE
                                  | LBRACE RBRACE """                              

# 写パターンリスト
def p_map_pattern_list(p):
    """ map_pattern_list : map_pattern map_pattern_list_part """

# 写パターンリスト部品
def p_map_pattern_list_part(p):
    """ map_pattern_list_part : map_pattern_list_part COMMA map_pattern 
                              | empty """

# 写パターン
def p_map_pattern(p):
    """ map_pattern : pattern VERARROW pattern """

# 写像併合パターン
def p_map_munion_pattern(p):
    """ map_munion_pattern : pattern MUNION pattern """

# 組パターン
def p_tuple_pattern(p):
    """ tuple_pattern : MK_ LPAR pattern COMMA pattern_list RPAR """

# レコードパターン
def p_record_pattern(p):
    """ record_pattern : MK_ name LPAR pattern_list RPAR 
                       | MK_ name LPAR RPAR """

# パターンリスト
def p_pattern_list(p):
    """ pattern_list : pattern pattern_list_part """

# パターンリスト部品
def p_pattern_list_part(p):
    """ pattern_list_part : pattern_list_part COMMA pattern 
                          | empty """

# パターン束縛
def p_pattern_binding(p):
    """ pattern_binding : pattern 
                        | binding """

# 束縛
def p_binding(p):
    """ binding : set_binding
                | type_binding """

# 集合束縛
def p_set_binding(p):
    """ set_binding : pattern IN SET expression """

# 型束縛
def p_type_binding(p):
    """ type_binding : pattern COLON vdmsl_type """

# 束縛リスト
def p_binding_list(p):
    """ binding_list : multi_binding binding_list_part """

# 束縛リスト部品
def p_binding_list_part(p):
    """ binding_list_part : binding_list_part COMMA multi_binding
                          | empty """

# 多重束縛
def p_multi_binding(p):
    """ multi_binding : multi_set_binding
                      | multi_type_binding """

# 多重集合束縛
def p_multi_set_binding(p):
    """ multi_set_binding : pattern_list IN SET expression """

# 多重型束縛
def p_multi_type_binding(p):
    """ multi_type_binding : pattern_list COLON vdmsl_type """

# 型束縛リスト
def p_type_binding_list(p):
    """ type_binding_list : type_binding type_binding_list_part """

# 型束縛リスト部品
def p_type_binding_list_part(p):
    """ type_binding_list_part : type_binding_list_part COMMA type_binding 
                               | empty """

# 型変数識別子
def p_type_variable_ident(p):
    """ type_variable_ident : '@' IDENT """


# Optional(expression_list)
def p_option_expression_list(p):
    """ option_expression_list : expression_list 
                               | empty """

# Optional('by' + expression)
def p_optional_byop_expression(p):
    """ optional_byop_expression : BY expression
                                 | empty """
# Optional(':=' + expression)
def p_optional_coleqop_expression(p):
    """ optional_coleqop_expression : COLEQUAL expression
                                    | empty """

# Optional(expression)
def p_optional_expression(p):
    """ optional_expression : expression 
                            | empty """

# Optional('&' + expression)
def p_option_andop_expression(p):
    """ option_andop_expression : ANDOP expression
                                | empty """

# Optional(';')
def p_option_semi_expression(p):
    """ option_semi_expression : SEMI 
                               | empty """
    if p[1] != None:
        p[0] = p[1]

# Optional('be'+'st'+expression)
def p_optional_be_st_expression(p):
    """ optional_be_st_expression : BE ST expression
                                  | empty """

# Optional('else' statement)
def p_optional_else_statement(p):
    """ optional_else_statement : ELSE statement 
                                | empty """

# Optional('reverse')
def p_optional_reverse(p):
    """ optional_reverse : REVERSE
                         | empty """

# 空（繰り返し対策）
def p_empty(p):
    'empty :'
    print("empty")
    pass

# 構文エラー
def p_error(p):
    print("Syntax error in input")


# デバッグ
if __name__ == '__main__':  
    
    import logging
    log = logging.getLogger()

    grammer = input('start grammer > ')
    # 構文解析器の構築
    if grammer == '':
        parser = yacc.yacc(start='type_definition_group')
    else:
        parser = yacc.yacc(start=grammer) 

    while True:
        try:
            s = input('vdmsl > ')
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s, debug=log)
        print(result)

        # print("== symbol table ==")
        # for k, v in ast.symbol_table.items():
        #     print("%10s  %10s" % (k, v.__class__.__name__))

