'''Helpers for scraping methods.'''

import re
import requests
from logger import log

def decode(strr):
  '''Decodes strings that were scraped from the web.'''
  strr = re.sub(r'&nbsp;', ' ', strr)
  strr = strr.strip().strip('\r\n').strip('\n')
  return strr

def get_content(url):
  '''Returns the text content of a webpage, encoded as ASCII.'''
  try:
    return requests.get(url).text.encode('ascii', 'ignore')
  except Exception as e:
    log.error('Error opening url %s: %s' % (url, e))
    return None
