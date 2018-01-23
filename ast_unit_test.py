# coding:utf-8

import sys
import os.path
import logging
from vdmparser import parser

if __name__ == '__main__':

    log = logging.getLogger()
    fname = sys.argv[1]

    with open(fname, 'r') as fp:
        txt = fp.read()
    
        result = parser.parse(txt, debug=log)
        print(result)

        # VDM-SL AST生成
        with open('./output/'+os.path.splitext(fname)[0]+'.vdm_ast', 'w') as output:
            output.write(result.dumps())        