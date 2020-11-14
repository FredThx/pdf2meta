#!/usr/bin/env python
# -*- coding:utf-8 -*

from pdfCS2meta import *
from FUTIL.my_logging import *

my_logging(console_level = DEBUG, logfile_level = INFO, details = True)


parser = pdfCS2meta()

results = parser.parse('q:\\OLFA\\pdf2meta\\out.pdf')
parser.write_metadata()
print(results)
#results = parser.parse('q:\\OLFA\\pdf2meta\\Exemples\\pblive012020072459470.pdf')
#print(results)
#results = parser.parse('q:\\OLFA\\pdf2meta\\Exemples\\pecdea012020070252474.pdf')
#print(results)
