# -*- coding: utf-8 -*-

import math
from itertools import chain,combinations

"""
VDM-SL用の拡張モジュール
"""

# 数値型操作
def floor(value:float):
    """ 底値 """
    return math.floor(value)

def rem(x:int, y:int):
    """ 剰余算 """
    return x - y * ( x // y )

# 集合操作
def dunion(ss:set):
    """ 分配的集合合併 """
    s = set()
    for e in ss:
        if type(e) == frozenset:
            s = s.union(e)     
        else:
            s = s.union({e})
    return s

def dinter(ss:set):
    """ 分配的集合共通部分 """
    s = set()
    for e in ss:
        if type(e) == frozenset:
            s = s.intersection(e)
        else:
            s = s.intersection({e})
    return s

def power(s:set):
    """ 有限べき集合 """
    l = list(s)
    return { frozenset(e) for e in chain.from_iterable(combinations(l, r) for r in range(len(l)+1)) } 

# 列操作
def conc(ll:list):
    """ 分配的列連結 """
    flat_list = []
    for e in ll:
        if type(e) == list:
            flat_list.extend(e)
        else:
            flat_list.append(e)
    return flat_list

# 写像操作
def map_inverse(m:dict):
    """ 逆写像 """
    return { v:k for k,v in m.items() }

def limit_map_dom(m:dict, s:set):
    """ 写像定義域限定 """
    return { k:v for k,v in m.items() for e in s if k == e }

def reduce_map_dom(m:dict, s:set):
    """ 写像定義域削減 """
    m_copy = m.copy()
    for e in s:
        if e in m_copy:
            m.pop(e)
    return m

def limit_map_range(m:dict, s:set):
    """ 写像値域限定 """
    return { k:v for k,v in m.items() for e in s if v == e }

def reduce_map_range(m:dict, s:set):
    """ 写像値域削減 """
    m_copy = m.copy()
    for k,v in m_copy.items():
        for e in s:
            if v == e:
                m.pop(k)
    return m

def map_or_list_update(l, r):
    """ 写像修正または列修正 """
    if type(l) == list:
        for k,v in r.items():
            l[k-1:k] = [v]
        return l
    elif type(l) == dict:
        return l.update(r)
    else:
        print(" map_or_list_update : arg error ")
        return None


# 限量式
def forall(binds, expr):
    """ 全称限量式 """
    pass

def exists(binds, expr):
    """ 存在限量式 """
    pass

def exist1(binds, expr):
    """ 1存在限量式 """
    pass


# デバッグ用記述
if __name__ == '__main__':
    pass
        
