'''Helpers for scraping methods.'''

import re
import requests
from logger import log

def decode(strr):
  '''Decodes strings that were scraped from the web. Fixes spacing and quotes'''
  strr = strr.strip().strip('\r\n').strip('\n')
  #strr = strr.decode('utf-8')
  strr = re.sub(u'\u2018', "'", strr)
  strr = re.sub(u'\u2019', "'", strr)
  return strr

def get_content(url):
  '''Returns the text content of a webpage, encoded as ASCII.'''
  try:
    text = requests.get(url).text
    text = re.sub(r'&nbsp;', ' ', text)
    text = text.strip().strip('\r\n').strip('\n')
    #text = text.encode('ascii', 'ignore')
    return text
  except Exception as e:
    log.error('Error opening url %s: %s' % (url, e))
    return None
