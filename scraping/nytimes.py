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


logging.basicConfig(filename='nytimes.log', level=logging.WARNING)

class NYTIMES(news_interface.NewsOrg):
  '''Methods for interacting with the AlJazeera website.'''

  def get_article(self, url):
    '''Implementation for getting an article from New York Times.
                                                                                                                                                                                                                                                                                                                            
    url: A URL in the www.nytimes.* domain.                                                                                                                                                                                                                                                                                     
                                                                                                                                                                                                                                                                                                                            
    Returns: The Article representing the article at that url.                                                                                                                                                                                                                                                              
    '''

    response = urllib2.urlopen(url)
    data = json.load(response)
    u = data["response"]["docs"][0]["web_url"]
    headline = data["response"]["docs"][0]["headline"]["main"]
   
    with open("hard_coded_input/nytimes.html") as f:
      content = f.readlines()
    str = ""
    for line in content:
        str+= line + " "
    soup = BeautifulSoup(str)
    output +=  "\"article_text\": \""
    c = soup.findAll("p",{"class":"story-body-text story-content"})
    for paragraph in c:
        try:
            output +=  paragraph.text.decode("utf-8").replace("\"","'") + " "
        except UnicodeEncodeError:
            pass
    output += "\"}\n"
    return output
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)
    a = soup.find("title")
    headline = a.text

    body = ""
    c = soup.findAll("p")
    for paragraph in c:
        try:
            body +=  paragraph.text.decode("utf-8").replace("\"","'").replace("\n","") + " "
        except UnicodeEncodeError:
            pass


    log.info(headline)
    log.info(body)
    return news_interface.Article(headline, body, url, news_orgs.ALJAZEERA)

#  def get_query_results(self, query):
#    '''Implementation for keyword searches from BBC.                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                                                                            
 #   query: A URL-encoded string.                                                                                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                                                                                            
 #   Returns: A list of the top Articles returned by the query search.                                                                                                                                                                                                                                                       
#    '''
 #   res = requests.get(
  #      'http://www.bbc.co.uk/search?q=%s&sa_f=search-serp&filter=news'
  #      % (query))
  #  soup = BeautifulSoup(res.text)
  #  articles = soup.find_all('article')
  #  article_urls = [article.h1.a.get('href') for article in articles]

   # top_articles = []
  #  for url in article_urls[0:news_interface.NUM_ARTICLES]:
#        top_articles.append(self.get_article(url))
  #  return top_articles


