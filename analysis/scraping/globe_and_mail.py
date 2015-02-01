from bs4 import BeautifulSoup
import json
import logging
import requests

from logger import log
import news_interface
import news_orgs
import api_keys

logging.basicConfig(filename='globe_and_mail.log', level=logging.WARNING)


class GlobeAndMail(news_interface.NewsOrg):
  '''Methods for interacting with the Globe and Mail website.'''

  def get_article(self, url):
    '''Implementation for getting an article from the Globe and Mail.

    url: A URL in the theglobeandmail.com/* domain.

    Returns: The Article representing the article at that url.
    '''
    soup = BeautifulSoup(requests.get(url).text)

    soup.h1.a.extract()
    headline = soup.h1.get_text().encode('ascii', 'ignore').strip('\n')
    article = soup.find('div', attrs={'class': 'entry-content'})

    # Remove other content that is inline with the article text
    [div.extract() for div in article.find_all('div', attrs={'class': 'entry-related'})]
    [aside.extract() for aside in article.find_all('aside')]

    paragraphs = article.find_all('p', attrs={'class': None})
    body = ' '.join([p.get_text().encode('ascii', 'ignore') for p in paragraphs])

    log.info(headline)
    log.info(body)
    return news_interface.Article(headline, body, url, news_orgs.GLOBE_AND_MAIL)

  def get_query_results(self, query):
    '''Implementation for getting an article from the Globe and Mail.

    query: A URL-encoded string.

    Returns: A list of the top Articles returned by the query search.
    '''
    res = requests.get('http://www.theglobeandmail.com/search/?q=%s' % (query))
    soup = BeautifulSoup(res.text)
    articles = soup.find_all('h3')
    root = 'http://www.theglobeandmail.com'
    article_urls = [root + article.a.get('href') for article in articles
        if article.a]
    non_video_urls = [url for url in article_urls if 'news-video' not in url]

    top_articles = []
    for url in non_video_urls[0:news_interface.NUM_ARTICLES]:
        top_articles.append(self.get_article(url))
    return top_articles
