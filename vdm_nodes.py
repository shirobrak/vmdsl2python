# -*- coding: utf-8 -*-

import ast as pyast
import re

# 定数
VDMFUNC_MODULE_NAME = 'vdmslfunc'

# 数値リテラル用正規表現
HEXNUM = re.compile(r"(0x|0X)[0-9a-fA-F]+")
INTNUM = re.compile(r"\d+((E|e)(\+|\-)?\d+)?")
FLOATNUM = re.compile(r"\dA+\.(\d+)((E|e)(\+|\-)?\d+)?")


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

    @classmethod
    def _p(self, v, indent):
        output = "{}{}".format(self.SPACER * indent, v)
        return output + '\n'

    def dumps(self, indent=0):
        output = ""
        output += self._p(self.__class__.__name__ + '(', indent)
        for field in self._fields:
            output += self._p(field + '=', indent + 1)
            value = getattr(self, field)
            if type(value) == list:
                for value2 in value:
                    if isinstance(value2, VdmslNode):
                        output += value2.dumps(indent + 2)
                    else:
                        output += self._p(value2, indent + 2)
            else:
                if value:
                    if isinstance(value, VdmslNode):
                        output += value.dumps(indent + 2)
                    else:
                        output += self._p(value, indent + 2)
        output += self._p(')', indent)
        return output
    
    def toPy(self):
        """ this func is converter VDM-SL Node to Python Node of ast module """
        return pyast.AST

# モジュール本体

class ModuleBody(VdmslNode):
    """ モジュール本体 """
    _fields = ('blocks',)

    def __init__(self, blocks, lineno, lexpos):
        self.blocks = blocks
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
    
    def toPy(self):
        stmt_list = []
        stmt_list += [pyast.Import([pyast.alias('vdmslfunc', None)])]
        for block in self.blocks:
            stmt_list += block.toPy()
        return pyast.Module(stmt_list)

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
    def toPy(self):
        return pyast.Name('bool', pyast.Load())

class NatType(BasicDataType):
    """ Nat型(自然数) """
    def toPy(self):
        return pyast.Name('nat', pyast.Load())

class Nat1Type(BasicDataType):
    """ Nat1型(正の自然数) """
    def toPy(self):
        return pyast.Name('nat1', pyast.Load())

class IntType(BasicDataType):
    """ Int型(整数) """
    def toPy(self):
        return pyast.Name('int', pyast.Load())

class RatType(BasicDataType):
    """ Rat型(有理数) """
    def toPy(self):
        return pyast.Name('rat', pyast.Load())

class RealType(BasicDataType):
    """ Real型(実数) """
    def toPy(self):
        return pyast.Name('real', pyast.Load())

class CharType(BasicDataType):
    """ 文字型 """
    def toPy(self):
        return pyast.Name('char', pyast.Load())

class QuoteType(BasicDataType):
    """ 引用型 """
    def toPy(self):
        return pyast.Name('quote', pyast.Load())

class TokenType(BasicDataType):
    """ トークン型 """
    def toPy(self):
        return pyast.Name('token', pyast.Load())

# 合成型
class SyntheticDataType(VdmslNode):
    """ 合成型基底クラス """
    _fields = ('type_name',)

    def __init__(self, type_name, lineno, lexpos):
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
    
    def toPy(self):
        return pyast.Name(self.id, pyast.Load())

class Name(NameBase):
    """ 名称 """
    def toPy(self):
        return pyast.Name(self.id, pyast.Load())

class OldName(NameBase):
    """ 旧名称 """
    def toPy(self):
        return pyast.Name(self.id, pyast.Load())

class SymbolLiteral(NameBase):
    """ 記号リテラル """
    pass

class VdmBool(NameBase):
    """ ブールリテラル """
    def toPy(self):
        if self.id == 'true':
            return pyast.NameConstant(True)
        elif self.id == 'false':
            return pyast.NameConstant(False)
        else:
            return pyast.NameConstant(None)

class VdmNum(NameBase):
    """ 数値リテラル """
    def toPy(self):
        # 数値型チェック
        if re.fullmatch(HEXNUM, self.id):
            return pyast.Num(int(self.id, 16))
        elif re.fullmatch(FLOATNUM, self.id):
            return pyast.Num(float(self.id))
        elif re.fullmatch(INTNUM, self.id):
            return pyast.Num(int(self.id))

class VdmChar(NameBase):
    """ 文字リテラル """
    def toPy(self):
        char = self.id.replace('’','')
        return pyast.Str(char)

class VdmText(NameBase):
    """ テキストリテラル """
    def toPy(self):
        txt = self.id.replace('"','')
        return pyast.Str(txt)

class VdmQuote(NameBase):
    """ 引用リテラル """
    def toPy(self):
        return pyast.Str(self.id)

class TypeName(NameBase):
    """ 型名称 """
    def toPy(self):
        return self.id.toPy()

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

    def toPy(self):
        return self.value.toPy()

# 括弧式
class BracketExpression(VdmslNode):
    """ 括弧式 """
    _fields = ('body',)

    def __init__(self, body, lineno, lexpos):
        self.body = body
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
    
    def toPy(self):
        return self.body.toPy()

# let式
class LetExpression(VdmslNode):
    """ let式 """
    _fields = ('local_definition', 'body',)

    def __init__(self, local_definition, body, lineno, lexpos):
        self.local_definition = local_definition
        self.body = body
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
    
    def toPy(self):
        body = self.body.toPy()
        ptns = []
        exprs = []
        for ld in self.local_definition:
            ptns += [pyast.arg(ld.definition.pattern.toPy(), None)]
            exprs += [ld.definition.expr.toPy()]
        args = pyast.arguments(ptns, None, [], [], None, [])
        func = pyast.Lambda(args, body)
        return pyast.Call(func, exprs,[])
         
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
    
    def toPy(self):
        body = self.body.toPy()
        pbs = []
        exprs = []
        for pb in self.pattern_binding:
            pbs += [pyast.arg(pb.ptn_binding.toPy(), None)]
            exprs += [pb.expr.toPy()]
        args = pyast.arguments(pbs, None, [], [], None, [])
        func = pyast.Lambda(args, body)
        return pyast.Call(func, exprs,[])

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
    
    def toPy(self):
        el = self.else_
        def create_orelse(elifs):
            if elifs == []:
                return el.toPy()
            elif len(elifs) == 1:
                return pyast.IfExp(elifs[0].cond.toPy(), elifs[0].then.toPy(), el.toPy())
            else:
                return pyast.IfExp(elifs[0].cond.toPy(), elifs[0].then.toPy(), create_orelse(elifs[1:]))

        return pyast.IfExp(self.cond.toPy(), self.body.toPy(), create_orelse(self.elseif))

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
    
    def toPy(self):
        cond = self.cond.toPy()
        ops = [pyast.Eq()]

        def make_comp_expr(comparators):
            return pyast.Compare(cond, ops, comparators.toPy())

        def make_case_group(cgs):
            if len(cgs) == 1:
                if self.other == []:
                    return pyast.IfExp(make_comp_expr(cgs[0].pattern_list), cgs[0].expr.toPy(), None)
                else:
                    return pyast.IfExp(make_comp_expr(cgs[0].pattern_list), cgs[0].expr.toPy(), self.other.toPy())
            else:
                return pyast.IfExp(make_comp_expr(cgs[0].pattern_list), cgs[0].expr.toPy(), make_case_group(cgs[1:]))

        return make_case_group(self.case_group)
        
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
    """ 正符号 """
    def toPy(self):
        return pyast.UnaryOp(pyast.UAdd(), self.right.toPy())

class Minus(UnaryBaseExpression):
    """ 負符号 """
    def toPy(self):
        return pyast.UnaryOp(pyast.USub(), self.right.toPy())

class Abs(UnaryBaseExpression):
    """ 算術絶対値 """
    def toPy(self):
        return pyast.Call(pyast.Name('abs', pyast.Load()), [self.right.toPy()], [])

class Floor(UnaryBaseExpression):
    """ 底値 """
    def toPy(self):
        attr = 'floor'
        func = pyast.Attribute(pyast.Name(VDMFUNC_MODULE_NAME, pyast.Load()), attr, pyast.Load())
        args = [self.right.toPy()]
        keywords = []
        return pyast.Call(func, args, keywords)

class Not(UnaryBaseExpression):
    """ 否定 """
    def toPy(self):
        return pyast.UnaryOp(pyast.Not(), self.right.toPy())

class Card(UnaryBaseExpression):
    """ 集合の濃度 """
    def toPy(self):
        return pyast.Call(pyast.Name('len', pyast.Load()), [self.right.toPy()], [])

class Power(UnaryBaseExpression):
    """ べき集合 """
    def toPy(self):
        attr = 'power'
        func = pyast.Attribute(pyast.Name(VDMFUNC_MODULE_NAME, pyast.Load()), attr, pyast.Load())
        args = [self.right.toPy()]
        keywords = []
        return pyast.Call(func, args, keywords)

class Dunion(UnaryBaseExpression):
    """ 分配的集合合併 """
    def toPy(self):
        attr = 'dunion'
        func = pyast.Attribute(pyast.Name(VDMFUNC_MODULE_NAME, pyast.Load()), attr, pyast.Load())
        args = [self.right.toPy()]
        keywords = []
        return pyast.Call(func, args, keywords)

class Dinter(UnaryBaseExpression):
    """ 分配的集合共通部分 """
    def toPy(self):
        attr = 'dinter'
        func = pyast.Attribute(pyast.Name(VDMFUNC_MODULE_NAME, pyast.Load()), attr, pyast.Load())
        args = [self.right.toPy()]
        keywords = []
        return pyast.Call(func, args, keywords)

class Hd(UnaryBaseExpression):
    """ 列の先頭 """
    def toPy(self):
        return pyast.Subscript(self.right.toPy(), pyast.Index(pyast.Num(n=0)), pyast.Load())

class Tl(UnaryBaseExpression):
    """ 列の尾部 """
    def toPy(self):
        return pyast.Subscript(self.right.toPy(), pyast.Index(pyast.UnaryOp(pyast.USub(), pyast.Num(n=1))), pyast.Load())

class Len(UnaryBaseExpression):
    """ 列の長さ """
    def toPy(self):
        return pyast.Call(pyast.Name('len', pyast.Load()), [self.right.toPy()], [])

class Elems(UnaryBaseExpression):
    """ 要素集合 """
    def toPy(self):
        return pyast.Call(pyast.Name('set', pyast.Load()), [self.right.toPy()], [])

class Inds(UnaryBaseExpression):
    """ 索引集合 """
    def toPy(self):
        return pyast.ListComp(pyast.Name('e', pyast.Load()), [pyast.comprehension(pyast.Name('e', pyast.Store()), pyast.Call(pyast.Name('range', pyast.Load()), [pyast.Call(pyast.Name('len', pyast.Load()), [self.right.toPy()], [])], []), [], 0)])

class Conc(UnaryBaseExpression):
    """ 分配的列連結 """
    def toPy(self):
        attr = 'conc'
        func = pyast.Attribute(pyast.Name(VDMFUNC_MODULE_NAME, pyast.Load()), attr, pyast.Load())
        args = [self.right.toPy()]
        keywords = []
        return pyast.Call(func, args, keywords)

class Dom(UnaryBaseExpression):
    """ 定義域 """
    def toPy(self):
        return pyast.Call(pyast.Name('set', pyast.Load()), [pyast.Call(pyast.Attribute(self.right.toPy(), 'keys', pyast.Load()), [], [])], [])

class Rng(UnaryBaseExpression):
    """ 値域 """
    def toPy(self):
        return pyast.Call(pyast.Name('set', pyast.Load()), [pyast.Call(pyast.Attribute(self.right.toPy(), 'values', pyast.Load()), [], [])], [])

class Merge(UnaryBaseExpression):
    """ 分配的写像併合 """
    pass

class Inverse(UnaryBaseExpression):
    """ 逆写像 """
    def toPy(self):
        attr = 'map_inverse'
        func = pyast.Attribute(pyast.Name(VDMFUNC_MODULE_NAME, pyast.Load()), attr, pyast.Load())
        args = [self.right.toPy()]
        keywords = []
        return pyast.Call(func, args, keywords)

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
    def toPy(self):
        return pyast.BinOp(self.left.toPy(), pyast.Add(), self.right.toPy())

class Sub(BinBaseExpression):
    """ 減算 """
    def toPy(self):
        return pyast.BinOp(self.left.toPy(), pyast.Sub(), self.right.toPy())

class Mul(BinBaseExpression):
    """ 乗算 """
    def toPy(self):
        return pyast.BinOp(self.left.toPy(), pyast.Mult(), self.right.toPy())

class Div(BinBaseExpression):
    """ 除算 """
    def toPy(self):
        return pyast.BinOp(self.left.toPy(), pyast.Div(), self.right.toPy())

class IntDiv(BinBaseExpression):
    """ 整数除算 """
    def toPy(self):
        return pyast.BinOp(self.left.toPy(), pyast.FloorDiv(), self.right.toPy())

class Rem(BinBaseExpression):
    """ 剰余算 """
    def toPy(self):
        attr = 'rem'
        func = pyast.Attribute(pyast.Name(VDMFUNC_MODULE_NAME, pyast.Load()), attr, pyast.Load())
        args = [self.left.toPy(), self.right.toPy()]
        keywords = []
        return pyast.Call(func, args, keywords)

class Mod(BinBaseExpression):
    """ 法算 """
    def toPy(self):
        return pyast.BinOp(self.left.toPy(), pyast.Mod(), self.right.toPy())

class Lt(BinBaseExpression):
    """ より小さい """
    def toPy(self):
        return pyast.Compare(self.left.toPy(), [pyast.Lt()], [self.right.toPy()])

class LtEq(BinBaseExpression):
    """ より小さいか等しい """
    def toPy(self):
        return pyast.Compare(self.left.toPy(), [pyast.LtE()], [self.right.toPy()])

class Gt(BinBaseExpression):
    """ より大きい """
    def toPy(self):
        return pyast.Compare(self.left.toPy(), [pyast.Gt()], [self.right.toPy()])

class GtEq(BinBaseExpression):
    """ より大きいか等しい """
    def toPy(self):
        return pyast.Compare(self.left.toPy(), [pyast.GtE()], [self.right.toPy()])

class Equal(BinBaseExpression):
    """ 相等 """
    def toPy(self):
        return pyast.Compare(self.left.toPy(), [pyast.Eq()], [self.right.toPy()])

class NotEq(BinBaseExpression):
    """ 不等 """
    def toPy(self):
        return pyast.Compare(self.left.toPy(), [pyast.NotEq()], [self.right.toPy()])

class Or(BinBaseExpression):
    """ 論理和 """
    def toPy(self):
        return pyast.BoolOp(pyast.Or(), [self.left.toPy(), self.right.toPy()])

class And(BinBaseExpression):
    """ 論理積 """
    def toPy(self):
        return pyast.BoolOp(pyast.And(), [self.left.toPy(), self.right.toPy()])

class Imp(BinBaseExpression):
    """ 含意 """
    def toPy(self):
        return pyast.BoolOp(pyast.Or(), [pyast.UnaryOp(pyast.Not(), self.left.toPy()), self.right.toPy()])

class Equivalence(BinBaseExpression):
    """ 同値 """
    def toPy(self):
        return pyast.BoolOp(pyast.And(), [pyast.BoolOp(pyast.Or(), [pyast.UnaryOp(pyast.Not(), self.left.toPy()), self.right.toPy()]), pyast.BoolOp(pyast.Or(), [pyast.UnaryOp(pyast.Not(), self.right.toPy()), self.left.toPy()])])

class InSet(BinBaseExpression):
    """ 帰属 """
    def toPy(self):
        return pyast.Compare(self.left.toPy(), [pyast.In()], [self.right.toPy()])

class NotInSet(BinBaseExpression):
    """ 非帰属 """
    def toPy(self):
        return pyast.Compare(self.left.toPy(), [pyast.NotIn()], [self.right.toPy()])

class Subset(BinBaseExpression):
    """ 包含 """
    def toPy(self):
        return pyast.Compare(self.left.toPy(), [pyast.GtE()], [self.right.toPy()])
    
class PSubset(BinBaseExpression):
    """ 真包含 """
    def toPy(self):
        return pyast.Compare(self.left.toPy(), [pyast.Gt()], [self.right.toPy()])

class Union(BinBaseExpression):
    """ 集合合併 """
    def toPy(self):
        return pyast.BinOp(self.left.toPy(), pyast.BitOr(), self.right.toPy())

class SetDiff(BinBaseExpression):
    """ 集合差 """
    def toPy(self):
        return pyast.BinOp(self.left.toPy(), pyast.Sub(), self.right.toPy())

class Inter(BinBaseExpression):
    """ 集合共通部分 """
    def toPy(self):
        return pyast.BinOp(self.left.toPy(), pyast.BitAnd(), self.right.toPy())

class ColLink(BinBaseExpression):
    """ 列連結 """
    def toPy(self):
        return pyast.BinOp(self.left.toPy(), pyast.Add(), self.right.toPy())

class MapColUpdate(BinBaseExpression):
    """ 写像修正または列修正 """
    def toPy(self):
        attr = 'map_or_list_update'
        func = pyast.Attribute(pyast.Name(VDMFUNC_MODULE_NAME, pyast.Load()), attr, pyast.Load())
        args = [self.left.toPy(), self.right.toPy()]
        keywords = []
        return pyast.Call(func, args, keywords)

class Munion(BinBaseExpression):
    """ 写像併合 """
    def toPy(self):
        return pyast.Call(pyast.Attribute(self.left.toPy(), 'update', pyast.Load()), [self.right.toPy()], [])

class MapDomRes(BinBaseExpression):
    """ 写像定義域限定 """
    def toPy(self):
        attr = 'limit_map_dom'
        func = pyast.Attribute(pyast.Name(VDMFUNC_MODULE_NAME, pyast.Load()), attr, pyast.Load())
        args = [self.left.toPy(), self.right.toPy()]
        keywords = []
        return pyast.Call(func, args, keywords)

class MapDomRed(BinBaseExpression):
    """ 写像定義域削減 """
    def toPy(self):
        attr = 'reduce_map_dom'
        func = pyast.Attribute(pyast.Name(VDMFUNC_MODULE_NAME, pyast.Load()), attr, pyast.Load())
        args = [self.left.toPy(), self.right.toPy()]
        keywords = []
        return pyast.Call(func, args, keywords)

class MapRangeRes(BinBaseExpression):
    """ 写像値域限定 """
    def toPy(self):
        attr = 'limit_map_range'
        func = pyast.Attribute(pyast.Name(VDMFUNC_MODULE_NAME, pyast.Load()), attr, pyast.Load())
        args = [self.left.toPy(), self.right.toPy()]
        keywords = []
        return pyast.Call(func, args, keywords)

class MapRangeRed(BinBaseExpression):
    """ 写像値域削減 """
    def toPy(self):
        attr = 'reduce_map_range'
        func = pyast.Attribute(pyast.Name(VDMFUNC_MODULE_NAME, pyast.Load()), attr, pyast.Load())
        args = [self.left.toPy(), self.right.toPy()]
        keywords = []
        return pyast.Call(func, args, keywords)

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
    
    def toPy(self):
        ptns = []
        binds = []
        for e in self.bind_list:
            ptns += e.pattern_list.patterns
            binds += [e.expr.toPy()]
        
        ctx = pyast.Load()
        args = pyast.arguments([pyast.arg(p.toPy(), None) for p in ptns], None, [], [], None, [])
        cond_expr = pyast.Lambda(args, self.body.toPy())
        attr = 'forall'
        call_func = pyast.Attribute(pyast.Name(VDMFUNC_MODULE_NAME, ctx), attr, ctx)
        call_args = [pyast.List(binds, ctx), cond_expr]
        return pyast.Call(call_func, call_args, [])

class ExistsExpression(VdmslNode):
    """ 存在限量式 """
    _fields = ('bind_list', 'body',)

    def __init__(self, bind_list, body, lineno, lexpos):
        self.bind_list = bind_list
        self.body = body
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
    
    def toPy(self):
        ptns = []
        binds = []
        for e in self.bind_list:
            ptns += e.pattern_list.patterns
            binds += [e.expr.toPy()]
        
        ctx = pyast.Load()
        args = pyast.arguments([pyast.arg(p.toPy(), None) for p in ptns], None, [], [], None, [])
        cond_expr = pyast.Lambda(args, self.body.toPy())
        attr = 'exists'
        call_func = pyast.Attribute(pyast.Name(VDMFUNC_MODULE_NAME, ctx), attr, ctx)
        call_args = [pyast.List(binds, ctx), cond_expr]
        return pyast.Call(call_func, call_args, [])

class Exist1Expression(VdmslNode):
    """ 1存在限量式 """
    _fields = ('bind', 'body',)

    def __init__(self, bind, body, lineno, lexpos):
        self.bind = bind
        self.body = body
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
    
    def toPy(self):
        ctx = pyast.Load()
        cond_args = pyast.arguments([self.bind.bindings.pattern.toPy()], None, [], [], None, [])
        cond_expr = pyast.Lambda(cond_args, self.body.toPy())
        attr = 'exists1'
        call_func = pyast.Attribute(pyast.Name(VDMFUNC_MODULE_NAME, ctx), attr, ctx)
        call_args = [self.bind.bindings.expr.toPy(), cond_expr]
        return pyast.Call(call_func, call_args, [])

# iota式
class IotaExpression(VdmslNode):
    """ iota式 """
    _fields = ('bind', 'body',)

    def __init__(self, bind, body, lineno, lexpos):
        self.bind = bind
        self.body = body
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
    
    def toPy(self):
        ctx = pyast.Load()
        cond_args = pyast.arguments([self.bind.bindings.pattern.toPy()], None, [], [], None, [])
        cond_expr = pyast.Lambda(cond_args, self.body.toPy())
        attr = 'iota'
        call_func = pyast.Attribute(pyast.Name(VDMFUNC_MODULE_NAME, ctx), attr, ctx)
        call_args = [self.bind.bindings.expr.toPy(), cond_expr]
        return pyast.Call(call_func, call_args, [])

# 集合式
class SetEnumExpression(VdmslNode):
    """ 集合列挙 """
    _fields = ('expr_list',)

    def __init__(self, expr_list, lineno, lexpos):
        self.expr_list = expr_list
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

    def toPy(self):
        # 集合の集合対策してない. 
        # リストの対策も. 
        elts = [ e.toPy() for e in self.expr_list ]
        return pyast.Set(elts)

class SetCompExpression(VdmslNode):
    """ 集合内包 """
    _fields = ('body', 'bind_list', 'predicate',)

    def __init__(self, body, bind_list, predicate, lineno, lexpos):
        self.body = body
        self.bind_list = bind_list
        self.predicate = predicate
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

    def toPy(self):
        # 集合束縛のパターンは1つしか受け付けれない
        elt = self.body.toPy()
        binding = self.bind_list[0]
        target = binding.pattern_list.toPy()[0]
        iter = binding.expr.toPy()
        ifs = [self.predicate.toPy()]
        generators = [pyast.comprehension(target, iter, ifs, 0)]
        return pyast.SetComp(elt, generators)
        

class SetRangeExpression(VdmslNode):
    """ 集合範囲式 """
    _fields = ('start','end',)

    def __init__(self, start, end, lineno, lexpos):
        self.start = start
        self.end = end
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
    
    def toPy(self):
        elt = pyast.Name('e', pyast.Load())
        start = self.start.toPy()
        if type(self.end.toPy()) == pyast.Num:
            end = pyast.Num(self.end.toPy().n+1)
        else:
            end = pyast.BinOp(self.end.toPy(), pyast.Add(), pyast.Num(1))
        generators = [pyast.comprehension(pyast.Name('e', pyast.Store()), 
                      pyast.Call(pyast.Name('range', pyast.Load()), [start, end], []), [], 0)]
        return pyast.SetComp(elt, generators)

# 列式
class ColEnumExpression(VdmslNode):
    """ 列列挙 """
    _fields = ('expr_list',)

    def __init__(self, expr_list, lineno, lexpos):
        self.expr_list = expr_list
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
    
    def toPy(self): 
        elts = [ e.toPy() for e in self.expr_list ]
        return pyast.List(elts, pyast.Load())

class ColCompExpression(VdmslNode):
    """ 列内包 """
    _fields = ('body', 'set_bind', 'predicate',)

    def __init__(self, body, set_bind, predicate, lineno, lexpos):
        self.body = body
        self.set_bind = set_bind
        self.predicate = predicate
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
    
    def toPy(self):
        # 集合束縛のパターンは1つしか受け付けれない
        elt = self.body.toPy()
        target = self.set_bind.pattern.toPy()
        iter = self.set_bind.expr.toPy()
        ifs = [self.predicate.toPy()]
        generators = [pyast.comprehension(target, iter, ifs, 0)]
        return pyast.ListComp(elt, generators)

class SubseqExpression(VdmslNode):
    """ 部分列 """
    _fields = ('column', 'start', 'end',)

    def __init__(self, column, start, end, lineno, lexpos):
        self.column = column
        self.start = start
        self.end = end
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
    
    def toPy(self):
        value = self.column.toPy()
        if type(self.start.toPy()) == pyast.Num:
            lower = pyast.Num(self.start.toPy().n-1)
        else:
            lower = pyast.BinOp(self.start.toPy(), pyast.Sub(), pyast.Num(1))
        if type(self.end.toPy()) == pyast.Num:
            upper = pyast.Num(self.end.toPy().n-1)
        else:
            upper = pyast.BinOp(self.end.toPy(), pyast.Sub(), pyast.Num(1))
        slice = pyast.Slice(lower, upper, None)
        ctx = pyast.Load()
        return pyast.Subscript(value, slice, ctx)
        

# 写像式
class MapEnumExpression(VdmslNode):
    """ 写像列挙 """
    _fields = ('map_list',)

    def __init__(self, map_list, lineno, lexpos):
        self.map_list = map_list
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
    
    def toPy(self):
        keys = []
        values = []
        for map in self.map_list:
            keys.append(map.dom.toPy())
            values.append(map.range.toPy())
        return pyast.Dict(keys, values)

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
    
    def toPy(self):
        # 写像束縛のパターンは1つしか受け付けれない
        key = self.map.dom.toPy()
        value = self.map.range.toPy()
        binding = self.bind_list[0]
        elts = [ e for e in binding.pattern_list.toPy() ]
        target = pyast.Tuple(elts, pyast.Store())
        iter = binding.expr.toPy()
        ifs = [self.predicate.toPy()]
        generators = [pyast.comprehension(target, iter, ifs, 0)]
        return pyast.DictComp(key, value, generators)
        
# 組構成子式
class TupleConExpression(VdmslNode):
    """ 組構成子 """
    _fields = ('elts',)

    def __init__(self, elts, lineno, lexpos):
        self.elts = elts
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
    
    def toPy(self):
        elts = [e.toPy() for e in self.elts]
        ctx = pyast.Load()
        return pyast.Tuple(elts, ctx)

# レコード式
class RecordConExpression(VdmslNode):
    """ レコード構成子 """
    _fields = ('record_name', 'expr_list',)

    def __init__(self, record_name, expr_list, lineno, lexpos):
        self.record_name = record_name
        self.expr_list = expr_list
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
    
    def toPy(self):
        exprs = [ expr.toPy() for expr in self.expr_list ]
        func = self.record_name.toPy()
        args = [ e for e in exprs ]
        keywords = []
        return pyast.Call(func, args, keywords)

class RecordModExpression(VdmslNode):
    """ レコード修正子 """
    _fields = ('body', 'record_update_list',)

    def __init__(self, body, record_update_list, lineno, lexpos):
        self.body = body
        self.record_update_list = record_update_list
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
    
    def toPy(self):
        pass

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
    
    def toPy(self):
        func = self.body.toPy()
        args = [ e.toPy() for e in self.expr_list ]
        return pyast.Call(func, args, [])

class ItemChoice(VdmslNode):
    """ 項目選択式 """
    _fields = ('expr', 'ident',)

    def __init__(self, expr, ident, lineno, lexpos):
        self.expr = expr
        self.ident = ident
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

    def toPy(self):
        value = self.expr.toPy()
        attr = self.ident
        ctx = pyast.Store()
        return pyast.Attribute(value, attr, ctx)

class TupleChoice(VdmslNode):
    """ 組選択式 """
    _fields = ('expr', 'index',)

    def __init__(self, expr, index, lineno, lexpos):
        self.expr = expr
        self.index = index
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
    
    def toPy(self):
        value = self.expr.toPy()
        slice = pyast.Index(pyast.Num(int(self.index)))
        ctx = pyast.Load()
        return pyast.Subscript(value, slice, ctx)

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

    def toPy(self):
        args = pyast.arguments([x.pattern.toPy() for x in self.type_bind_list], None, [], [], None, [])
        return pyast.Lambda(args, self.body.toPy())

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
    
    def toPy(self):
        ctx = pyast.Load()
        call = pyast.Call(pyast.Name('type', ctx), [self.body.toPy()], [])
        ops = [pyast.Eq()]
        comparators = [pyast.Name(self.type_name, ctx)]
        return pyast.Compare(call, ops, comparators)

class TypeJudgeExpression(VdmslNode):
    """ 型判定 """
    _fields = ('body', 'type_name',)

    def __init__(self, body, type_name, lineno, lexpos):
        self.body = body
        self.type_name = type_name
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
    
    def toPy(self):
        ctx = pyast.Load()
        call = pyast.Call(pyast.Name('type', ctx), [self.body.toPy()], [])
        ops = [pyast.Eq()]
        comparators = [self.type_name.toPy()]
        return pyast.Compare(call, ops, comparators)

# 未定義式
class UnDefExpression(VdmslNode):
    """ 未定義式 """
    _fields = ('body',)

    def __init__(self, body, lineno, lexpos):
        self.body = body
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
    
    def toPy(self):
        return pyast.NameConstant(None)

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
    
    def toPy(self):
        return pyast.Name(self.ptn_id, pyast.Load())

class MatchValue(VdmslNode):
    """ 一致値 """
    _fields = ('match_value',)

    def __init__(self, match_value, lineno, lexpos):
        self.match_value = match_value
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
    def toPy(self):
        return self.match_value.toPy()

class SetEnumPattern(VdmslNode):
    """ 集合列挙パターン """
    _fields = ('ptn_list',)

    def __init__(self, ptn_list, lineno, lexpos):
        self.ptn_list = ptn_list
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
    
    def toPy(self):
        elts = [ ptn.toPy() for ptn in self.ptn_list ]
        return pyast.Set(elts)

class SetUnionPattern(VdmslNode):
    """ 集合合併パターン """
    _fields = ('left', 'right',)

    def __init__(self, left, right, lineno, lexpos):
        self.left = left
        self.right = right
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
    
    def toPy(self):
        return pyast.BinOp(self.left.toPy(), pyast.BitOr(), self.right.toPy())

class ColEnumPattern(VdmslNode):
    """ 列列挙パターン """
    _fields = ('ptn_list',)

    def __init__(self, ptn_list, lineno, lexpos):
        self.ptn_list = ptn_list
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
    
    def toPy(self):
        elts = [ ptn.toPy() for ptn in self.ptn_list ]
        return List(elts, pyast.Load())

class ColLinkPattern(VdmslNode):
    """ 列連結パターン """
    _fields = ('left', 'right',)

    def __init__(self, left, right, lineno, lexpos):
        self.left = left
        self.right = right
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
    
    def toPy(self):
        return pyast.BinOp(self.left.toPy(), pyast.Add(), self.right.toPy())

class MapEnumPattern(VdmslNode):
    """ 写像列挙パターン """
    _fields = ('map_pattern_list',)

    def __init__(self, map_pattern_list, lineno, lexpos):
        self.map_pattern_list = map_pattern_list
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
    
    def toPy(self):
        keys = []
        values = []
        for map_ptn in self.map_pattern_list:
            keys.append(map_ptn.key.toPy())
            values.append(map_ptn.value.toPy())
        return pyast.Dict(keys, values)
        
class MapPattern(VdmslNode):
    """ 写パターン """
    _fields = ('key', 'value',)

    def __init__(self, key, value, lineno, lexpos):
        self.key = key
        self.value = value
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
    
    def toPy(self):
        return pyast.Call(pyast.Attribute(self.left.toPy(), 'update', pyast.Load()), [self.right.toPy()], [])

class TuplePattern(VdmslNode):
    """ 組パターン """
    _fields = ('ptn_list',)

    def __init__(self, ptn_list, lineno, lexpos):
        self.ptn_list = ptn_list
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
    
    def toPy(self):
        elts = [e.toPy() for e in self.ptn_list]
        ctx = pyast.Load()
        return pyast.Tuple(elts, ctx)

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
    
    def toPy(self):
        return 

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

    # 出力 stmt* body
    def toPy(self):
        return [stmt.toPy() for stmt in self.value_definitions]

class ValueDefinition(VdmslNode):
    """ 値定義 """
    _fields = ('pattern', 'type', 'expr',)

    def __init__(self, pattern, type, expr, lineno, lexpos):
        self.pattern = pattern
        self.type = type
        self.expr = expr
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
    
    def toPy(self):
        if self.type == None:
            return pyast.Assign([self.pattern.toPy()], self.expr.toPy())
        else:
            return pyast.AnnAssign(self.pattern.toPy(), self.type.toPy(), self.expr.toPy(), 1)
        

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
    
    def toPy(self):
        stmts = []
        for stmt in self.operation_definitions:
            stmts += stmt.toPy()
        return stmts
        
class OpeDefinition(VdmslNode):
    """ 操作定義 """
    _fields = ('operation_definition',)

    def __init__(self, operation_definition, lineno, lexpos):
        self.operation_definition = operation_definition
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

    def toPy(self):
        return self.operation_definition.toPy()

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
    
    def toPy(self):
        func_name = self.ope_ident
        func_args = pyast.arguments([pyast.arg(e.ptn_id, None) for e in self.param_group.pattern_list.patterns], None, [], [], None, [])
        ope_body = self.ope_body.toPy()
        decorator_list = []
        returns = None                  
        return [pyast.FunctionDef(func_name, func_args, ope_body, decorator_list, returns)]

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
    
    def toPy(self):
        name = self.ident
        args = self.param_type.toPy()
        body = [pyast.Pass()]
        return pyast.FunctionDef(name, args, body, [], None)

class ImpOpeBody(VdmslNode):
    """ 陰操作本体 """
    _fields = ('ext_sec', 'pre_expr', 'post_expr', 'exception',)

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
    
    def toPy(self):
        return [ p.toPy() for p in self.patterns ] 
        
class OperationBody(VdmslNode):
    """ 操作本体 """
    _fields = ('statement',)

    def __init__(self, statement, lineno, lexpos):
        self.statement = statement
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
    
    def toPy(self):
        return self.statement.toPy()

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

class ErrorExpr(VdmslNode):
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
    
     # 出力 stmt* body
    def toPy(self):
        return [stmt.toPy() for stmt in self.function_definitions]

class FuncDefinition(VdmslNode):
    """ 関数定義 """
    _fields = ('function_definition',)

    def __init__(self, function_definition, lineno, lexpos):
        self.function_definition = function_definition
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

    def toPy(self):
        return self.function_definition.toPy()

class ExpFuncDefinition(VdmslNode):
    """ 陽関数定義 """
    _fields = ('ident1', 'type_variable_list', 'func_type', 'ident2', 'param_list', 
               'func_body', 'pre_expr', 'post_expr', 'measure_expr',)
    
    def __init__(self, ident1, type_variable_list, func_type, ident2, param_list, 
               func_body, pre_expr, post_expr, measure_expr, lineno, lexpos):
        self.ident1 = ident1
        self.type_variable_list = type_variable_list
        self.func_type = func_type
        self.ident2 = ident2
        self.param_list = param_list
        self.func_body = func_body
        self.pre_expr = pre_expr
        self.post_expr = post_expr
        self.measure_expr = measure_expr
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
    
    def toPy(self):
        func_name = self.ident1
        func_args = pyast.arguments([pyast.Name(e.ptn_id, pyast.Load()) for e in self.param_list[0].pattern_list.patterns], None, [], [], None, [])
        func_body = [pyast.Return(self.func_body.expression.toPy())]
        decorator_list = []
        returns = None
        return pyast.FunctionDef(func_name, func_args, func_body, decorator_list, returns)

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

    def toPy(self):
        name = self.ident
        args = self.param_type.toPy()
        body = [pyast.Pass()]
        return pyast.FunctionDef(name, args, body, [], None)

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

    def toPy(self):
        return self.pattern_type_pair_list.toPy()

class PatternTypePairList(VdmslNode):
    """ パターン型ペアリスト """
    _fields = ('pattern_type_pairs',)

    def __init__(self, pattern_type_pairs, lineno, lexpos):
        self.pattern_type_pairs = pattern_type_pairs
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
    
    def toPy(self):
        arg_list = []
        for ptn_pair in self.pattern_type_pairs:
            type = ptn_pair.type
            ptn_list = ptn_pair.pattern_list
            arg_list += [ pyast.arg(ptn.toPy().id, type.toPy()) for ptn in ptn_list.patterns ]
        return pyast.arguments(arg_list, None, [], [], None, [])

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
class Statement(VdmslNode):
    """ 文 """
    _fields = ('body',)

    def __init__(self, body, lineno, lexpos):
        self.body = body
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
    
    def toPy(self):
        stmts = self.body.toPy()
        return stmts

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
    _fields =('dcl_stmts', 'statements',)

    def __init__(self, dcl_stmts, statements, lineno, lexpos):
        self.dcl_stmts = dcl_stmts
        self.statements = statements
        self.__setattr__('lineno', lineno) 
        self.__setattr__('lexpos', lexpos)
    
    def toPy(self):
        dcl_stmts = []
        for dcl_stmt in self.dcl_stmts:
            dcl_stmts += dcl_stmt.toPy()
        stmts = []
        for stmt in self.statements:
            stmts += stmt.toPy()
        return dcl_stmts + stmts

class DclStatement(VdmslNode):
    """ dcl文 """
    _fields = ('assign_definitions',)

    def __init__(self, assign_definitions, lineno, lexpos):
        self.assign_definitions = assign_definitions
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
    
    def toPy(self):
        return [ stmt.toPy() for stmt in self.assign_definitions ]

class AssignDefinition(VdmslNode):
    """ 代入定義 """
    _fields = ('ident', 'type', 'expr',)

    def __init__(self, ident, type, expr, lineno, lexpos):
        self.ident = ident
        self.type = type
        self.expr = expr
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
    
    def toPy(self):
        target = pyast.Name(self.ident, pyast.Store())
        annotation = pyast.Name(self.type.toPy(), pyast.Load())
        value = self.expr.toPy()
        simple = 1
        return pyast.AnnAssign(target, annotation, value, simple)

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
    
    def toPy(self):
        targets = [self.status_indicator.toPy()]
        value = self.expr.toPy()
        return [pyast.Assign(targets, value)]

class MultiAssignStatement(VdmslNode):
    """ 多重代入文 """
    _fields = ('assign_stmts',)

    def __init__(self, assign_stmts, lineno, lexpos):
        self.assign_stmts = assign_stmts
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
    
    def toPy(self):
        return [stmt.toPy()[0] for stmt in self.assign_stmts]

class StatusIndicator(VdmslNode):
    """ 状態指示子 """
    _fields = ('indicator',)

    def __init__(self, indicator, lineno, lexpos):
        self.indicator = indicator
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

class ItemReference(VdmslNode):
    """ 項目参照 """
    _fields = ('status_indicator', 'ident',)

    def __init__(self, status_indicator, ident, lineno, lexpos):
        self.status_indicator = status_indicator
        self.ident = ident
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
    
    def toPy(self):
        value = self.status_indicator.toPy()
        attr = self.ident
        return pyast.Attribute(value, attr, pyast.Load())

class MapOrColReference(VdmslNode):
    """ 写像参照または列参照 """
    _fields = ('status_indicator', 'expr',)

    def __init__(self, status_indicator, expr, lineno, lexpos):
        self.status_indicator = status_indicator
        self.expr = expr
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
    
    def toPy(self):
        value = self.status_indicator.toPy()
        slice = pyast.Index(self.expr.toPy())
        return pyast.Subscript(value, slice, pyast.Load())


# 条件文
class IfStatement(VdmslNode):
    """ if文 """
    _fields = ('cond', 'body', 'elseif_stmts', 'else_stmt',)

    def __init__(self, cond, body, elseif_stmts, else_stmt, lineno, lexpos):
        self.cond = cond
        self.body = body
        self.elseif_stmts = elseif_stmts
        self.else_stmt = else_stmt
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
    
    def toPy(self):
        el = self.else_stmt
        def make_orelse_stmt(elifs):
            if elifs == []:
                return el.toPy()
            elif len(elifs) == 1:
                return pyast.If(elifs[0].cond.toPy(), elifs[0].body.toPy(), el.toPy())
            else:
                return pyast.If(elifs[0].cond.toPy(), elifs[0].body.toPy(), [make_orelse_stmt(elifs[1:])])

        return [pyast.If(self.cond.toPy(), self.body.toPy(), [make_orelse_stmt(self.elseif_stmts)])]

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

    def __init__(self, cond, case_stmt_options, other_stmt, lineno, lexpos):
        self.cond = cond
        self.case_stmt_options = case_stmt_options
        self.other_stmt = other_stmt
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
    
    def toPy(self):
        cond = self.cond.toPy()
        ops = [pyast.Eq()]

        def make_test_expr(comparators):
            return pyast.Compare(cond, ops, comparators.toPy())

        def convert_cases_to_if_stmt(cgs):
            test_expr = make_test_expr(cgs[0].pattern_list)
            body_stmts = cgs[0].statement.toPy()
            if len(cgs) == 1:
                if self.other_stmt == []:
                    return [pyast.If(test_expr, body_stmts, [])]
                else:
                    return [pyast.If(test_expr, body_stmts, self.other_stmt.toPy())]
            else:
                return pyast.If(test_expr, body_stmts, convert_cases_to_if_stmt(cgs[1:]))

        return [convert_cases_to_if_stmt(self.case_stmt_options)]

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
    
    def toPy(self):
        target = self.pattern_binding.toPy()
        iter_expr = self.expr.toPy()
        stmt_body = self.body.toPy()
        return [pyast.For(target, iter_expr, stmt_body, [])]

class SetForStatement(VdmslNode):
    """ 集合forループ """
    _fields = ('pattern', 'expr', 'body',)

    def __init__(self, pattern, expr, body, lineno, lexpos):
        self.pattern = pattern
        self.expr = expr
        self.body = body
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
    
    def toPy(self):
        target = self.pattern.toPy()
        iter_expr = self.expr.toPy()
        stmt_body = self.body.toPy()
        return [pyast.For(target, iter_expr, stmt_body, [])]

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

    def toPy(self):

        def set_iter_args(s, e, step):
            """ range の引数設定 """
            if step == None:
                return [s.toPy(), e.toPy()]
            else: 
                return [s.toPy(), e.toPy(), step.toPy()]

        ctx_load = pyast.Load()
        target = pyast.Name(self.ident, ctx_load)
        iter_args = set_iter_args(self.expr, self.to_expr, self.by_expr)
        iter_expr = pyast.Call(pyast.Name('range', ctx_load), iter_args, [])
        stmt_body = [pyast.Expr(self.body.toPy())]
        return [pyast.For(target, iter_expr, stmt_body, [])]

# while ループ文
class WhileStatement(VdmslNode):
    """ whileループ """
    _fields = ('cond', 'body',)

    def __init__(self, cond, body, lineno, lexpos):
        self.cond = cond
        self.body = body
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)

    def toPy(self):
        test_expr = self.cond.toPy()
        body_stmts = [pyast.Expr(self.body.toPy())]
        return [pyast.While(test_expr, body_stmts, [])]

# 非決定文
class NonDeterminationStatement(VdmslNode):
    """ 非決定文 """
    _fields = ('statements',)

    def __init__(self, statements, lineno, lexpos):
        self.statements = statements
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
    
    def toPy(self):
        stmts = []
        for stmt in self.statements:
            stmts += stmt.toPy()
        return stmts
        
# call文
class CallStatement(VdmslNode):
    """ call文 """
    _fields = ('opename', 'expr_list',)

    def __init__(self, opename, expr_list, lineno, lexpos):
        self.opename = opename
        self.expr_list = expr_list
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
    
    def toPy(self):
        ctx_load = pyast.Load()
        opname = self.opename
        args = [ expr.toPy() for expr in self.expr_list ]
        return [pyast.Expr(pyast.Call(opname, args, []))]

# return文
class ReturnStatement(VdmslNode):
    """ return文 """
    _fields = ('expr',)

    def __init__(self, expr, lineno, lexpos):
        self.expr = expr
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
    
    def toPy(self):
        if self.expr != None:
            return [pyast.Return(self.expr.toPy())]
        else:
            return [pyast.Return(None)]

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
    
    def toPy(self):
        if self.body == None:
            return [pyast.Raise(None, None)]
        else:
            return [pyast.Raise(self.body.toPy(), None)]

# error文
class Error(VdmslNode):
    """ error文 """
    _fields = ()
    
    def __init__(self, lineno, lexpos):
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
    
    def toPy(self):
        return [pyast.Raise(None, None)]

# 恒等文
class Skip(VdmslNode):
    """ 恒等文 """
    _fields = ()

    def __init__(self, lineno, lexpos):
        self.__setattr__('lineno', lineno)
        self.__setattr__('lexpos', lexpos)
    
    def toPy(self):
        return pyast.Pass()

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


    



    
