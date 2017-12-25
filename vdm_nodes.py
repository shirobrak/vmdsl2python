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

class Expression(VdmslNode):
    """ 式 """
    _field = ('value',)

    def __init__(self, value, lineno, lexpos):
        self.value = value
        self.lineno = lineno
        self.lexpos = lexpos

class BracketExpression(VdmslNode):
    """ 括弧式 """
    _field = ('body',)

    def __init__(self, body, lineno, lexpos):
        self.body = body
        self.lineno = lineno
        self.lexpos = lexpos

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
 
class DefExpression(VdmslNode):
    """ def式 """
    _field = ('pattern_binding', 'body',)

    def __init__(self, pattern_binding, body, lineno, lexpos):
        self.pattern_binding = pattern_binding
        self.body = body
        self.lineno = lineno
        self.lexpos = lexpos




# デバッグ用記述
if __name__ == '__main__':
    pass

    



    
