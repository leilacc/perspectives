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
from selenium import webdriver


logging.basicConfig(filename='times_of_israel.log', level=logging.WARNING)

class TIMES_OF_ISRAEL(news_interface.NewsOrg):
  '''Methods for interacting with the Times of Israel website.'''

  def get_article(self, url):
    '''Implementation for getting an article from Times of Israel.                                                                                                                                                                                                                                                                      
                                                                                                                                                                                                                                                                                                                           
    url: A URL in the www.timesofisrael.* domain.                                                                                                                                                                                                                                                                                     
                                                                                                                                                                                                                                                                                                                            
    Returns: The Article representing the article at that url.                                                                                                                                                                                                                                                              
    '''
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)


    a = soup.find("title")
    headline = a.text
    paragraphs = soup.findAll("p", {"itemprop": "articleBody"})
    body = ' '.join([p.text.encode('ascii', 'ignore') for p in paragraphs])

    log.info(headline)
    log.info(body)
    return news_interface.Article(headline, body, url, news_orgs.TIMES_OF_ISRAEL)

  def get_query_results(self, query):
    '''Implementation for keyword searches from Times of Israel                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                                                                            
    query: A URL-encoded string.                                                                                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                                                                                            
    Returns: A list of the top Articles returned by the query search.                                                                                                                                                                                                                                                       
    '''
    res = requests.get("https://www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&rsz=filtered_cse&num=10&hl=en&prettyPrint=false&source=gcsc&gss=.com&sig=23952f7483f1bca4119a89c020d13def&cx=015742192883069867459:k3m1yn-i4ua&q=%s&googlehost=www.google.com&callback=google.search.Search.apiary782&nocache=1422549552720" % (query))

    output = res.text.encode('ascii', 'ignore').split("\"ogUrl\":")
    article_urls = []
    for line in output:
      try:
        a = line.split(",")[0].replace('"',"")
        if "http" in a:
          article_urls.append(a)
      except:
        pass

    print article_urls
    top_articles = []
    for url in article_urls[0:news_interface.NUM_ARTICLES]:
      top_articles.append(self.get_article(url))
