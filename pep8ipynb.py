# coding: utf-8

import sys
import io
import json
import logging
import pep8


def load_code_from_ipynb(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    codes = dict([(x['execution_count'], x['source']) for x in data['cells']
                  if x['cell_type'] == 'code' and x['execution_count']])
    return codes


def _check_pep8_from_file(filename):
    codes = load_code_from_ipynb(filename)
    return [(i, check_pep8_from_lines(codes[i])) for i in codes]


def check_pep8_from_file(filename):
    for result in _check_pep8_from_file(filename):
        num, msg = result
        print('In [{}]: '.format(num))
        for x in msg:
            print(x)


def check_pep8_from_lines(lines):
    logger = logging.getLogger('pep8')
    logger.setLevel(logging.INFO)
    # output is written to stdout
    # remember and replace
    old_stdout = sys.stdout
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    pep8.Checker(lines=lines).check_all()
    stdout = sys.stdout.getvalue().splitlines()
    # restore
    sys.stdout = old_stdout
    return stdout


if __name__ == '__main__':
    check_pep8_from_file(sys.argv[1])
