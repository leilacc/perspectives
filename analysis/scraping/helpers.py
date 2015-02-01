'''Helpers for scraping methods.'''

import re

def decode(strr):
  strr = re.sub(r'&nbsp;', ' ', strr)
  strr = strr.encode('ascii', 'ignore')
  strr = strr.strip().strip('\r\n').strip('\n')
  return strr
