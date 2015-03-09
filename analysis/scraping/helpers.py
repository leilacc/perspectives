'''Helpers for scraping methods.'''

import codecs
import re
import requests
from . import logger

def decode(strr):
  '''Decodes strings that were scraped from the web. Fixes spacing and quotes'''
  strr = strr.strip().strip('\r\n').strip('\n')
  #strr = strr.decode('utf-8')
  strr = re.sub(u'\u2018', "'", strr)
  strr = re.sub(u'\u2019', "'", strr)
  return strr

def get_content(url):
  '''Returns the text content of a webpage, encoded as ASCII.'''
  #try:
  text = requests.get(url).text
  text = re.sub(r'&nbsp;', ' ', text)
  text = text.strip().strip('\r\n').strip('\n')
  text = text.encode('utf-8')
  #text = re.sub(u'\u2018', "'", text)
  #text = re.sub(u'\u2019', "'", text)
  #text = text.encode('ascii', 'ignore')
  return text
  '''
  except Exception as e:
    log.error('Error getting content for url %s: %s' % (url, e))
    return None
    '''
