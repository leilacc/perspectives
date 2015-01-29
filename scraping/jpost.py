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



logging.basicConfig(filename='jpost.log', level=logging.WARNING)

class JPOST(news_interface.NewsOrg):
  '''Methods for interacting with the JPOST website.'''

  def get_article(self, url):
    '''Implementation for getting an article from JPost.
                                                                                                                                                                                                                                                                                                                            
    url: A URL in the www.jpost.* domain.                                                                                                                                                                                                                                                                                     
                                                                                                                                                                                                                                                                                                                            
    Returns: The Article representing the article at that url.                                                                                                                                                                                                                                                              
    '''

    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)
    a = soup.find("title")
    headline = a.text
    paragraphs = soup.find("div", {"class": "article-text"})
    article = paragraphs.find("p")

    body = article.text.encode('ascii', 'ignore')


    log.info(headline)
    log.info(body)
    return news_interface.Article(headline, body, url, news_orgs.JPOST)

  def get_query_results(self, query):
    '''Implementation for keyword searches from JPOST.                                                                                                                       
                                                                                                                                                 
    query: A URL-encoded string. 
    
    Returns: A list of the top Articles returned by the query search.                                                                                                           
                                                                                                                                            
    '''

   browser = webdriver.Firefox()
   browser.get("http://www.jpost.com/Search?search" + query)
   html_source = browser.page_source
   soup = BeautifulSoup(html_source)
   articles = soup.findAll('li', attrs={'class': "search-item"})

   article_urls = [article.a.get('href') for article in articles]
   top_articles = []
   for url in article_urls[0:news_interface.NUM_ARTICLES]:
     top_articles.append(self.get_article(url))

   return top_articles




