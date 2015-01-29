from bs4 import BeautifulSoup
import json
import logging
import requests

from api_keys import api_keys
from logger import log
import news_interface
import news_orgs

import analysis
from BeautifulSoup import BeautifulSoup
import urllib2
import codecs
import copy
import re
import argparse
import sys
import json
import wget
from get_query import get_keyword


logging.basicConfig(filename='zamandaily.log', level=logging.WARNING)

class ZAMANDAILY(news_interface.NewsOrg):
  '''Methods for interacting with the AlJazeera website.'''

  def get_article(self, url):
    '''Implementation for getting an article from Zaman Daily.
                                                                                                                                                                                                                                                                                                                            
    url: A URL in the www.zamandaily.* domain.                                                                                                                                                                                                                                                                                     
                                                                                                                                                                                                                                                                                                                            
    Returns: The Article representing the article at that url.                                                                                                                                                                                                                                                              
    '''
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)
   

    a = soup.find("title")
    headline = a.text
    c = soup.findAll("p")
    body = ""
    for paragraph in c:
        try:
            output +=  paragraph.text.decode("utf-8").replace("\"","'").replace("^M","").replace("\n","").replace("\\","").replace(r'\r','').replace("\r", "").replace("\n", "") + " "
        except UnicodeEncodeError:
            pass

   
    log.info(headline)
    log.info(body)
    return news_interface.Article(headline, body, url, news_orgs.ZAMANDAILY)

  def get_query_results(self, query):
    '''Implementation for keyword searches from Zaman Daily.                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                                                                            
    query: A URL-encoded string.                                                                                                                                                                                                                                                                                            

    Returns: A list of the top Articles returned by the query search.                                                                                                                                                                                                                                                       
    '''
    res = requests.get(
        'http://www.todayszaman.com/search.action;jsessionid=bGucr4qN9Lo-TclLpIykGYg1?archiveDate=&words='
        % (query))
    soup = BeautifulSoup(res.text)
    articles = soup.find_all('pageSearchMainContentTitle')
    article_urls = [article.a.get('href') for article in articles]

   top_articles = []
   for url in article_urls[0:news_interface.NUM_ARTICLES]:
        top_articles.append(self.get_article(url))
  return top_articles


