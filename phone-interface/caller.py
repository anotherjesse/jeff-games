#!/usr/bin/python
"""
Foo bar
"""

import os, sys, shutil

TMP_FOLDER = '/tmp'

def generate_call():
  dial_string = """

  """
  f = open('%s/dialme' % (TMP_FOLDER,) , 'w+')
  print >> f, dial_string
  f.close()
  os.fchmod(f, 0777)
  shutil.move(
  


if __name__ == '__main':
  generate_call()
  exit(0)

