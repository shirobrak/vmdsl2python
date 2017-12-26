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
    _fields = ('binding', 'option_expr', 'body',)

    def __init__(self, binding, option_expr, body, lineno, lexpos):
        self.binding = binding
        self.option_expr = option_expr
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

# 値定義
class ValueDefinitionGroup(VdmslNode):
    """ 値定義群 """
    _fields = ('value_definitions')

    def __init__(self, value_definitions, lineno, lexpos):
        self.value_definitions = value_definitions
        self.lineno = lineno
        self.lexpos = lexpos

class ValueDefinition(VdmslNode):
    """ 値定義 """
    _fields = ('pattern', 'type', 'expr',)

    def __init__(self, pattern, type, expr, lineno, lexpos):
        self.pattern = pattern
        self.type = type
        self.lineno
        self.lexpos

# 状態定義
class StateDefinition(VdmslNode):
    """ 状態定義 """
    _fields = ('ident', 'item_list', 'inv_cond', 'init',)

    def __init__(self, ident, item_list, inv_cond, init, lineno, lexpos):
        self.ident = ident
        self.item_list = item_list
        self.inv_cond = inv_cond
        self.init = init
        self.lineno = lineno
        self.lexpos = lexpos

class InvCondition(VdmslNode):
    """ 不変条件 """
    _fields = ('inv_condition_init_function',)

    def __init__(self, inv_condition_init_function, lineno, lexpos):
        self.inv_condition_init_function = inv_condition_init_function
        self.lineno = lineno
        self.lexpos = lexpos

class Initialization(VdmslNode):
    """ 初期化 """
    _fields = ('inv_condition_init_function',)

    def __init__(self, inv_condition_init_function, lineno, lexpos):
        self.inv_condition_init_function = inv_condition_init_function
        self.lineno = lineno
        self.lexpos = lexpos

class InvCondInitFunc(VdmslNode):
    """ 不変条件初期関数 """
    _fields = ('pattern', 'expr',)

    def __init__(self, pattern, expr, lineno, lexpos):
        self.pattern = pattern
        self.expr = expr
        self.lineno = lineno
        self.lexpos = lexpos

# 操作定義
class OpeDefinitionGroup(VdmslNode):
    """ 操作定義群 """
    _fields = ('operation_definitions',)

    def __init__(self, operation_definitions, lineno, lexpos):
        self.operation_definitions = operation_definitions
        self.lineno = lineno
        self.lexpos = lexpos

class OpeDefinition(VdmslNode):
    """ 操作定義 """
    _fields = ('operation_definition',)

    def __init__(self, operation_definition, lineno, lexpos):
        self.operation_definition = operation_definition
        self.lineno = lineno
        self.lexpos = lexpos

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
        self.lineno = lineno
        self.lexpos = lexpos

class ImpOpeDefinition(VdmslNode):
    """ 陰操作定義 """
    _fields = ('param_ident', 'param_type', 'ident_type_pair_list', 'imp_body',)

    def __init__(self, param_ident, param_type, 
                 ident_type_pair_list, imp_body, lineno, lexpos):
        self.param_ident = param_ident
        self.param_type = param_type
        self.ident_type_pair_list = ident_type_pair_list
        self.imp_body = imp_body
        self.lineno = lineno
        self.lexpos = lexpos

class ImpOpeBody(VdmslNode):
    """ 陰操作本体 """
    _fields = ('ext_sec', 'pre_expr', 'post_expr', 'except',)

    def __init__(self, ext_sec, pre_expr, post_expr, exception, lineno, lexpos):
        self.ext_sec = ext_sec
        self.pre_expr = pre_expr
        self.post_expr = post_expr
        self.exception = exception
        self.lineno = lineno
        self.lexpos = lexpos

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
        self.lineno = lineno
        self.lexpos = lexpos

class OperationType(VdmslNode):
    """ 操作型 """
    _fields = ('left', 'right',)

    def __init__(self, left, right, lineno, lexpos):
        self.left = left
        self.right = right
        self.lineno = lineno
        self.lexpos = lexpos

class AnyType(VdmslNode):
    """ 任意の型 """
    _fields = ('type',)

    def __init__(self, type, lineno, lexpos):
        self.type = type
        self.lineno = lineno
        self.lexpos = lexpos

class ParamGroup(VdmslNode):
    """ パラメータ群 """
    _fields = ('pattern_list',)

    def __init__(self, pattern_list, lineno, lexpos):
        self.pattern_list = pattern_list
        self.lineno = lineno
        self.lexpos = lexpos


class PatternList(VdmslNode):
    """ パターンリスト """
    _fields = ('patterns',)

    def __init__(self, patterns, lineno, lexpos):
        self.patterns = patterns
        self.lineno = lineno
        self.lexpos = lexpos

class OperationBody(VdmslNode):
    """ 操作本体 """
    _fields = ('statement',)

    def __init__(self, statement, lineno, lexpos):
        self.statement = statement
        self.lineno = lineno
        self.lexpos = lexpos

class ExtSection(VdmslNode):
    """ 外部節 """
    _fields = ('var_infos',)

    def __init__(self, var_infos, lineno, lexpos):
        self.var_infos = var_infos
        self.lineno = lineno
        self.lexpos = lexpos

class VarInfo(VdmslNode):
    """ var 情報 """
    _fields = ('mode', 'name_list', 'type',)

    def __init__(self, mode, name_list, type, lineno, lexpos):
        self.mode = mode
        self.name_list = name_list
        self.type = type
        self.lineno = lineno
        self.lexpos = lexpos

class NameList(VdmslNode):
    """ 名称リスト """
    _fields = ('idents',)

    def __init__(self, idents, lineno, lexpos):
        self.idents = idents
        self.lineno = lineno
        self.lexpos = lexpos

class Exception(VdmslNode):
    """ 例外 """
    _fields = ('err_list',)

    def __init__(self, err_list, lineno, lexpos):
        self.err_list = err_list
        self.lineno = lineno
        self.lexpos = lexpos

class ErrorList(VdmslNode):
    """ エラーリスト """
    _fields = ('errors',)

    def __init__(self, errors, lineno, lexpos):
        self.errors = errors
        self.lineno = lineno
        self.lexpos = lexpos

class Error(VdmslNode):
    """ エラー """
    _fields = ('ident', 'left', 'right',)

    def __init__(self, ident, left, right, lineno, lexpos):
        self.ident = ident
        self.left = left
        self.right = right
        self.lineno = lineno
        self.lexpos = lexpos

# 関数定義
class FuncDefinitionGroup(VdmslNode):
    """ 関数定義群 """
    _fields = ('function_definitions',)

    def __init__(self, function_definitions, lineno, lexpos):
        self.function_definitions = function_definitions
        self.lineno = lineno
        self.lexpos = lexpos

class FuncDefinition(VdmslNode):
    """ 関数定義 """
    _fields = ('function_definition',)

    def __init__(self, function_definition, lineno, lexpos):
        self.function_definition = function_definition
        self.lineno = lineno
        self.lexpos = lexpos

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
        self.lineno = lineno
        self.lexpos = lexpos

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
        self.lineno = lineno
        self.lexpos = lexpos

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
        self.lineno = lineno
        self.lexpos = lexpos

class TypeVariableList(VdmslNode):
    """ 型変数リスト """
    _fields = ('type_variable_idents',)

    def __init__(self, type_variable_idents, lineno, lexpos):
        self.type_variable_idents = type_variable_idents
        self.lineno = lineno
        self.lexpos = lexpos

class IdentTypePairList(VdmslNode):
    """ 識別子型ペアリスト """
    _fields = ('ident_type_pairs',)

    def __init__(self, ident_type_pairs, lineno, lexpos):
        self.ident_type_pairs = ident_type_pairs
        self.lineno = lineno
        self.lexpos = lexpos

class IdentTypePair(VdmslNode):
    """ 識別子ペア """
    _fields = ('ident', 'type',)

    def __init__(self, ident, type, lineno, lexpos):
        self.ident = ident
        self.type = type
        self.lineno = lineno
        self.lexpos = lexpos

class ParamType(VdmslNode):
    """ パラメーター型 """
    _fields = ('pattern_type_pair_list',)

    def __init__(self, pattern_type_pair_list, lineno, lexpos):
        self.pattern_type_pair_list = pattern_type_pair_list
        self.lineno = lineno
        self.lexpos = lexpos

class PatternTypePairList(VdmslNode):
    """ パターン型ペアリスト """
    _fields = ('pattern_type_pairs',)

    def __init__(self, pattern_type_pairs, lineno, lexpos):
        self.pattern_type_pairs = pattern_type_pairs
        self.lineno = lineno
        self.lexpos = lexpos

class PatternTypePair(VdmslNode):
    """ パターン型ペア """
    _fields = ('pattern_list', 'type',)

    def __init__(self, pattern_list, type, lineno, lexpos):
        self.pattern_list = pattern_list
        self.type = type
        self.lineno = lineno
        self.lexpos = lexpos

class FuncionType(VdmslNode):
    """ 関数型 """
    _fields = ('function_type',)

    def __init__(self, function_type, lineno, lexpos):
        self.function_type = function_type
        self.lineno = lineno
        self.lexpos = lexpos

class PartialFunctionType(VdmslNode):
    """ 部分関数型 """
    _fields = ('any_type', 'type',)

    def __init__(self, any_type, type, lineno, lexpos):
        self.any_type = any_type
        self.type = type
        self.lineno = lineno
        self.lexpos = lexpos

class FunnFuntionType(VdmslNode):
    """ 全関数型 """
    _fields = ('any_type', 'type',)

    def __init__(self, any_type, type, lineno, lexpos):
        self.any_type = any_type
        self.type = type
        self.lineno = lineno
        self.lexpos = lexpos

class FunctionBody(VdmslNode):
    """ 関数本体 """
    _fields = ('expression',)

    def __init__(self, expressions, lineno, lexpos):
        self.expression = expression
        self.lineno = lineno
        self.lexpos = lexpos

# 文
class Statements(VdmslNode):
    """ 文 """
    _fields = ('statement',)

    def __init__(self, statement, lineno, lexpos):
        self.statement = statement
        self.lineno = lineno
        self.lexpos = lexpos

# let 文
class LetStatement(VdmslNode):
    """ let文 """
    _fields = ('local_definitions', 'body',)

    def __init__(self, local_definitions, body, lineno, lexpos):
        self.local_definitions = local_definitions
        self.body = body
        self.lineno = lineno
        self.lexpos = lexpos

class LetBeStatement(VdmslNode):
    """ let be 文 """
    _fields = ('binding', 'option_expr', 'body',)

    def __init__(self, binding, option_expr, body, lineno, lexpos):
        self.binding = binding
        self.option_expr = option_expr
        self.body = body
        self.lineno = lineno 
        self.lexpos = lexpos

class LocalDefinitions(VdmslNode):
    """ ローカル定義 """
    _fields = ('definition',)

    def __init__(self, definition, lineno, lexpos):
        self.definition = definition
        self.lineno = lineno
        self.lexpos

# def 文

class DefStatement(VdmslNode):
    """ def文 """
    _fields = ('equal_definitions', 'body',)

    def __init__(self, equal_definitions, body, lineno, lexpos):
        self.equal_definitions = equal_definitions
        self.body = body
        self.lineno = lineno 
        self.lexpos = lexpos

class EqualDefinition(VdmslNode):
    """ 相等定義 """
    _fields = ('pattern_binding', 'expr',)

    def __init__(self, pattern_binding, expr, lineno, lexpos):
        self.pattern_binding = pattern_binding
        self.expr = expr
        self.lineno = lineno
        self.lexpos = lexpos

# ブロック文
class BlockStatement(VdmslNode):
    """ ブロック文 """
    _fields =('dcl_stmt', 'statements',)

    def __init__(self, dcl_stmt, statement, lineno, lexpos):
        self.dcl_stmt = dcl_stmt
        self.statement = statement
        self.lineno = lineno 
        self.lexpos = lexpos

class DclStatement(VdmslNode):
    """ dcl文 """
    _fields = ('assign_definitions',)

    def __init__(self, assign_definitions, lineno, lexpos):
        self.assign_definitions = assign_definitions
        self.lineno = lineno
        self.lexpos = lexpos

class AssignDefinition(VdmslNode):
    """ 代入定義 """
    _fields = ('ident', 'type', 'expr',)

    def __init__(self, ident, type, expr, lineno, lexpos):
        self.ident = ident
        self.type = type
        self.expr = expr
        self.lineno = lineno
        self.lexpos = lexpos

# 代入文
class GeneralAssignStatement(VdmslNode):
    """ 一般代入文 """
    _fields = ('statement',)

    def __init__(self, statement, lineno, lexpos):
        self.statement = statement
        self.lineno = lineno
        self.lexpos = lexpos

class AssignStatement(VdmslNode):
    """ 代入文 """
    _fields = ('status_indicator', 'expr',)

    def __init__(self, status_indicator, expr, lineno, lexpos):
        self.status_indicator = status_indicator
        self.expr = expr
        self.lineno = lineno
        self.lexpos = lexpos

class StatusIndicator(VdmslNode):
    """ 状態指示子 """
    _fields = ('indicator',)

    def __init__(self, indicator, lineno, lexpos):
        self.indicator = indicator
        self.indicator = lineno
        self.lexpos = lexpos

class ItemReference(VdmslNode):
    """ 項目参照 """
    _fields = ('status_indicator', 'ident',)

    def __init__(self, status_indicator, ident, lineno, lexpos):
        self.status_indicator = status_indicator
        self.ident = ident
        self.lineno = lineno
        self.lexpos = lexpos

class MapOrColReference(VdmslNode):
    """ 写像参照または列参照 """
    _fields = ('status_indicator', 'expr',)

    def __init__(self, status_indicator, expr, lineno, lexpos):
        self.status_indicator = status_indicator
        self.expr = expr
        self.lineno = lineno
        self.lexpos = lexpos

class MultiAssignStatement(VdmslNode):
    """ 多重代入文 """
    _fields = ('assign_stmts',)

    def __init__(self, assign_stmts, lineno, lexpos):
        self.assign_stmts = assign_stmts
        self.lineno = lineno
        self.lexpos = lexpos

# 条件文
class IfStatement(VdmslNode):
    """ if文 """
    _fields = ('cond', 'body', 'elseif_stmts', 'else_stmt',)

    def __init__(self, cond, then, elseif_stmts, else_stmt, lineno, lexpos):
        self.cond = cond
        self.then = then
        self.elseif_stmts = elseif_stmts
        self.else_stmt = else_stmt
        self.lineno = lineno
        self.lexpos = lexpos
    
class ElseIfStatement(VdmslNode):
    """ elseif文 """
    _fields = ('cond', 'body',)

    def __init__(self, cond, body, lineno, lexpos):
        self.cond = cond
        self.body = body
        self.lineno = lineno
        self.lexpos = lexpos

class CasesStatement(VdmslNode):
    """ cases文 """
    _fields = ('cond', 'case_stmt_options', 'other_stmt',)

    def __init__(self, cond, case_stmt_options, other, lineno, lexpos):
        self.cond = cond
        self.case_stmt_options = case_stmt_options
        self.other_stmt = other_stmt
        self.lineno = lineno
        self.lexpos = lexpos

class CaseStmtOption(VdmslNode):
    """ case文選択肢 """
    _fields = ('pattern_list', 'statement',)

    def __init__(self, pattern_list, statement, lineno, lexpos):
        self.pattern_list = pattern_list
        self.statement = statement
        self.lineno = lineno
        self.lexpos = lexpos

# forループ文
class ColForStatement(VdmslNode):
    """ 列forループ """
    _fields = ('pattern_binding', 'expr', 'body',)

    def __init__(self, pattern_binding, expr, body, lineno, lexpos):
        self.pattern_binding = pattern_binding
        self.expr = expr
        self.body = body
        self.lineno = lineno 
        self.lexpos = lexpos

class SetForStatement(VdmslNode):
    """ 集合forループ """
    _fields = ('pattern', 'expr', 'body',)

    def __init__(self, pattern, expr, body, lineno, lexpos):
        self.pattern = pattern
        self.expr = expr
        self.body = body
        self.lineno = lineno
        self.lexpos = lexpos

class IndexForStatement(VdmslNode):
    """ 索引forループ """
    _fields = ('ident', 'expr', 'to_expr', 'by_expr', 'body',)

    def __init__(self, ident, expr, to_expr, by_expr, body, lineno, lexpos):
        self.ident = ident
        self.expr = expr
        self.to_expr = to_expr
        self.by_expr = by_expr
        self.body = body
        self.lineno = lineno
        self.lexpos = lexpos




# デバッグ用記述
if __name__ == '__main__':
    pass

    



    
