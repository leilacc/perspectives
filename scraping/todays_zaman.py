from bs4 import BeautifulSoup
import json
import logging
import requests


from logger import log
import news_interface
import news_orgs


from BeautifulSoup import BeautifulSoup
import urllib2
import codecs
import copy
import re
import argparse
import sys
import json
import wget


logging.basicConfig(filename='todays_zaman.log', level=logging.WARNING)

class TODAYSZAMAN(news_interface.NewsOrg):
  '''Methods for interacting with the Todays Zaman website.'''

  def get_article(self, url):
    '''Implementation for getting an article from Todays Zaman
                                                                                                                                                                                                                                                                                                                            
    url: A URL in the www.todayszaman.* domain.                                                                                                                                                                                                                                                                                     
                                                                                                                                                                                                                                                                                                                            
    Returns: The Article representing the article at that url.                                                                                                                                                                                                                                                              
    '''
    soup = BeautifulSoup(requests.get(url).text)
    a = soup.find("title")
    headline = a.text.encode('ascii', 'ignore')
    paragraphs = soup.find("div", {"id": "newsText"})
    article = paragraphs.findAll("p")
    body = ' '.join([p.text.encode('ascii', 'ignore') for p in article])
    log.info(headline)
    log.info(body)
    return news_interface.Article(headline, body, url, news_orgs.TODAYSZAMAN)

  def get_query_results(self, query):
    '''Implementation for keyword searches from Todays Zaman.                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                                                                            
    query: A URL-encoded string.                                                                                                                                                                                                                                                                                            

    Returns: A list of the top Articles returned by the query search.                                                                                                                                                                                                                                                       
    '''

    res = requests.get(
      'http://www.todayszaman.com/search.action;jsessionid=bGucr4qN9Lo-TclLpIykGYg1?archiveDate=&words=%s'
      % (query))
    soup = BeautifulSoup(res.text)
    articles = soup.findAll("div", {"class": "pageSearchMainContentText"})

    article_urls = [article.a.get('href') for article in articles]


    top_articles = []
    for url in article_urls[0:news_interface.NUM_ARTICLES]:
      top_articles.append(self.get_article(url))

    return top_articles

