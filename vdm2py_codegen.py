# -*- coding: utf-8 -*-

import sys
import os.path
import logging
from vdmparser import parser
import astor
import re

COMMENT = re.compile(r"--.*|\/\*[\s\S]*?\*\/.*")


if __name__ == '__main__':

    log = logging.getLogger()
    fpath = sys.argv[1]
    fname = fpath.replace("input/","")

    with open(fpath, 'r') as fp:

        txt = fp.read()
        # コメントアウトを削除
        ret = re.sub(COMMENT, "", txt)

        result = parser.parse(ret, debug=log)
        code = astor.to_source(result.toPy(), ' '*4, False)

        # VDM-SL AST生成
        with open('./output/'+os.path.splitext(fname)[0]+'.vdm_ast', 'w') as output:
            output.write(result.dumps())

        # Pythonコード生成
        with open('./output/'+os.path.splitext(fname)[0]+'.py', 'w') as output:
            output.write(code)

