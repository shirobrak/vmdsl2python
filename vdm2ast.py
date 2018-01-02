# -*- coding: utf-8 -*-

from vdmparser import parser
import sys
import os.path
import logging


if __name__ == '__main__':

    log = logging.getLogger()
    fname = sys.argv[1]

    with open(fname, 'r') as fp:
        txt = fp.read()
        res = parser.parse(txt, debug=log)
        with open('ast_'+os.path.splitext(fname)[0]+'.txt', 'w') as output:
            output.write(res.dumps())
