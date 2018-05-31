#!/usr/bin/env python

from zipfile import ZipFile
import json
import glob
import os

replays = glob.glob('*.wotbreplay')
print_header = 1

print "<table border=1>"

for replay in replays:

  source = ZipFile(replay, 'r')

  for file in source.filelist:
    if file.filename == 'meta.json':
      meta = source.extract('meta.json')
      meta_fh = open(meta,'r')
      data = json.load(meta_fh)
      meta_fh.close()
      os.remove('meta.json')
      data.update({u'filename': source.filename})

      if print_header == 1:
        print "<tr>"
        for key,value in sorted(data.iteritems()):
          print "<th>"+ str(key) +"</th>"
          print_header = 0
        print "</tr>"

      print "<tr>"
      for key,value in sorted(data.iteritems()):
        print "<td>"+ str(value) +"</td>"
      print "</tr>"

print "</table>"
