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
from selenium import webdriver



logging.basicConfig(filename='aljazeera.log', level=logging.WARNING)

class ALJAZEERA(news_interface.NewsOrg):
  '''Methods for interacting with the AlJazeera website.'''

  def get_article(self, url):
    '''Implementation for getting an article from AlJazeera.
                                                                                                                                                                                                                                                                                                                            
    url: A URL in the www.aljazeera.* domain.                                                                                                                                                                                                                                                                                     
                                                                                                                                                                                                                                                                                                                            
    Returns: The Article representing the article at that url.                                                                                                                                                                                                                                                              
    '''


  


    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)
    a = soup.find("title")
    headline = a.text

    paragraphs = soup.find("div", {"class": "text section"})
    article = paragraphs.findAll("p")
    body = ' '.join([p.text.encode('ascii', 'ignore') for p in article])
    log.info(headline)
    log.info(body)
    return news_interface.Article(headline, body, url, news_orgs.ALJAZEERA)

  def get_query_results(self, query):
   '''Implementation for keyword searches from BBC.                                                                                                                               
                                                                                                                                         
                                                                                                                                                                                                                                                                                                                            
    query: A URL-encoded string.                                                                                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                                                                                            
    Returns: A list of the top Articles returned by the query search.                                                                                                                                                                                                                                                       
    '''
   
   browser = webdriver.Firefox()
   browser.get("http://america.aljazeera.com/search.html?q=" + query)
   html_source = browser.page_source
   soup = BeautifulSoup(html_source)
   articles = soup.findAll('div', attrs={'class': 'gs-webResult gs-result'})

   article_urls = [article.a.get('href') for article in articles]
   top_articles = []
   for url in article_urls[0:news_interface.NUM_ARTICLES]:
     top_articles.append(self.get_article(url))

   return top_articles


