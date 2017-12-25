# -*- coding: utf-8 -*-

class VdmslNode(object):
    """ VDM-SLのASTノード基底クラス """
    _field = ()
    _attributes = ('lineno', 'col_offset')

class NameBase(VdmslNode):
    """ 名称基底クラス """
    _field = ('name')

    def __init__(self, name, lineno, lexpos):
        self.name = name
        self.lineno = lineno
        self.lexpos = lexpos

class Name(NameBase):
    """ 名称クラス """
    pass

class OldName(NameBase):
    """ 旧名称 """
    pass

class SymbolLiteral(NameBase):
    """ 記号リテラル """
    pass



# デバッグ用記述
if __name__ == '__main__':
    pass
    



    
