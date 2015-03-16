'''Helpers for scraping methods.'''

import codecs
import re
import requests
import sys

from . import logger

def decode(strr):
  '''Decodes strings that were scraped from the web. Fixes spacing and quotes'''
  strr = strr.strip().strip('\r\n').strip('\n')
  strr = re.sub(u'\u2018', "'", strr)
  strr = re.sub(u'\u2019', "'", strr)
  strr = re.sub(u'\u201C', '"', strr)
  strr = re.sub(u'\u201d', '"', strr)
  strr = re.sub(u'\u2013', '"', strr)

  if sys.version_info < (3, 0):
    # Python 2
    strr = strr.encode('ascii', 'ignore')

  return strr

def get_content(url):
  '''Returns the text content of a webpage, encoded as ASCII.'''
  try:
    text = requests.get(url).text
    text = re.sub(r'&nbsp;', ' ', text)
    text = text.strip().strip('\r\n').strip('\n')
    return text
  except Exception as e:
    logger.log.error('Error getting content for url %s: %s' % (url, e))
    return None
