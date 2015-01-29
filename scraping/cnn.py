from bs4 import BeautifulSoup
import json
import logging
import requests

from logger import log
import news_interface
import news_orgs
from BeautifulSoup import BeautifulSoup
import urllib2
from selenium import webdriver


logging.basicConfig(filename='cnn.log', level=logging.WARNING)

class CNN(news_interface.NewsOrg):
  '''Methods for interacting with the CNN website.'''

  def get_article(self, url):
    '''Implementation for getting an article from CNN.                                                                                                                                                                                                                                                                      
                                                                                                                                                                                                                                                                                                                           
    url: A URL in the www.cnn.* domain.                                                                                                                                                                                                                                                                                     
                                                                                                                                                                                                                                                                                                                            
    Returns: The Article representing the article at that url.                                                                                                                                                                                                                                                              
    '''

    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)
    a = soup.find("title")
    k = a.text.split("-")
    headline = k[0]
    date = k[1]
    c = soup.findAll("p")
    body = ""
    for paragraph in c:
        try:
            body += paragraph.text.decode("utf-8").replace("\"","'") + " "
        except UnicodeEncodeError:
            pass
    log.info(headline)
    log.info(body)
    return news_interface.Article(headline,body,url,news_orgs.CNN)



  def get_query_results(self, query):
    '''Implementation for keyword searches from CNN                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                                                                            
    query: A URL-encoded string.                                                                                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                                                                                            
    Returns: A list of the top Articles returned by the query search.                                                                                                                                                                                                                                                       
    '''
    browser = webdriver.Firefox()
    browser.get("http://www.cnn.com/search/?text=" + query)
    html_source = browser.page_source
    soup = BeautifulSoup(html_source)
    articles = soup.findAll('article', attrs={'class': 'cd cd--card cd--idx-0 cd--large cd--horizontal cd--has-media cd--video'})
    article_urls = [article.a.get('href') for article in articles]
    top_articles = []
    for url in article_urls[0:news_interface.NUM_ARTICLES]:                                                                                                                         
      top_articles.append(self.get_article(url))                                                                                                                                  
      
    return top_articles

