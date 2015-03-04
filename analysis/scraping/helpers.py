'''Helpers for scraping methods.'''

import re
import requests
from logger import log

def decode(strr):
  '''Decodes strings that were scraped from the web. Fixes spacing'''
  strr = strr.strip().strip('\r\n').strip('\n')
  return strr

def get_content(url):
  '''Returns the text content of a webpage, encoded as ASCII.'''
  try:
    text = requests.get(url).text
    text = re.sub(r'&nbsp;', ' ', text)
    text = text.strip().strip('\r\n').strip('\n')
    return text.encode('ascii', 'ignore')
  except Exception as e:
    log.error('Error opening url %s: %s' % (url, e))
    return None
