# -*- coding: utf-8 -*-

class VdmslNode(object):
    """ VDM-SLのASTノード基底クラス """
    _fields = ()
    _attributes = ('lineno', 'lexpos')

    def __repr__(self):
        return "{}({})".format(
            self.__class__.__name__,
            ', '.join(["%s=%s" % (field, getattr(self, field))
                    for field in self._fields])
    )

class NameBase(VdmslNode):
    """ 名称基底クラス """
    _fields = ('name',)

    def __init__(self, name, lineno, lexpos):
        self.name = name
        self.lineno = lineno
        self.lexpos = lexpos

class Name(NameBase):
    """ 名称 """
    pass

class OldName(NameBase):
    """ 旧名称 """
    pass

class SymbolLiteral(NameBase):
    """ 記号リテラル """
    pass

# 式
class Expression(VdmslNode):
    """ 式 """
    _fields = ('value',)

    def __init__(self, value, lineno, lexpos):
        self.value = value
        self.lineno = lineno
        self.lexpos = lexpos

# 括弧式
class BracketExpression(VdmslNode):
    """ 括弧式 """
    _fields = ('body',)

    def __init__(self, body, lineno, lexpos):
        self.body = body
        self.lineno = lineno
        self.lexpos = lexpos

# let式
class LetExpression(VdmslNode):
    """ let式 """
    _fields = ('local_definition', 'body',)

    def __init__(self, local_definition, body, lineno, lexpos):
        self.local_definition = local_definition
        self.body = body
        self.lineno = lineno
        self.lexpos = lexpos

class LetBeExpression(VdmslNode):
    """ letbe式 """
    _fields = ('binding', 'Option', 'body',)

    def __init__(self, binding, option, body, lineno, lexpos):
        self.binding = binding
        self.option = option
        self.body = body
        self.lineno = lineno
        self.lexpos = lexpos
 

# def式
class DefExpression(VdmslNode):
    """ def式 """
    _fields = ('pattern_binding', 'body',)

    def __init__(self, pattern_binding, body, lineno, lexpos):
        self.pattern_binding = pattern_binding
        self.body = body
        self.lineno = lineno
        self.lexpos = lexpos

# 条件式
class IfExpression(VdmslNode):
    """ if式 """
    _fields = ('cond', 'body', 'elseif', 'else',)

    def __init__(self, cond, then, elseif, else_, lineno, lexpos):
        self.cond = cond
        self.then = then
        self.elseif = elseif
        self.else_ = else_
        self.lineno = lineno
        self.lexpos = lexpos

class ElseIfExpression(VdmslNode):
    """ elseif式 """
    _fields = ('cond', 'then',)

    def __init__(self, cond, then, lineno, lexpos):
        self.cond = cond
        self.then = then
        self.lineno = lineno
        self.lexpos = lexpos

class CasesExpression(VdmslNode):
    """ cases式 """
    _fields = ('cond', 'case_group', 'other',)

    def __init__(self, cond, case_group, other, lineno, lexpos):
        self.cond = cond
        self.case_group = case_group
        self.other = other
        self.lineno = lineno
        self.lexpos = lexpos

# 単項式
class UnaryBaseExpression(VdmslNode):
    """ 単項式基底クラス """
    _fields = ('op', 'right',)

    def __init__(self, op, right, lineno, lexpos):
        self.op = op
        self.right = right
        self.lineno = lineno
        self.lexpos = lexpos

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
    _fields = ('op', 'left', 'right',)

    def __init__(self, op, left, right, lineno, lexpos):
        self.op = op
        self.left = left
        self.right = right
        self.lineno = lineno
        self.lexpos = lexpos

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
        self.lineno = lineno
        self.lexpos = lexpos

class ExistsExpression(VdmslNode):
    """ 存在限量式 """
    _fields = ('bind_list', 'body',)

    def __init__(self, bind_list, body, lineno, lexpos):
        self.bind_list = bind_list
        self.body = body
        self.lineno = lineno
        self.lexpos = lexpos

class Exist1Expression(VdmslNode):
    """ 1存在限量式 """
    _fields = ('bind', 'body',)

    def __init__(self, bind, body, lineno, lexpos):
        self.bind = bind
        self.body = body
        self.lineno = lineno
        self.lexpos = lexpos

# iota式
class IotaExpression(VdmslNode):
    """ iota式 """
    _fields = ('bind', 'body',)

    def __init__(self, bind, body, lineno, lexpos):
        self.bind = bind
        self.body = body
        self.lineno = lineno
        self.lexpos = lexpos

# 集合式
class SetEnumExpression(VdmslNode):
    """ 集合列挙 """
    _fields = ('expr_list',)

    def __init__(self, expr_list, lineno, lexpos):
        self.expr_list = expr_list
        self.lineno = lineno
        self.lexpos = lexpos

class SetCompExpression(VdmslNode):
    """ 集合内包 """
    _fields = ('body', 'bind_list', 'predicate',)

    def __init__(self, body, bind_list, predicate, lineno, lexpos):
        self.body = body
        self.bind_list = bind_list
        self.predicate = predicate
        self.lineno = lineno
        self.lexpos = lexpos

class SetRangeExpression(VdmslNode):
    """ 集合範囲式 """
    _fields = ('start','end',)

    def __init__(self, start, end, lineno, lexpos):
        self.start = start
        self.end = end
        self.lineno = lineno
        self.lexpos = lexpos

# 列式
class ColEnumExpression(VdmslNode):
    """ 列列挙 """
    _fields = ('expr_list',)

    def __init__(self, expr_list, lineno, lexpos):
        self.expr_list = expr_list
        self.lineno = lineno
        self.lexpos = lexpos

class ColCompExpression(VdmslNode):
    """ 列内包 """
    _fields = ('body', 'set_bind', 'predicate',)

    def __init__(self, body, set_bind, predicate, lineno, lexpos):
        self.body = body
        self.set_bind = set_bind
        self.predicate = predicate
        self.lineno = lineno
        self.lexpos = lexpos

class SubseqExpression(VdmslNode):
    """ 部分列 """
    _fields = ('column', 'start', 'end',)

    def __init__(self, column, start, end, lineno, lexpos):
        self.column = column
        self.start = start
        self.end = end
        self.lineno = lineno
        self.lexpos = lexpos

# 写像式
class MapEnumExpression(VdmslNode):
    """ 写像列挙 """
    _fields = ('map_list',)

    def __init__(self, map_list, lineno, lexpos):
        self.map_list = map_list
        self.lineno = lineno
        self.lexpos = lexpos

class MapExpression(VdmslNode):
    """ 写像 """
    _fields = ('dom', 'range',)

    def __init__(self, dom, range, lineno, lexpos):
        self.dom = dom
        self.range = range
        self.lineno = lineno
        self.lexpos = lexpos

class MapCompExpression(VdmslNode):
    """ 写像内包 """
    _fields = ('map', 'bind_list', 'predicate',)

    def __init__(self, map, bind_list, predicate, lineno, lexpos):
        self.map = map
        self.bind_list = bind_list
        self.predicate = predicate
        self.lineno = lineno
        self.lexpos = lexpos
        
# 組構成子式
class TupleConExpression(VdmslNode):
    """ 組構成子 """
    _fields = ('body', 'expr_list',)

    def __init__(self, body, expr_list, lineno, lexpos):
        self.body = body
        self.expr_list = expr_list
        self.lineno = lineno
        self.lexpos = lexpos

# レコード式
class RecordConExpression(VdmslNode):
    """ レコード構成子 """
    _fields = ('record_name', 'expr_list',)

    def __init__(self, record_name, expr_list, lineno, lexpos):
        self.record_name = record_name
        self.expr_list = expr_list
        self.lineno = lineno
        self.lexpos = lexpos

class RecordModExpression(VdmslNode):
    """ レコード修正子 """
    _fields = ('body', 'record_update_list',)

    def __init__(self, body, record_update_list, lineno, lexpos):
        self.body = body
        self.record_update_list = record_update_list
        self.lineno = lineno
        self.lexpos = lexpos

class RecordUpdateExpression(VdmslNode):
    """ レコード修正 """
    _fields = ('left','right',)

    def __init__(self, left, right, lineno, lexpos):
        self.left = left
        self.right = right
        self.lineno = lineno
        self.lexpos = lexpos

# 適用式
class AppExpression(VdmslNode):
    """ 適用式 """
    _fields = ('body', 'expr_list',)

    def __init__(self, body, expr_list, lineno, lexpos):
        self.body = body
        self.expr_list = expr_list
        self.lineno = lineno
        self.lexpos = lexpos

class ItemChoiceExpression(VdmslNode):
    """ 項目選択式 """
    _fields = ('body',)

    def __init__(self, body, lineno, lexpos):
        self.body = body
        self.lineno = lineno
        self.lexpos = lexpos

class TupleChoiceExpression(VdmslNode):
    """ 組選択式 """
    _fields = ('body',)

    def __init__(self, body, lineno, lexpos):
        self.body = body
        self.lineno = lineno
        self.lexpos = lexpos

class FuncInstExpression(VdmslNode):
    """ 関数型インスタンス化 """
    _fields = ('name', 'type_list',)

    def __init__(self, name, type_list, lineno, lexpos):
        self.name = name
        self.type_list = type_list
        self.lineno = lineno
        self.lexpos = lexpos

# ラムダ式
class LambdaExpression(VdmslNode):
    """ ラムダ式 """
    _fields = ('type_bind_list', 'body',)

    def __init__(self, type_bind_list, body, lineno, lexpos):
        self.type_bind_list = type_bind_list
        self.body = body
        self.lineno = lineno
        self.lexpos = lexpos

# is式
class GeneralIsExpression(VdmslNode):
    """ 一般is式 """
    _fields = ('body',)

    def __init__(self, body, lineno, lexpos):
        self.body = body
        self.lineno = lineno
        self.lexpos = lexpos

class IsExpression(VdmslNode):
    """ is式 """
    _fields = ('type_name', 'body',)

    def __init__(self, type_name, body, lineno, lexpos):
        self.type_name = type_name
        self.body = body
        self.lineno = lineno
        self.lexpos = lexpos

class TypeJudgeExpression(VdmslNode):
    """ 型判定 """
    _fields = ('body', 'type_name',)

    def __init__(self, body, type_name, lineno, lexpos):
        self.body = body
        self.type_name = type_name
        self.lineno = lineno
        self.lexpos = lexpos

# 未定義式
class UnDefExpression(VdmslNode):
    """ 未定義式 """
    _fields = ('body',)

    def __init__(self, body, lineno, lexpos):
        self.body = body
        self.lineno = lineno
        self.lexpos = lexpos

# 事前条件式
class PreCondExpression(VdmslNode):
    """ 事前条件式 """
    _fields = ('expr_list',)

    def __init__(self, expr_list, lineno, lexpos):
        self.expr_list = expr_list
        self.lineno = lineno
        self.lexpos = lexpos

# パターン 
class Pattern(VdmslNode):
    """ パターン """
    _fields = ('patterns',)

    def __init__(self, patterns, lineno, lexpos):
        self.patterns = patterns
        self.lineno = lineno
        self.lexpos = lexpos

class PatternIdent(VdmslNode):
    """ パターン識別子 """
    _fields = ('pattern_ident',)

    def __init__(self, pattern_ident, lineno, lexpos):
        self.pattern_ident = pattern_ident
        self.lineno = lineno
        self.lexpos = lexpos

class MatchValue(VdmslNode):
    """ 一致値 """
    _fields = ('match_value',)

    def __init__(self, match_value, lineno, lexpos):
        self.match_value = match_value
        self.lineno = lineno
        self.lexpos = lexpose

class SetEnumPattern(VdmslNode):
    """ 集合列挙パターン """
    _fields = ('pattern_list',)

    def __init__(self, pattern_list, lineno, lexpos):
        self.pattern_list = pattern_list
        self.lineno = lineno
        self.lexpos = lexpos

class SetUnionPattern(VdmslNode):
    """ 集合合併パターン """
    _fields = ('left', 'right',)

    def __init__(self, left, right, lineno, lexpos):
        self.left = left
        self.right = right
        self.lineno = lineno
        self.lexpos = lexpos

class ColEnumPattern(VdmslNode):
    """ 列列挙パターン """
    _fields = ('pattern_list',)

    def __init__(self, pattern_list, lineno, lexpos):
        self.pattern_list = pattern_list
        self.lineno = lineno
        self.lexpos = lexpos

class ColLinkPattern(VdmslNode):
    """ 列連結パターン """
    _fields = ('left', 'right',)

    def __init__(self, left, right, lineno, lexpos):
        self.left = left
        self.right = right
        self.lineno = lineno
        self.lexpos = lexpos

class MapEnumPattern(VdmslNode):
    """ 写像列挙パターン """
    _fields = ('map_pattern_list',)

    def __init__(self, map_pattern_list, lineno, lexpos):
        self.map_pattern_list = map_pattern_list
        self.lineno = lineno
        self.lexpos = lexpos

class MapPattern(VdmslNode):
    """ 写パターン """
    _fields = ('left', 'right',)

    def __init__(self, left, right, lineno, lexpos):
        self.left = left
        self.right = right
        self.lineno = lineno
        self.lexpos = lexpos

class MapMunionPattern(VdmslNode):
    """ 写像併合パターン """
    _fields = ('left', 'right',)

    def __init__(self, left, right, lineno, lexpos):
        self.left = left
        self.right = right
        self.lineno = lineno
        self.lexpos = lexpos

class TuplePattern(VdmslNode):
    """ 組パターン """
    _fields = ('pattern', 'pattern_list',)

    def __init__(self, pattern, pattern_list, lineno, lexpos):
        self.pattern = pattern
        self.pattern_list = pattern_list
        self.lineno = lineno
        self.lexpos = lexpos

class RecordPattern(VdmslNode):
    """ レコードパターン """
    _fields = ('name', 'pattern_list',)

    def __init__(self, name, pattern_list, lineno, lexpos):
        self.name = name
        self.pattern_list = pattern_list
        self.lineno = lineno
        self.lexpos = lexpos

# 束縛
class Binding(VdmslNode):
    """ 束縛 """
    _fields = ('bindings',)

    def __init__(self, bindings, lineno, lexpos):
        self.bindings = bindings
        self.lineno = lineno
        self.lexpos = lexpos

class SetBinding(VdmslNode):
    """ 集合束縛 """
    _fields = ('pattern', 'expr',)

    def __init__(self, pattern, expr, lineno, lexpos):
        self.pattern = pattern
        self.expr = expr
        self.lineno = lineno
        self.lexpos = lexpos

class TypeBinding(VdmslNode):
    """ 型束縛 """
    _fields = ('pattern', 'type',)

    def __init__(self, pattern, type, lineno, lexpos):
        self.pattern = pattern
        self.type = type
        self.lineno = lineno
        self.lexpos = lexpos

class BindingList(VdmslNode):
    """ 束縛リスト """
    _fields = ('multi_bindings',)

    def __init__(self, multi_bindings, lineno, lexpos):
        self.multi_bindings = multi_bindings
        self.lineno = lineno
        self.lexpos = lexpos

class MultiBinding(VdmslNode):
    """ 多重束縛 """
    _fields = ('bindings',)

    def __init__(self, bindings, lineno, lexpos):
        self.bindings = bindings
        self.lineno = lineno
        self.lexpos = lexpos

class MultiSetBinding(VdmslNode):
    """ 多重集合束縛 """
    _fields = ('pattern_list', 'expr',)

    def __init__(self, pattern_list, expr, lineno, lexpos):
        self.pattern_list = pattern_list
        self.expr = expr
        self.lineno = lineno 
        self.lexpos = lexpos

class MultiTypeBinding(VdmslNode):
    """ 多重型束縛 """
    _fields = ('pattern_list', 'type',)

    def __init__(self, pattern_list, type, lineno, lexpos):
        self.pattern_list = pattern_list
        self.type = type
        self.lineno = lineno
        self.lexpos = lexpos



# デバッグ用記述
if __name__ == '__main__':
    pass

    



    
