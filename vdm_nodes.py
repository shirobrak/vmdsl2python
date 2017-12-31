# -*- coding: utf-8 -*-

class VdmslNode(object):
    SPACER = " "
    """ VDM-SLのASTノード基底クラス """
    _fields = ()
    _attributes = ('lineno', 'lexpos')

    def __repr__(self):
        return "{}({})".format(
            self.__class__.__name__,
            ', '.join(["%s=%s" % (field, getattr(self, field))
                    for field in self._fields])
    )

    def _p(self, v, indent):
        print("{}{}".format(self.SPACER * indent, v))

    def dumps(self, indent=0):
        self._p(self.__class__.__name__ + '(', indent)
        for field in self._fields:
            self._p(field + '=', indent + 1)
            value = getattr(self, field)
            if type(value) == list:
                for value2 in value:
                    if isinstance(value2, ASTNode):
                        value2.dumps(indent + 2)
                    else:
                        self._p(value2, indent + 2)
            else:
                if value:
                    if isinstance(value, ASTNode):
                        value.dumps(indent + 2)
                    else:
                        self._p(value, indent + 2)
        self._p(')', indent)


# データ型定義

class TypeDefinitionGroup(VdmslNode):
    """ 型定義群 """
    _fields = ('type_definitions',)

    def __init__(self, type_definitions, lineno, lexpos):
        self.type_definitions = type_definitions
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class TypeDefinition(VdmslNode):
    """ 型定義 """
    _fields = ('id', 'type', 'inv_cond',)

    def __init__(self, id, type, inv_cond, lineno, lexpos):
        self.id = id
        self.type = type
        self.inv_cond = inv_cond
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
        

# 基本データ型
class BasicDataType(VdmslNode):
    """ 基本データ型基底クラス """
    _fields = ('value',)

    def __init__(self, value, lineno, lexpos):
        self.value = value
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class BoolType(BasicDataType):
    """ ブール型 """
    pass

class NatType(BasicDataType):
    """ Nat型(自然数) """
    pass

class Nat1Type(BasicDataType):
    """ Nat1型(正の自然数) """
    pass

class IntType(BasicDataType):
    """ Int型(整数) """
    pass

class RatType(BasicDataType):
    """ Rat型(有理数) """
    pass

class RealType(BasicDataType):
    """ Real型(実数) """
    pass

class CharType(BasicDataType):
    """ 文字型 """
    pass

class QuoteType(BasicDataType):
    """ 引用型 """
    pass

class TokenType(BasicDataType):
    """ トークン型 """
    pass

# 合成型
class SyntheticDataType(VdmslNode):
    """ 合成型基底クラス """
    _fields = ('type_name',)

    def __init__(self, value, lineno, lexpos):
        self.type_name = type_name
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class SetType(SyntheticDataType):
    """ 集合型 """
    pass

class SeqType(SyntheticDataType):
    """ 空列を含む列型 """
    pass

class Seq1Type(SyntheticDataType):
    """ 空列を含まない列型 """
    pass

class MapType(VdmslNode):
    """ 一般写像型 """
    _fields = ('type1', 'type2',)

    def __init__(self, type1, type2, lineno, lexpos):
        self.type1 = type1
        self.type2 = type2
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class InMapType(SyntheticDataType):
    """ 1対1写像型 """
    _fields = ('type1', 'type2',)

    def __init__(self, type1, type2, lineno, lexpos):
        self.type1 = type1
        self.type2 = type2
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class TupleType(VdmslNode):
    """ 組型 """
    _fields = ('type_list',)

    def __init__(self, type_list, lineno, lexpos):
        self.type_list = type_list
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class RecordType(VdmslNode):
    """ レコード型 """
    _fields = ('ident', 'item_list',)

    def __init__(self, ident, item_list, lineno, lexpos):
        self.ident = ident
        self.item_list = item_list
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class Item(VdmslNode):
    """ 項目 """
    _fields = ('ident', 'type',)

    def __init__(self, ident, type, lineno, lexpos):
        self.ident = ident
        self.type = type
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class MergerType(VdmslNode):
    """ 合併型 """
    _fields = ('type_list',)

    def __init__(self, type_list, lineno, lexpos):
        self.type_list = type_list
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class SelectType(VdmslNode):
    """ 選択型 """
    _fields = ('value',)

    def __init__(self, value, lineno, lexpos):
        self.value = value
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)


class FuncionType(VdmslNode):
    """ 関数型基底クラス """
    _fields = ('any_type', 'type',)

    def __init__(self, any_type, type, lineno, lexpos):
        self.any_type = any_type
        self.type = type
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class PartialFunctionType(FuncionType):
    """ 部分関数型 """
    pass

class FullFuntionType(FuncionType):
    """ 全関数型 """
    pass

class AnyType(VdmslNode):
    """ 任意の型 """
    _fields = ('type',)

    def __init__(self, type, lineno, lexpos):
        self.type = type
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)


class NameBase(VdmslNode):
    """ 名称基底クラス """
    _fields = ('id',)

    def __init__(self, id, lineno, lexpos):
        self.id = id
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class Name(NameBase):
    """ 名称 """
    pass

class OldName(NameBase):
    """ 旧名称 """
    pass

class SymbolLiteral(NameBase):
    """ 記号リテラル """
    pass

class TypeName(NameBase):
    """ 型名称 """
    pass

class TypeVariableIdent(NameBase):
    """ 型変数識別子 """
    pass


# 式
class Expression(VdmslNode):
    """ 式 """
    _fields = ('value',)

    def __init__(self, value, lineno, lexpos):
        self.value = value
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

# 括弧式
class BracketExpression(VdmslNode):
    """ 括弧式 """
    _fields = ('body',)

    def __init__(self, body, lineno, lexpos):
        self.body = body
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

# let式
class LetExpression(VdmslNode):
    """ let式 """
    _fields = ('local_definition', 'body',)

    def __init__(self, local_definition, body, lineno, lexpos):
        self.local_definition = local_definition
        self.body = body
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class LetBeExpression(VdmslNode):
    """ letbe式 """
    _fields = ('binding', 'option_expr', 'body',)

    def __init__(self, binding, option_expr, body, lineno, lexpos):
        self.binding = binding
        self.option_expr = option_expr
        self.body = body
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
 

# def式
class DefExpression(VdmslNode):
    """ def式 """
    _fields = ('pattern_binding', 'body',)

    def __init__(self, pattern_binding, body, lineno, lexpos):
        self.pattern_binding = pattern_binding
        self.body = body
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class DefPtnBinding(VdmslNode):
    """ def式 パターン束縛&式の組 """
    _fields = ('ptn_binding', 'expr',)

    def __init__(self, ptn_binding, expr):
        self.ptn_binding = ptn_binding
        self.expr = expr

# 条件式
class IfExpression(VdmslNode):
    """ if式 """
    _fields = ('cond', 'body', 'elseif', 'else_',)

    def __init__(self, cond, body, elseif, else_, lineno, lexpos):
        self.cond = cond
        self.body = body
        self.elseif = elseif
        self.else_ = else_
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class ElseIfExpression(VdmslNode):
    """ elseif式 """
    _fields = ('cond', 'then',)

    def __init__(self, cond, then, lineno, lexpos):
        self.cond = cond
        self.then = then
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class CasesExpression(VdmslNode):
    """ cases式 """
    _fields = ('cond', 'case_group', 'other',)

    def __init__(self, cond, case_group, other, lineno, lexpos):
        self.cond = cond
        self.case_group = case_group
        self.other = other
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class CasesExprOption(VdmslNode):
    """ cases式選択肢 """
    _fields = ('pattern_list', 'expr',)

    def __init__(self, pattern_list, expr, lineno, lexpos):
        self.pattern_list = pattern_list
        self.expr = expr
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)


# 単項式
class UnaryBaseExpression(VdmslNode):
    """ 単項式基底クラス """
    _fields = ('right',)

    def __init__(self, right, lineno, lexpos):
        self.right = right
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class Plus(UnaryBaseExpression):
    pass

class Minus(UnaryBaseExpression):
    pass

class Abs(UnaryBaseExpression):
    pass

class Floor(UnaryBaseExpression):
    pass

class Not(UnaryBaseExpression):
    pass

class Card(UnaryBaseExpression):
    pass

class Power(UnaryBaseExpression):
    pass

class Dunion(UnaryBaseExpression):
    pass

class Dinter(UnaryBaseExpression):
    pass

class Hd(UnaryBaseExpression):
    pass

class Tl(UnaryBaseExpression):
    pass

class Len(UnaryBaseExpression):
    pass

class Elems(UnaryBaseExpression):
    pass

class Inds(UnaryBaseExpression):
    pass

class Conc(UnaryBaseExpression):
    pass

class Dom(UnaryBaseExpression):
    pass

class Rng(UnaryBaseExpression):
    pass

class Merge(UnaryBaseExpression):
    pass

class Inverse(UnaryBaseExpression):
    pass

# 二項式
class BinBaseExpression(VdmslNode):
    """ 二項式基底クラス """
    _fields = ('left', 'right',)

    def __init__(self, left, right, lineno, lexpos):
        self.left = left
        self.right = right
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class Add(BinBaseExpression):
    """ 加算 """
    pass

class Sub(BinBaseExpression):
    """ 減算 """
    pass

class Mul(BinBaseExpression):
    """ 乗算 """
    pass

class Div(BinBaseExpression):
    """ 除算 """
    pass

class IntDiv(BinBaseExpression):
    """ 整数除算 """
    pass

class Rem(BinBaseExpression):
    """ 剰余算 """
    pass

class Mod(BinBaseExpression):
    """ 法算 """
    pass

class Lt(BinBaseExpression):
    """ より小さい """
    pass

class LtEq(BinBaseExpression):
    """ より小さいか等しい """
    pass

class Gt(BinBaseExpression):
    """ より大きい """
    pass

class GtEq(BinBaseExpression):
    """ より大きいか等しい """
    pass

class Equal(BinBaseExpression):
    """ 相等 """
    pass

class NotEq(BinBaseExpression):
    """ 不等 """
    pass

class Or(BinBaseExpression):
    """ 論理和 """
    pass

class And(BinBaseExpression):
    """ 論理積 """
    pass

class Imp(BinBaseExpression):
    """ 含意 """
    pass

class Equivalence(BinBaseExpression):
    """ 同値 """
    pass

class InSet(BinBaseExpression):
    """ 帰属 """
    pass

class NotInSet(BinBaseExpression):
    """ 非帰属 """
    pass

class Subset(BinBaseExpression):
    """ 包含 """
    pass

class PSubset(BinBaseExpression):
    """ 真包含 """
    pass

class Union(BinBaseExpression):
    """ 集合合併 """
    pass

class SetDiff(BinBaseExpression):
    """ 集合差 """
    pass

class Inter(BinBaseExpression):
    """ 集合共通部分 """
    pass

class ColLink(BinBaseExpression):
    """ 列連結 """
    pass

class MapColUpdate(BinBaseExpression):
    """ 写像修正または列修正 """
    pass

class Munion(BinBaseExpression):
    """ 写像併合 """
    pass

class MapDomRes(BinBaseExpression):
    """ 写像定義域限定 """
    pass

class MapDomRed(BinBaseExpression):
    """ 写像定義域削減 """
    pass

class MapRangeRes(BinBaseExpression):
    """ 写像値域限定 """
    pass

class MapRangeRed(BinBaseExpression):
    """ 写像値域削減 """
    pass

class Comp(BinBaseExpression):
    """ 合成 """
    pass

class Rep(BinBaseExpression):
    """ 反復 """
    pass

# 限量式
class ForallExpression(VdmslNode):
    """ 全称限量式 """
    _fields = ('bind_list', 'body',)

    def __init__(self, bind_list, body, lineno, lexpos):
        self.bind_list = bind_list
        self.body = body
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class ExistsExpression(VdmslNode):
    """ 存在限量式 """
    _fields = ('bind_list', 'body',)

    def __init__(self, bind_list, body, lineno, lexpos):
        self.bind_list = bind_list
        self.body = body
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class Exist1Expression(VdmslNode):
    """ 1存在限量式 """
    _fields = ('bind', 'body',)

    def __init__(self, bind, body, lineno, lexpos):
        self.bind = bind
        self.body = body
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

# iota式
class IotaExpression(VdmslNode):
    """ iota式 """
    _fields = ('bind', 'body',)

    def __init__(self, bind, body, lineno, lexpos):
        self.bind = bind
        self.body = body
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

# 集合式
class SetEnumExpression(VdmslNode):
    """ 集合列挙 """
    _fields = ('expr_list',)

    def __init__(self, expr_list, lineno, lexpos):
        self.expr_list = expr_list
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class SetCompExpression(VdmslNode):
    """ 集合内包 """
    _fields = ('body', 'bind_list', 'predicate',)

    def __init__(self, body, bind_list, predicate, lineno, lexpos):
        self.body = body
        self.bind_list = bind_list
        self.predicate = predicate
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class SetRangeExpression(VdmslNode):
    """ 集合範囲式 """
    _fields = ('start','end',)

    def __init__(self, start, end, lineno, lexpos):
        self.start = start
        self.end = end
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

# 列式
class ColEnumExpression(VdmslNode):
    """ 列列挙 """
    _fields = ('expr_list',)

    def __init__(self, expr_list, lineno, lexpos):
        self.expr_list = expr_list
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class ColCompExpression(VdmslNode):
    """ 列内包 """
    _fields = ('body', 'set_bind', 'predicate',)

    def __init__(self, body, set_bind, predicate, lineno, lexpos):
        self.body = body
        self.set_bind = set_bind
        self.predicate = predicate
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class SubseqExpression(VdmslNode):
    """ 部分列 """
    _fields = ('column', 'start', 'end',)

    def __init__(self, column, start, end, lineno, lexpos):
        self.column = column
        self.start = start
        self.end = end
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

# 写像式
class MapEnumExpression(VdmslNode):
    """ 写像列挙 """
    _fields = ('map_list',)

    def __init__(self, map_list, lineno, lexpos):
        self.map_list = map_list
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class MapExpression(VdmslNode):
    """ 写像 """
    _fields = ('dom', 'range',)

    def __init__(self, dom, range, lineno, lexpos):
        self.dom = dom
        self.range = range
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class MapCompExpression(VdmslNode):
    """ 写像内包 """
    _fields = ('map', 'bind_list', 'predicate',)

    def __init__(self, map, bind_list, predicate, lineno, lexpos):
        self.map = map
        self.bind_list = bind_list
        self.predicate = predicate
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
        
# 組構成子式
class TupleConExpression(VdmslNode):
    """ 組構成子 """
    _fields = ('body', 'expr_list',)

    def __init__(self, body, expr_list, lineno, lexpos):
        self.body = body
        self.expr_list = expr_list
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

# レコード式
class RecordConExpression(VdmslNode):
    """ レコード構成子 """
    _fields = ('record_name', 'expr_list',)

    def __init__(self, record_name, expr_list, lineno, lexpos):
        self.record_name = record_name
        self.expr_list = expr_list
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class RecordModExpression(VdmslNode):
    """ レコード修正子 """
    _fields = ('body', 'record_update_list',)

    def __init__(self, body, record_update_list, lineno, lexpos):
        self.body = body
        self.record_update_list = record_update_list
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class RecordUpdateExpression(VdmslNode):
    """ レコード修正 """
    _fields = ('left','right',)

    def __init__(self, left, right, lineno, lexpos):
        self.left = left
        self.right = right
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

# 適用式
class AppExpression(VdmslNode):
    """ 適用式 """
    _fields = ('body', 'expr_list',)

    def __init__(self, body, expr_list, lineno, lexpos):
        self.body = body
        self.expr_list = expr_list
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class ItemChoice(VdmslNode):
    """ 項目選択式 """
    _fields = ('expr', 'ident',)

    def __init__(self, expr, ident, lineno, lexpos):
        self.expr = expr
        self.ident = ident
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class TupleChoice(VdmslNode):
    """ 組選択式 """
    _fields = ('expr', 'number',)

    def __init__(self, expr, number, lineno, lexpos):
        self.expr = expr
        self.number = number
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class FuncInstExpression(VdmslNode):
    """ 関数型インスタンス化 """
    _fields = ('name', 'type_list',)

    def __init__(self, name, type_list, lineno, lexpos):
        self.name = name
        self.type_list = type_list
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

# ラムダ式
class LambdaExpression(VdmslNode):
    """ ラムダ式 """
    _fields = ('type_bind_list', 'body',)

    def __init__(self, type_bind_list, body, lineno, lexpos):
        self.type_bind_list = type_bind_list
        self.body = body
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

# is式
class GeneralIsExpression(VdmslNode):
    """ 一般is式 """
    _fields = ('body',)

    def __init__(self, body, lineno, lexpos):
        self.body = body
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class IsExpression(VdmslNode):
    """ is式 """
    _fields = ('type_name', 'body',)

    def __init__(self, type_name, body, lineno, lexpos):
        self.type_name = type_name
        self.body = body
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class TypeJudgeExpression(VdmslNode):
    """ 型判定 """
    _fields = ('body', 'type_name',)

    def __init__(self, body, type_name, lineno, lexpos):
        self.body = body
        self.type_name = type_name
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

# 未定義式
class UnDefExpression(VdmslNode):
    """ 未定義式 """
    _fields = ('body',)

    def __init__(self, body, lineno, lexpos):
        self.body = body
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

# 事前条件式
class PreCondExpression(VdmslNode):
    """ 事前条件式 """
    _fields = ('expr_list',)

    def __init__(self, expr_list, lineno, lexpos):
        self.expr_list = expr_list
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

# パターン 
class Pattern(VdmslNode):
    """ パターン """
    _fields = ('patterns',)

    def __init__(self, patterns, lineno, lexpos):
        self.patterns = patterns
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class PatternIdent(VdmslNode):
    """ パターン識別子 """
    _fields = ('ptn_id',)

    def __init__(self, ptn_id, lineno, lexpos):
        self.ptn_id = ptn_id
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class MatchValue(VdmslNode):
    """ 一致値 """
    _fields = ('match_value',)

    def __init__(self, match_value, lineno, lexpos):
        self.match_value = match_value
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class SetEnumPattern(VdmslNode):
    """ 集合列挙パターン """
    _fields = ('ptn_list',)

    def __init__(self, ptn_list, lineno, lexpos):
        self.ptn_list = ptn_list
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class SetUnionPattern(VdmslNode):
    """ 集合合併パターン """
    _fields = ('left', 'right',)

    def __init__(self, left, right, lineno, lexpos):
        self.left = left
        self.right = right
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class ColEnumPattern(VdmslNode):
    """ 列列挙パターン """
    _fields = ('ptn_list',)

    def __init__(self, ptn_list, lineno, lexpos):
        self.ptn_list = ptn_list
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class ColLinkPattern(VdmslNode):
    """ 列連結パターン """
    _fields = ('left', 'right',)

    def __init__(self, left, right, lineno, lexpos):
        self.left = left
        self.right = right
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class MapEnumPattern(VdmslNode):
    """ 写像列挙パターン """
    _fields = ('map_pattern_list',)

    def __init__(self, map_pattern_list, lineno, lexpos):
        self.map_pattern_list = map_pattern_list
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class MapPattern(VdmslNode):
    """ 写パターン """
    _fields = ('left', 'right',)

    def __init__(self, left, right, lineno, lexpos):
        self.left = left
        self.right = right
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class MapMunionPattern(VdmslNode):
    """ 写像併合パターン """
    _fields = ('left', 'right',)

    def __init__(self, left, right, lineno, lexpos):
        self.left = left
        self.right = right
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class TuplePattern(VdmslNode):
    """ 組パターン """
    _fields = ('ptn_list',)

    def __init__(self, pattern_list, lineno, lexpos):
        self.ptn_list = ptn_list
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class RecordPattern(VdmslNode):
    """ レコードパターン """
    _fields = ('name', 'pattern_list',)

    def __init__(self, name, pattern_list, lineno, lexpos):
        self.name = name
        self.pattern_list = pattern_list
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

# 束縛
class Binding(VdmslNode):
    """ 束縛 """
    _fields = ('bindings',)

    def __init__(self, bindings, lineno, lexpos):
        self.bindings = bindings
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class SetBinding(VdmslNode):
    """ 集合束縛 """
    _fields = ('pattern', 'expr',)

    def __init__(self, pattern, expr, lineno, lexpos):
        self.pattern = pattern
        self.expr = expr
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class TypeBinding(VdmslNode):
    """ 型束縛 """
    _fields = ('pattern', 'type',)

    def __init__(self, pattern, type, lineno, lexpos):
        self.pattern = pattern
        self.type = type
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class BindingList(VdmslNode):
    """ 束縛リスト """
    _fields = ('multi_bindings',)

    def __init__(self, multi_bindings, lineno, lexpos):
        self.multi_bindings = multi_bindings
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class MultiBinding(VdmslNode):
    """ 多重束縛 """
    _fields = ('bindings',)

    def __init__(self, bindings, lineno, lexpos):
        self.bindings = bindings
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class MultiSetBinding(VdmslNode):
    """ 多重集合束縛 """
    _fields = ('pattern_list', 'expr',)

    def __init__(self, pattern_list, expr, lineno, lexpos):
        self.pattern_list = pattern_list
        self.expr = expr
        self.__setattr__('lineno', lineno) 
        self.__setattr__('lexpos', lexpos)

class MultiTypeBinding(VdmslNode):
    """ 多重型束縛 """
    _fields = ('pattern_list', 'type',)

    def __init__(self, pattern_list, type, lineno, lexpos):
        self.pattern_list = pattern_list
        self.type = type
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

# 値定義
class ValueDefinitionGroup(VdmslNode):
    """ 値定義群 """
    _fields = ('value_definitions',)

    def __init__(self, value_definitions, lineno, lexpos):
        self.value_definitions = value_definitions
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class ValueDefinition(VdmslNode):
    """ 値定義 """
    _fields = ('pattern', 'type', 'expr',)

    def __init__(self, pattern, type, expr, lineno, lexpos):
        self.pattern = pattern
        self.type = type
        self.expr = expr
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

# 状態定義
class StateDefinition(VdmslNode):
    """ 状態定義 """
    _fields = ('ident', 'item_list', 'inv_cond', 'init',)

    def __init__(self, ident, item_list, inv_cond, init, lineno, lexpos):
        self.ident = ident
        self.item_list = item_list
        self.inv_cond = inv_cond
        self.init = init
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class InvCondition(VdmslNode):
    """ 不変条件 """
    _fields = ('inv_condition_init_function',)

    def __init__(self, inv_condition_init_function, lineno, lexpos):
        self.inv_condition_init_function = inv_condition_init_function
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class Initialization(VdmslNode):
    """ 初期化 """
    _fields = ('inv_condition_init_function',)

    def __init__(self, inv_condition_init_function, lineno, lexpos):
        self.inv_condition_init_function = inv_condition_init_function
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class InvCondInitFunc(VdmslNode):
    """ 不変条件初期関数 """
    _fields = ('pattern', 'expr',)

    def __init__(self, pattern, expr, lineno, lexpos):
        self.pattern = pattern
        self.expr = expr
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

# 操作定義
class OpeDefinitionGroup(VdmslNode):
    """ 操作定義群 """
    _fields = ('operation_definitions',)

    def __init__(self, operation_definitions, lineno, lexpos):
        self.operation_definitions = operation_definitions
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class OpeDefinition(VdmslNode):
    """ 操作定義 """
    _fields = ('operation_definition',)

    def __init__(self, operation_definition, lineno, lexpos):
        self.operation_definition = operation_definition
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class ExpOpeDefinition(VdmslNode):
    """ 陽操作定義 """
    _fields = ('ope_ident', 'ope_type', 'param_ident', 
               'param_group', 'ope_body', 'pre_expr', 'post_expr',)
    
    def __init__(self, ope_ident, ope_type, param_ident, 
                 param_group, ope_body, pre_expr, post_expr, lineno, lexpos):
        self.ope_ident = ope_ident
        self.ope_type = ope_type
        self.param_ident = param_ident
        self.param_group = param_group
        self.ope_body = ope_body
        self.pre_expr = pre_expr
        self.post_expr = post_expr
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class ImpOpeDefinition(VdmslNode):
    """ 陰操作定義 """
    _fields = ('param_ident', 'param_type', 'ident_type_pair_list', 'imp_body',)

    def __init__(self, param_ident, param_type, 
                 ident_type_pair_list, imp_body, lineno, lexpos):
        self.param_ident = param_ident
        self.param_type = param_type
        self.ident_type_pair_list = ident_type_pair_list
        self.imp_body = imp_body
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class ImpOpeBody(VdmslNode):
    """ 陰操作本体 """
    _fields = ('ext_sec', 'pre_expr', 'post_expr', 'except',)

    def __init__(self, ext_sec, pre_expr, post_expr, exception, lineno, lexpos):
        self.ext_sec = ext_sec
        self.pre_expr = pre_expr
        self.post_expr = post_expr
        self.exception = exception
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class ExpandExpOpeDefinition(VdmslNode):
    """ 拡張陽操作定義 """
    _fields = ('ident', 'param_type', 'ident_type_pair_list', 'ope_body',
               'ext_sec', 'pre_expr', 'post_expr', 'exception',)
    
    def __init__(self, ident, param_type, ident_type_pair_list, ope_body,
                 ext_sec, pre_expr, post_expr, exception, lineno, lexpos):
        self.ident = ident
        self.param_type = param_type
        self.ident_type_pair_list = ident_type_pair_list
        self.ope_body = ope_body
        self.ext_sec = ext_sec
        self.pre_expr = pre_expr
        self.post_expr = post_expr
        self.exception = exception
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class OperationType(VdmslNode):
    """ 操作型 """
    _fields = ('left', 'right',)

    def __init__(self, left, right, lineno, lexpos):
        self.left = left
        self.right = right
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)


class ParamGroup(VdmslNode):
    """ パラメータ群 """
    _fields = ('pattern_list',)

    def __init__(self, pattern_list, lineno, lexpos):
        self.pattern_list = pattern_list
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)


class PatternList(VdmslNode):
    """ パターンリスト """
    _fields = ('patterns',)

    def __init__(self, patterns, lineno, lexpos):
        self.patterns = patterns
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class OperationBody(VdmslNode):
    """ 操作本体 """
    _fields = ('statement',)

    def __init__(self, statement, lineno, lexpos):
        self.statement = statement
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class ExtSection(VdmslNode):
    """ 外部節 """
    _fields = ('var_infos',)

    def __init__(self, var_infos, lineno, lexpos):
        self.var_infos = var_infos
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class VarInfo(VdmslNode):
    """ var 情報 """
    _fields = ('mode', 'name_list', 'type',)

    def __init__(self, mode, name_list, type, lineno, lexpos):
        self.mode = mode
        self.name_list = name_list
        self.type = type
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class NameList(VdmslNode):
    """ 名称リスト """
    _fields = ('idents',)

    def __init__(self, idents, lineno, lexpos):
        self.idents = idents
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class Exception(VdmslNode):
    """ 例外 """
    _fields = ('err_list',)

    def __init__(self, err_list, lineno, lexpos):
        self.err_list = err_list
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class ErrorList(VdmslNode):
    """ エラーリスト """
    _fields = ('errors',)

    def __init__(self, errors, lineno, lexpos):
        self.errors = errors
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class Error(VdmslNode):
    """ エラー """
    _fields = ('ident', 'left', 'right',)

    def __init__(self, ident, left, right, lineno, lexpos):
        self.ident = ident
        self.left = left
        self.right = right
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

# 関数定義
class FuncDefinitionGroup(VdmslNode):
    """ 関数定義群 """
    _fields = ('function_definitions',)

    def __init__(self, function_definitions, lineno, lexpos):
        self.function_definitions = function_definitions
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class FuncDefinition(VdmslNode):
    """ 関数定義 """
    _fields = ('function_definition',)

    def __init__(self, function_definition, lineno, lexpos):
        self.function_definition = function_definition
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class ExpFuncDefinition(VdmslNode):
    """ 陽関数定義 """
    _fields = ('ident1', 'type_variable_list', 'func_type', 'ident2', 'param_list', 
               'func_body', 'pre_expr', 'post_expr', 'name',)
    
    def __init__(self, ident1, type_variable_list, func_type, ident2, param_list, 
               func_body, pre_expr, post_expr, name, lineno, lexpos):
        self.ident1 = ident1
        self.type_variable_list = type_variable_list
        self.func_type = func_type
        self.ident2 = ident2
        self.param_list = param_list
        self.func_body = func_body
        self.pre_expr = pre_expr
        self.post_expr = post_expr
        self.name = name
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class ImpFuncDefinition(VdmslNode):
    """ 陰関数定義 """
    _fields = ('ident', 'type_variable_list', 'param_type', 
               'ident_type_pair_list', 'pre_expr', 'post_expr',)
    
    def __init__(self, ident, type_variable_list, param_type, 
                 ident_type_pair_list, pre_expr, post_expr, lineno, lexpos):
        self.ident = ident
        self.type_variable_list = type_variable_list
        self.param_type = param_type
        self.ident_type_pair_list = ident_type_pair_list
        self.pre_expr = pre_expr
        self.post_expr = post_expr
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class ExpandExpFuncDefinition(VdmslNode):
    """ 拡張陽関数定義 """
    _fields = ('ident', 'type_variable_list', 'param_type', 'ident_type_pair_list',
               'func_body', 'pre_expr', 'post_expr',)

    def __init__(self, ident, type_variable_list, param_type, ident_type_pair_list,
               func_body, pre_expr, post_expr, lineno, lexpos):
        self.ident = ident
        self.type_variable_list = type_variable_list
        self.param_type = param_type
        self.ident_type_pair_list = ident_type_pair_list
        self.func_body = func_body
        self.pre_expr = pre_expr
        self.post_expr = post_expr
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class TypeVariableList(VdmslNode):
    """ 型変数リスト """
    _fields = ('type_variable_idents',)

    def __init__(self, type_variable_idents, lineno, lexpos):
        self.type_variable_idents = type_variable_idents
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class IdentTypePairList(VdmslNode):
    """ 識別子型ペアリスト """
    _fields = ('ident_type_pairs',)

    def __init__(self, ident_type_pairs, lineno, lexpos):
        self.ident_type_pairs = ident_type_pairs
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class IdentTypePair(VdmslNode):
    """ 識別子ペア """
    _fields = ('ident', 'type',)

    def __init__(self, ident, type, lineno, lexpos):
        self.ident = ident
        self.type = type
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class ParamType(VdmslNode):
    """ パラメーター型 """
    _fields = ('pattern_type_pair_list',)

    def __init__(self, pattern_type_pair_list, lineno, lexpos):
        self.pattern_type_pair_list = pattern_type_pair_list
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class PatternTypePairList(VdmslNode):
    """ パターン型ペアリスト """
    _fields = ('pattern_type_pairs',)

    def __init__(self, pattern_type_pairs, lineno, lexpos):
        self.pattern_type_pairs = pattern_type_pairs
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class PatternTypePair(VdmslNode):
    """ パターン型ペア """
    _fields = ('pattern_list', 'type',)

    def __init__(self, pattern_list, type, lineno, lexpos):
        self.pattern_list = pattern_list
        self.type = type
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)



class FunctionBody(VdmslNode):
    """ 関数本体 """
    _fields = ('expression',)

    def __init__(self, expression, lineno, lexpos):
        self.expression = expression
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

# 文
class Statements(VdmslNode):
    """ 文 """
    _fields = ('statement',)

    def __init__(self, statement, lineno, lexpos):
        self.statement = statement
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

# let 文
class LetStatement(VdmslNode):
    """ let文 """
    _fields = ('local_definitions', 'body',)

    def __init__(self, local_definitions, body, lineno, lexpos):
        self.local_definitions = local_definitions
        self.body = body
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class LetBeStatement(VdmslNode):
    """ let be 文 """
    _fields = ('binding', 'option_expr', 'body',)

    def __init__(self, binding, option_expr, body, lineno, lexpos):
        self.binding = binding
        self.option_expr = option_expr
        self.body = body
        self.__setattr__('lineno', lineno) 
        self.__setattr__('lexpos', lexpos)

class LocalDefinitions(VdmslNode):
    """ ローカル定義 """
    _fields = ('definition',)

    def __init__(self, definition, lineno, lexpos):
        self.definition = definition
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

# def 文

class DefStatement(VdmslNode):
    """ def文 """
    _fields = ('equal_definitions', 'body',)

    def __init__(self, equal_definitions, body, lineno, lexpos):
        self.equal_definitions = equal_definitions
        self.body = body
        self.__setattr__('lineno', lineno) 
        self.__setattr__('lexpos', lexpos)

class EqualDefinition(VdmslNode):
    """ 相等定義 """
    _fields = ('pattern_binding', 'expr',)

    def __init__(self, pattern_binding, expr, lineno, lexpos):
        self.pattern_binding = pattern_binding
        self.expr = expr
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

# ブロック文
class BlockStatement(VdmslNode):
    """ ブロック文 """
    _fields =('dcl_stmt', 'statements',)

    def __init__(self, dcl_stmt, statement, lineno, lexpos):
        self.dcl_stmt = dcl_stmt
        self.statement = statement
        self.__setattr__('lineno', lineno) 
        self.__setattr__('lexpos', lexpos)

class DclStatement(VdmslNode):
    """ dcl文 """
    _fields = ('assign_definitions',)

    def __init__(self, assign_definitions, lineno, lexpos):
        self.assign_definitions = assign_definitions
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class AssignDefinition(VdmslNode):
    """ 代入定義 """
    _fields = ('ident', 'type', 'expr',)

    def __init__(self, ident, type, expr, lineno, lexpos):
        self.ident = ident
        self.type = type
        self.expr = expr
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

# 代入文
class GeneralAssignStatement(VdmslNode):
    """ 一般代入文 """
    _fields = ('statement',)

    def __init__(self, statement, lineno, lexpos):
        self.statement = statement
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class AssignStatement(VdmslNode):
    """ 代入文 """
    _fields = ('status_indicator', 'expr',)

    def __init__(self, status_indicator, expr, lineno, lexpos):
        self.status_indicator = status_indicator
        self.expr = expr
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class StatusIndicator(VdmslNode):
    """ 状態指示子 """
    _fields = ('indicator',)

    def __init__(self, indicator, lineno, lexpos):
        self.indicator = indicator
        self.indicator = lineno
        self.__setattr__('lexpos', lexpos)

class ItemReference(VdmslNode):
    """ 項目参照 """
    _fields = ('status_indicator', 'ident',)

    def __init__(self, status_indicator, ident, lineno, lexpos):
        self.status_indicator = status_indicator
        self.ident = ident
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class MapOrColReference(VdmslNode):
    """ 写像参照または列参照 """
    _fields = ('status_indicator', 'expr',)

    def __init__(self, status_indicator, expr, lineno, lexpos):
        self.status_indicator = status_indicator
        self.expr = expr
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class MultiAssignStatement(VdmslNode):
    """ 多重代入文 """
    _fields = ('assign_stmts',)

    def __init__(self, assign_stmts, lineno, lexpos):
        self.assign_stmts = assign_stmts
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

# 条件文
class IfStatement(VdmslNode):
    """ if文 """
    _fields = ('cond', 'body', 'elseif_stmts', 'else_stmt',)

    def __init__(self, cond, then, elseif_stmts, else_stmt, lineno, lexpos):
        self.cond = cond
        self.then = then
        self.elseif_stmts = elseif_stmts
        self.else_stmt = else_stmt
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
    
class ElseIfStatement(VdmslNode):
    """ elseif文 """
    _fields = ('cond', 'body',)

    def __init__(self, cond, body, lineno, lexpos):
        self.cond = cond
        self.body = body
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class CasesStatement(VdmslNode):
    """ cases文 """
    _fields = ('cond', 'case_stmt_options', 'other_stmt',)

    def __init__(self, cond, case_stmt_options, other, lineno, lexpos):
        self.cond = cond
        self.case_stmt_options = case_stmt_options
        self.other_stmt = other_stmt
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class CaseStmtOption(VdmslNode):
    """ case文選択肢 """
    _fields = ('pattern_list', 'statement',)

    def __init__(self, pattern_list, statement, lineno, lexpos):
        self.pattern_list = pattern_list
        self.statement = statement
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

# forループ文
class ColForStatement(VdmslNode):
    """ 列forループ """
    _fields = ('pattern_binding', 'expr', 'body',)

    def __init__(self, pattern_binding, expr, body, lineno, lexpos):
        self.pattern_binding = pattern_binding
        self.expr = expr
        self.body = body
        self.__setattr__('lineno', lineno) 
        self.__setattr__('lexpos', lexpos)

class SetForStatement(VdmslNode):
    """ 集合forループ """
    _fields = ('pattern', 'expr', 'body',)

    def __init__(self, pattern, expr, body, lineno, lexpos):
        self.pattern = pattern
        self.expr = expr
        self.body = body
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class IndexForStatement(VdmslNode):
    """ 索引forループ """
    _fields = ('ident', 'expr', 'to_expr', 'by_expr', 'body',)

    def __init__(self, ident, expr, to_expr, by_expr, body, lineno, lexpos):
        self.ident = ident
        self.expr = expr
        self.to_expr = to_expr
        self.by_expr = by_expr
        self.body = body
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

# while ループ文
class WhileStatement(VdmslNode):
    """ whileループ """
    _fields = ('cond', 'body',)

    def __init__(self, cond, body, lineno, lexpos):
        self.cond = cond
        self.body = body
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

# 非決定文
class NonDeterminationStatement(VdmslNode):
    """ 非決定文 """
    _fields = ('statements',)

    def __init__(self, statements, lineno, lexpos):
        self.statements = statements
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

# call文
class CallStatement(VdmslNode):
    """ call文 """
    _fields = ('opename', 'expr_list',)

    def __init__(self, opename, expr_list, lineno, lexpos):
        self.opename = opename
        self.expr_list = expr_list
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

# return文
class ReturnStatement(VdmslNode):
    """ return文 """
    _fields = ('expr',)

    def __init__(self, expr, lineno, lexpos):
        self.expr = expr
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

# 例外処理文
class AlwaysStatement(VdmslNode):
    """ always文 """
    _fields = ('stmt1', 'stmt2',)

    def __init__(self, stmt1, stmt2, lineno, lexpos):
        self.stmt1 = stmt1
        self.stmt2 = stmt2
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)


class TrapStatement(VdmslNode):
    """ trap文　"""
    _fields = ('pattern_binding', 'stmt1', 'stmt2',)

    def __init__(self, pattern_binding, stmt1, stmt2, lineno, lexpos):
        self.pattern_binding = pattern_binding
        self.stmt1 = stmt1
        self.stmt2 = stmt2
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)


class RecursiveTrapStatement(VdmslNode):
    """ 再帰trap文 """
    _fields = ('trap_group', 'body',)

    def __init__(self, trap_group, body, lineno, lexpos):
        self.trap_group = trap_group
        self.body = body
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)


class Trap(VdmslNode):
    """ Trap """
    _fields = ('pattern_binding', 'body',)

    def __init__(self, pattern_binding, body, lineno, lexpos):
        self.pattern_binding = pattern_binding
        self.body = body
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class ExitStatement(VdmslNode):
    """ exit文 """
    _fields = ('body',)

    def __init__(self, body ,lineno, lexpos):
        self.body = body
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

# error文
class Error(VdmslNode):
    """ error文 """
    _fields = ()
    
    def __init__(self, lineno, lexpos):
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

# 恒等文
class Skip(VdmslNode):
    """ 恒等文 """
    _fields = ()

    def __init__(self, lineno, lexpos):
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

# 仕様記述文
class SpecDecriptionStatement(VdmslNode):
    """ 仕様記述文 """
    _fields = ('imp_ope_body',)
    
    def __init__(self, imp_ope_body, lineno, lexpos):
        self.imp_ope_body = imp_ope_body
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)


# トップレベル仕様記述
class Specification(VdmslNode):
    """ 文書 """
    _fields = ('blocks',)

    def __init__(self, blocks, lineno, lexpos):
        self.blocks = blocks
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class Block(VdmslNode):
    """ 定義ブロック """
    _fields = ('block',)

    def __init__(self, block, lineno, lexpos):
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)


    
    



# デバッグ用記述
if __name__ == '__main__':
    pass


    



    
