# -*- coding: utf-8 -*-

from vdm_nodes import *

class VdmAstGenerator():
    """ VDM-SLのAST構築クラス  """

    def __init__(self):
        self.symbol_table = {}


    # 式
    def make_expression(self, tokens):
        """ 式　ノード作成 """
        return Expression(tokens[1], tokens.lineno, tokens.lexpos)

    def make_brackets_expression(self, tokens):
        """ 括弧式 ノード作成 """
        return BracketExpression(tokens[2], tokens.lineno, tokens.lexpos)

    def make_let_expression(self, tokens):
        """ let 式 ノード作成 """
        return LetExpression([tokens[2]]+tokens[3], tokens[5], tokens.lineno, tokens.lexpos)

    def make_let_be_expression(self, tokens):
        """ let be 式 ノード作成 """
        return LetBeExpression(tokens[2], tokens[3], tokens[5], tokens.lineno, tokens.lexpos)

    def make_def_expression(self, tokens):
        """ def 式 ノード作成 """
        ptn_bind = [DefPtnBinding(tokens[2], tokens[4])]
        return DefExpression(ptn_bind+tokens[5], tokens[8], tokens.lineno, tokens.lexpos)

    def make_def_ptn_binding(self, ptn_binding, expr):
        """ def 式 パターン束縛&式 組 """
        return DefPtnBinding(ptn_binding, expr)
        
    def make_prefix_expression(self, tokens):
        """ 接頭辞式 ノード作成 """
        if tokens[1] == '+':
            return Plus(tokens[2], tokens.lineno, tokens.lexpos)
        elif tokens[1] == '-':
            return Minus(tokens[2], tokens.lineno, tokens.lexpos)
        elif tokens[1] == 'abs':
            return Abs(tokens[2], tokens.lineno, tokens.lexpos)
        elif tokens[1] == 'floor':
            return Floor(tokens[2], tokens.lineno, tokens.lexpos)
        elif tokens[1] == 'not':
            return Not(tokens[2], tokens.lineno, tokens.lexpos)
        elif tokens[1] == 'card':
            return Card(tokens[2], tokens.lineno, tokens.lexpos)
        elif tokens[1] == 'power':
            return Power(tokens[2], tokens.lineno, tokens.lexpos)
        elif tokens[1] == 'dunion':
            return Dunion(tokens[2], tokens.lineno, tokens.lexpos)
        elif tokens[1] == 'dinter':
            return Dinter(tokens[2], tokens.lineno, tokens.lexpos)
        elif tokens[1] == 'hd':
            return Hd(tokens[2], tokens.lineno, tokens.lexpos)
        elif tokens[1] == 'tl':
            return Tl(tokens[2], tokens.lineno, tokens.lexpos)
        elif tokens[1] == 'len':
            return Len(tokens[2], tokens.lineno, tokens.lexpos)
        elif tokens[1] == 'elems':
            return Elems(tokens[2], tokens.lineno, tokens.lexpos)
        elif tokens[1] == 'inds':
            return Inds(tokens[2], tokens.lineno, tokens.lexpos)
        elif tokens[1] == 'conc':
            return Conc(tokens[2], tokens.lineno, tokens.lexpos)
        elif tokens[1] == 'dom':
            return Dom(tokens[2], tokens.lineno, tokens.lexpos)
        elif tokens[1] == 'rng':
            return Rng(tokens[2], tokens.lineno, tokens.lexpos)
        elif tokens[1] == 'merge':
            return Merge(tokens[2], tokens.lineno, tokens.lexpos)
        else:
            return None
    
    def make_inverse_mapping(self, tokens):
        """ 逆写像 ノード作成 """
        return Inverse(tokens[2], tokens.lineno, tokens.lexpos)

    def make_binomial_expression(self, tokens):
        """ 二項式 ノード作成 """
        if tokens[2] == '+':
            return Add(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)
        elif tokens[2] == '-':
            return Sub(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)
        elif tokens[2] == '*':
            return Mul(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)
        elif tokens[2] == '/':
            return Div(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)
        elif tokens[2] == 'div':
            return IntDiv(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)
        elif tokens[2] == 'rem':
            return Rem(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)
        elif tokens[2] == 'mod':
            return Mod(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)
        elif tokens[2] == '<':
            return Lt(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)
        elif tokens[2] == '<=':
            return LtEq(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)
        elif tokens[2] == '>':
            return Gt(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)
        elif tokens[2] == '>=':
            return GtEq(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)
        elif tokens[2] == '=':
            return Equal(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)
        elif tokens[2] == '<>':
            return NotEq(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)
        elif tokens[2] == 'or':
            return Or(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)
        elif tokens[2] == 'and':
            return And(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)
        elif tokens[2] == '=>':
            return Imp(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)
        elif tokens[2] == '<=>':
            return Equivalence(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)
        elif tokens[2] == 'in set':
            return InSet(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)
        elif tokens[2] == 'not in set':
            return NotInSet(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)
        elif tokens[2] == 'subset':
            return Subset(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)
        elif tokens[2] == 'psubset':
            return PSubset(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)
        elif tokens[2] == 'union':
            return Union(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)
        elif tokens[2] == '\\':
            return SetDiff(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)
        elif tokens[2] == 'inter':
            return Inter(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)
        elif tokens[2] == '^':
            return ColLink(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)
        elif tokens[2] == '++':
            return MapColUpdate(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)
        elif tokens[2] == 'munion':
            return Munion(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)
        elif tokens[2] == '<:':
            return MapDomRes(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)
        elif tokens[2] == '<-:':
            return MapDomRed(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)
        elif tokens[2] == ':>':
            return MapRangeRes(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)
        elif tokens[2] == ':->':
            return MapRangeRed(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)
        elif tokens[2] == 'comp':
            return Comp(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)
        elif tokens[2] == '**':
            return Rep(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)
        else:
            return None

    def make_local_definition(self, tokens):
        return LocalDefinitions(tokens[1], tokens.lineno, tokens.lexpos)

    def make_if_expression(self, tokens):
        """ if 式 ノード作成 """
        return IfExpression(tokens[2], tokens[4], tokens[5], tokens[7], tokens.lineno, tokens.lexpos)

    def make_elseif_expression(self, tokens):
        """ elseif 式 ノード作成 """
        return ElseIfExpression(tokens[2], tokens[4], tokens.lineno, tokens.lexpos) 

    def make_cases_expression(self, tokens):
        """ cases 式 ノード作成 """
        return CasesExpression(tokens[2], tokens[4], tokens[5], tokens.lineno, tokens.lexpos)

    def make_cases_expr_option(self, tokens):
        """ cases 式選択肢 """
        return CasesExprOption(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)

    def make_forall_expression(self, tokens):
        """ 全称限量式 ノード作成 """
        return ForallExpression(tokens[2], tokens[4], tokens.lineno, tokens.lexpos)

    def make_exists_expression(self, tokens):
        """ 存在限量式 ノード作成 """
        return ExistsExpression(tokens[2], tokens[4], tokens.lineno, tokens.lexpos)

    def make_exists1_expression(self, tokens):
        """ 1存在限量式 ノード作成 """
        return Exist1Expression(tokens[2], tokens[4], tokens.lineno, tokens.lexpos)

    def make_iota_expression(self, tokens):
        """ iota式 ノード作成 """
        return IotaExpression(tokens[2], tokens[4], tokens.lineno, tokens.lexpos)

    def make_set_enumeration(self, tokens):
        """ 集合列挙 ノード作成 """
        return SetEnumExpression(tokens[2], tokens.lineno, tokens.lexpos)

    def make_set_comprehension(self, tokens):
        """ 集合内包 ノード作成 """
        return SetCompExpression(tokens[2], tokens[4], tokens[5], tokens.lineno, tokens.lexpos)

    def make_set_range_expression(self, tokens):
        """ 集合範囲式 ノード作成 """
        return SetRangeExpression(tokens[2], tokens[6], tokens.lineno, tokens.lexpos)

    def make_column_enumeration(self, tokens):
        """ 列列挙 ノード作成 """
        return ColEnumExpression(tokens[2], tokens.lineno, tokens.lexpos)

    def make_column_comprehension(self, tokens):
        """ 列内包 ノード作成 """
        return ColCompExpression(tokens[2], tokens[4], tokens[5], tokens.lineno, tokens.lexpos)

    def make_subsequence(self, tokens):
        """ 部分列 ノード作成 """
        return SubseqExpression(tokens[1], tokens[3], tokens[7], tokens.lineno, tokens.lexpos)

    def make_map_enumeration(self, tokens):
        """ 写像列挙 ノード作成 """
        if len(tokens) == 5:
            return MapEnumExpression([tokens[2]]+tokens[3], tokens.lineno, tokens.lexpos)
        else:
            return MapEnumExpression([], tokens.lineno, tokens.lexpos)
            

    def make_copy(self, tokens):
        """ 写 ノード作成 """
        return MapExpression(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)

    def make_map_comprehension(self, tokens):
        """ 写像内包 ノード作成 """
        return MapCompExpression(tokens[2], tokens[4], tokens[5], tokens.lineno, tokens.lexpos)

    def make_tuple_constructor(self, tokens):
        """ 組構成子 ノード作成　"""
        return TupleConExpression(tokens[3], tokens[5], tokens.lineno, tokens.lexpos)

    def make_record_constructor(self, tokens):
        """ レコード構成子 ノード作成 """
        return RecordConExpression(tokens[2], tokens[4], tokens.lineno, tokens.lexpos)

    def make_record_modifier(self, tokens):
        """ レコード修正子 ノード作成 """
        if tokens[6] == None:
            return RecordModExpression(tokens[3], [tokens[5]], tokens.lineno, tokens.lexpos)
        else:
            return RecordModExpression(tokens[3], [tokens[5]] + tokens[6], tokens.lineno, tokens.lexpos)

    def make_record_update(self, tokens):
        """ レコード修正 ノード作成 """
        return RecordUpdateExpression(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)

    def make_application(self, tokens):
        """ 適用 ノード作成 """
        return AppExpression(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)
    
    def make_item_choice(self, tokens):
        """ 項目選択 ノード作成 """
        return ItemChoice(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)

    def make_tuple_choice(self, tokens):
        """ 組選択 ノード作成"""
        return TupleChoice(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)

    def make_functional_instantiation(self, tokens):
        """ 関数型インスタンス化 ノード作成 """
        return FuncInstExpression(tokens[1], [tokens[3]] + tokens[4], tokens.lineno, tokens.lexpos)

    def make_lambda_expression(self, tokens):
        """ ラムダ式 ノード作成 """
        return LambdaExpression(tokens[2], tokens[4], tokens.lineno, tokens.lexpos)

    def make_is_expression(self, tokens):
        """ is式 ノード作成 """
        if len(tokens) == 6:
            return IsExpression(tokens[2], tokens[4], tokens.lineno, tokens.lexpos)
        else:
            return IsExpression(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)   

    def make_type_judgment(self, tokens):
        """ 型判定 ノード作成 """
        return TypeJudgeExpression(tokens[3], tokens[5], tokens.lineno, tokens.lexpos)

    def make_undefined_expression(self, tokens):
        """ 未定義式 ノード作成 """
        return UnDefExpression(tokens[1], tokens.lineno, tokens.lexpos)

    def make_pre_condition_expression(self, tokens):
        """ 事前条件式 ノード作成 """
        return PreCondExpression([tokens[3]]+tokens[4], tokens.lineno, tokens.lexpos)
    
    def make_name(self, tokens):
        """ 名称 ノード作成 """
        return Name(tokens[1], tokens.lineno, tokens.lexpos)
    
    def make_oldname(self, tokens):
        """ 旧名称 ノード作成 """
        old_name = tokens[1] + tokens[2]
        return OldName(old_name, tokens.lineno, tokens.lexpos)

    def make_symbol_literal(self, tokens):
        """ シンボルリテラル ノード作成 """
        return SymbolLiteral(tokens[1], tokens.lineno, tokens.lexpos)

    # 型定義
    def make_type_definition_group(self, tokens):
        return TypeDefinitionGroup(tokens[2], tokens.lineno, tokens.lexpos)

    def make_optional_type_definition_group(self, tokens):
        tok_list = list(tokens)
        td_list = tok_list[:2]

        if len(tok_list) == 2:
            return None

        if tok_list[2] != None:
            # print(tok_list[2])
            td_list += tok_list[2]

        return [x for x in td_list if x]
            
    def make_type_definition(self, tokens):
        if len(tokens) == 5:
            return TypeDefinition(tokens[1], tokens[3], tokens[4], tokens.lineno, tokens.lexpos)
        elif len(tokens) == 6:
            return TypeDefinition(tokens[1], tokens[4], tokens[5], tokens.lineno, tokens.lexpos)
        else:
            return None

    def make_basic_type(self, tokens):
        if tokens[1] == 'bool':
            return BoolType(tokens[1], tokens.lineno, tokens.lexpos)
        elif tokens[1] == 'nat':
            return NatType(tokens[1], tokens.lineno, tokens.lexpos)
        elif tokens[1] == 'nat1':
            return Nat1Type(tokens[1], tokens.lineno, tokens.lexpos)
        elif tokens[1] == 'int':
            return IntType(tokens[1], tokens.lineno, tokens.lexpos)
        elif tokens[1] == 'rat':
            return RatType(tokens[1], tokens.lineno, tokens.lexpos)
        elif tokens[1] == 'real':
            return RealType(tokens[1], tokens.lineno, tokens.lexpos)
        elif tokens[1] == 'char':
            return CharType(tokens[1], tokens.lineno, tokens.lexpos)
        elif tokens[1] == 'token':
            return TokenType(tokens[1], tokens.lineno, tokens.lexpos)
        else:
            return None

    def make_is_basic_type(self, tokens):
        if tokens[1] == 'is_bool':
            return BoolType(tokens[1], tokens.lineno, tokens.lexpos)
        elif tokens[1] == 'is_nat':
            return NatType(tokens[1], tokens.lineno, tokens.lexpos)
        elif tokens[1] == 'is_nat1':
            return Nat1Type(tokens[1], tokens.lineno, tokens.lexpos)
        elif tokens[1] == 'is_rat':
            return RatType(tokens[1], tokens.lineno, tokens.lexpos)
        elif tokens[1] == 'is_real':
            return RealType(tokens[1], tokens.lineno, tokens.lexpos)
        elif tokens[1] == 'is_char':
            return CharType(tokens[1], tokens.lineno, tokens.lexpos)
        elif tokens[1] == 'is_token':
            return TokenType(tokens[1], tokens.lineno, tokens.lexpos)
        else:
            return None
    
    def make_quote_type(self, tokens):
        return QuoteType(tokens[2], tokens.lineno, tokens.lexpos)    

    def make_set_type(self, tokens):
        return SetType(tokens[3], tokens.lineno, tokens.lexpos)

    def make_seq_type(self, tokens):
        return SeqType(tokens[3], tokens.lineno, tokens.lexpos)

    def make_seq1_type(self, tokens):
        return Seq1Type(tokens[3], tokens.lineno, tokens.lexpos)

    def make_map_type(self, tokens):
        return MapType(tokens[2], tokens[4], tokens.lineno, tokens.lexpos)

    def make_inmap_type(self, tokens):
        return InMapType(tokens[2], tokens[4], tokens.lineno, tokens.lexpos)

    def make_tuple_type(self, tokens):
        
        tok_list = list(tokens)
        type_list = tok_list[:2]

        if type(tok_list[3]) == TupleType:
            type_list += tokens[3].type_list
        else:
            type_list += [tokens[3]]

        return TupleType([x for x in type_list if x], tokens.lineno, tokens.lexpos)

    def make_record_type(self, tokens):
        return RecordType(tokens[2], tokens[4], tokens.lineno, tokens.lexpos)

    def make_item(self, tokens):
        tok_len = len(tokens)
        if tok_len == 2:
            return Item(None, tokens[1], tokens.lineno, tokens.lexpos)
        elif tok_len == 4:
            return Item(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)
        elif tok_len == 5:
            return Item(tokens[1], tokens[4], tokens.lineno, tokens.lexpos)
        else:
            return Item()

    def make_merger_type(self, tokens):
        tok_list = list(tokens)
        type_list = tok_list[:2]

        if type(tok_list[3]) == MergerType:
            type_list += tokens[3].type_list
        else:
            type_list += [tokens[3]]

        return MergerType([x for x in type_list if x], tokens.lineno, tokens.lexpos)

    def make_selective_type(self, tokens):
        return SelectType(tokens[2], tokens.lineno, tokens.lexpos)

    def make_partial_function_type(self, tokens):
        return PartialFunctionType(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)

    def make_full_function_type(self, tokens):
        return FullFuntionType(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)

    def make_any_type(self, tokens):
        if len(tokens) == 2:
            return AnyType(tokens[1], tokens.lineno, tokens.lexpos)
        else:
            return AnyType(None, tokens.lineno, tokens.lexpos)

    def make_type_name(self, tokens):
        return TypeName(tokens[1], tokens.lineno, tokens.lexpos)
    
    def make_type_variable(self, tokens):
        return TypeVariableList(tokens[1], tokens.lineno, tokens.lexpos)

    # 状態定義
    def make_state_definition(self, tokens):
        return StateDefinition(tokens[2], tokens[3], tokens[5], tokens[6], tokens.lineno, tokens.lexpos)

    def make_inv_condition(self, tokens):
        return InvCondition(tokens[2], tokens.lineno, tokens.lexpos)

    def make_initialization(self, tokens):
        return Initialization(tokens[2], tokens.lineno, tokens.lexpos)

    def make_inv_cond_init_function(self, tokens):
        return InvCondInitFunc(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)

    # 値定義群
    def make_value_definition(self, tokens):
        if len(tokens) == 6:
            return ValueDefinition(tokens[1], tokens[3], tokens[5], tokens.lineno, tokens.lexpos)
        elif len(tokens) == 5:
            return ValueDefinition(tokens[1], None, tokens[3], tokens.lineno, tokens.lexpos)
        else:
            return ValueDefinition(tokens[1], None, tokens[3], tokens.lineno, tokens.lexpos)

    # パターン
    def make_pattern_ident(self, tokens):
        return PatternIdent(tokens[1], tokens.lineno, tokens.lexpos)

    def make_match_value(self, tokens):
        if len(tokens) == 4:
            return MatchValue(tokens[2], tokens.lineno, tokens.lexpos)
        else:
            return MatchValue(tokens[1])
    
    def make_set_enumration_pattern(self, tokens):
        if len(tokens) == 4:
            return SetEnumPattern(tokens[2], tokens.lineno, tokens.lexpos)
        else:
            return SetEnumPattern(None, tokens.lineno, tokens.lexpos)
    
    def make_set_union_pattern(self, tokens):
        return SetUnionPattern(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)

    def make_column_enumeration_pattern(self, tokens):
        if len(tokens) == 4:
            return ColEnumPattern(tokens[2], tokens.lineno, tokens.lexpos)
        else:
            return ColEnumPattern(None, tokens.lineno, tokens.lexpos)
    
    def make_column_link_pattern(self, tokens):
        return ColLinkPattern(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)

    def make_map_enumeration_pattern(self, tokens):
        if len(tokens) == 4:
            return MapEnumPattern(tokens[2], tokens.lineno, tokens.lexpos)
        else:
            return MapEnumPattern(None, tokens.lineno, tokens.lexpos)

    def make_map_pattern(self, tokens):
        return MapPattern(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)
    
    def make_map_munion_pattern(self, tokens):
        return MapMunionPattern(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)

    def make_tuple_pattern(self, tokens):
        ptn_list = [tokens[3]] + tokens[5].patterns
        return TuplePattern(ptn_list, tokens.lineno, tokens.lexpos)

    def make_record_pattern(self, tokens):
        if len(tokens) == 6:
            return RecordPattern(tokens[2], tokens[4], tokens.lineno, tokens.lexpos)
        else:
            return RecordPattern(tokens[2], None, tokens.lineno, tokens.lexpos)

    def make_pattern_list(self, tokens):
        if tokens[2] != None:
            return PatternList([tokens[1]] + tokens[2], tokens.lineno, tokens.lexpos)
        else:
            return PatternList([tokens[1]], tokens.lineno, tokens.lexpos)
    
    # 束縛
    def make_binding(self, tokens):
        return Binding(tokens[1], tokens.lineno, tokens.lexpos)

    def make_set_binding(self, tokens):
        return SetBinding(tokens[1], tokens[4], tokens.lineno, tokens.lexpos)

    def make_type_binding(self, tokens):
        return TypeBinding(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)

    def make_multi_set_binding(self, tokens):
        return MultiSetBinding(tokens[1], tokens[4], tokens.lineno, tokens.lexpos)

    def make_multi_type_binding(self, tokens):
        return MultiTypeBinding(tokens[1], tokens[3], tokens.lineno, tokens.lexpos)

    def make_type_variable_ident(self, tokens):
        return TypeVariableIdent(tokens[1] + tokens[2], tokens.lineno, tokens.lexpos)
        



if __name__ == '__main__':
    pass