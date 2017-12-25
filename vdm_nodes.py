# -*- coding: utf-8 -*-

class VdmslNode(object):
    """ VDM-SLのASTノード基底クラス """
    _field = ()
    _attributes = ('lineno', 'col_offset')

class NameBase(VdmslNode):
    """ 名称基底クラス """
    _field = ('name',)

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
    _field = ('value',)

    def __init__(self, value, lineno, lexpos):
        self.value = value
        self.lineno = lineno
        self.lexpos = lexpos

# 括弧式
class BracketExpression(VdmslNode):
    """ 括弧式 """
    _field = ('body',)

    def __init__(self, body, lineno, lexpos):
        self.body = body
        self.lineno = lineno
        self.lexpos = lexpos

# let式
class LetExpression(VdmslNode):
    """ let式 """
    _field = ('local_definition', 'body',)

    def __init__(self, local_definition, body, lineno, lexpos):
        self.local_definition = local_definition
        self.body = body
        self.lineno = lineno
        self.lexpos = lexpos

class LetBeExpression(VdmslNode):
    """ letbe式 """
    _field = ('binding', 'Option', 'body',)

    def __init__(self, binding, option, body, lineno, lexpos):
        self.binding = binding
        self.option = option
        self.body = body
        self.lineno = lineno
        self.lexpos = lexpos
 

# def式
class DefExpression(VdmslNode):
    """ def式 """
    _field = ('pattern_binding', 'body',)

    def __init__(self, pattern_binding, body, lineno, lexpos):
        self.pattern_binding = pattern_binding
        self.body = body
        self.lineno = lineno
        self.lexpos = lexpos

# 条件式
class IfExpression(VdmslNode):
    """ if式 """
    _field = ('cond', 'body', 'elseif', 'else',)

    def __init__(self, cond, then, elseif, else_, lineno, lexpos):
        self.cond = cond
        self.then = then
        self.elseif = elseif
        self.else_ = else_
        self.lineno = lineno
        self.lexpos = lexpos

class ElseIfExpression(VdmslNode):
    """ elseif式 """
    _field = ('cond', 'then',)

    def __init__(self, cond, then, lineno, lexpos):
        self.cond = cond
        self.then = then
        self.lineno = lineno
        self.lexpos = lexpos

class CasesExpression(VdmslNode):
    """ cases式 """
    _field = ('cond', 'case_group', 'other',)

    def __init__(self, cond, case_group, other, lineno, lexpos):
        self.cond = cond
        self.case_group = case_group
        self.other = other
        self.lineno = lineno
        self.lexpos = lexpos

# 単項式
class UnaryBaseExpression(VdmslNode):
    """ 単項式基底クラス """
    _field = ('op', 'right',)

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
    _field = ('op', 'left', 'right')

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


# デバッグ用記述
if __name__ == '__main__':
    pass

    



    
