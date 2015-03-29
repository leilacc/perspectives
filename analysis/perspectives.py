'''Get perspectives from different articles.'''

import futures
import json
import re
import time

from nltk.corpus import wordnet as wn

import compare_articles
import extract_keywords
from scraping import aljazeera, bbc, cbc, cnn, globe_and_mail, guardian, \
                     huff_post, jpost, ny_post, ny_times, reuters, \
                     russia_today, times_of_israel, todays_zaman, usa_today
from scraping import logger

AL_JAZEERA = aljazeera.AlJazeera()
BBC = bbc.BBC()
CBC = cbc.CBC()
CNN = cnn.CNN()
GLOBE_AND_MAIL = globe_and_mail.GlobeAndMail()
GUARDIAN = guardian.Guardian()
HUFF_POST = huff_post.HuffPost()
JPOST = jpost.JPost()
NY_POST = ny_post.NYPost()
NY_TIMES = ny_times.NYTimes()
REUTERS = reuters.Reuters()
RT = russia_today.RussiaToday()
TIMES_OF_ISRAEL = times_of_israel.TimesOfIsrael()
TODAYS_ZAMAN = todays_zaman.TodaysZaman()
USA_TODAY = usa_today.USAToday()

NEWS_ORGS = [AL_JAZEERA, BBC, CBC, CNN, GLOBE_AND_MAIL, GUARDIAN, HUFF_POST,
            JPOST, NY_POST, NY_TIMES, REUTERS, RT, TIMES_OF_ISRAEL,
            TODAYS_ZAMAN, USA_TODAY]


def get_perspectives(url):
  '''Get different perspectives on the topic covered by article.

  Args:
    url: A string.

  Returns:
    A JSON-encoded string representing other articles with different
    perspectives than the original article.

    Format: a list of Article.to_dict()s, each with an additional 'sentences'
    attribute. 'sentences' contains a list of sentences with semantically
    different words that were extracted from the corresponding article's body.
  '''
  start_time = time.time()
  article = url_to_article(url)
  print("--- url_to_article: %s seconds ---" % (time.time() - start_time))
  if article:
    start_time = time.time()
    headline = article.headline
    body = article.body
    org = article.news_org

    article_topic = extract_keywords.extract_keywords(headline)
    print("--- keyword extraction: %s seconds ---" % (time.time() - start_time))

    start_time = time.time()
    NP_to_sentence, VP_to_sentence  = compare_articles.get_phrases(body, org)
    NPs = set(NP_to_sentence.keys())
    VPs = set(VP_to_sentence.keys())
    print("--- surface comparison article: %s seconds ---" % (time.time() - start_time))

    start_time = time.time()
    NP_synsets = compare_articles.get_synsets_and_ancestors(NPs)
    VP_synsets = compare_articles.get_synsets_and_ancestors(VPs, NP=False)
    print("--- get_synsets: %s seconds ---" % (time.time() - start_time))

    n = len(NEWS_ORGS)
    with futures.ProcessPoolExecutor(max_workers=n) as executor:
      comparisons = executor.map(get_comparison, NEWS_ORGS, [article_topic]*n,
                                 [NP_to_sentence]*n, [VP_to_sentence]*n,
                                 [NPs]*n, [VPs]*n,
                                 [NP_synsets]*n, [VP_synsets]*n,
                                 [1]*n)
      compared_articles_by_org = list(comparisons)
      # flatten from list of lists of articles (separated by news org) to list
      # of articles
      compared_articles = [article for org_articles in compared_articles_by_org
                                   for article in org_articles]
      return json.dumps(compared_articles)
    # uncomment to run iteratively
      '''
    return json.dumps(get_comparison(1,article_topic,1,1,1,1, article))
    '''
  else:
    return json.dumps("Not a recognized article")

def get_comparison(news_org, article_topic, NP_to_sentence, VP_to_sentence,
                   NPs, VPs, NP_synsets, VP_synsets, article):
  '''Compares the articles from a single NewsOrg to an article that is
  represented by its NPs and VPs.'''
  NP_synsets = [wn._synset_from_pos_and_offset(pos, offset)
                for (pos, offset) in NP_synsets]
  VP_synsets = [wn._synset_from_pos_and_offset(pos, offset)
                for (pos, offset) in VP_synsets]

  comparison_articles = news_org.get_query_results(article_topic)
  comparisons = []
  for comparison_article in comparison_articles:
    try:
      comparisons.append(
          compare_articles.compare_articles(NP_to_sentence, VP_to_sentence,
                                            NPs, VPs,
                                            NP_synsets, VP_synsets,
                                            comparison_article))
    except:
      continue
  return comparisons
  # uncomment to run iteratively
  '''
  return compare_articles.compare_to_all_articles(
      article, query_all_news_orgs(article_topic))
  '''

def query_all_news_orgs(query):
  '''Get the top articles for the given query from all supported news orgs.

  Args:
    query: A string of keywords.

  Returns:
    A list of Articles.
  '''
  top_articles = []
  for news_org in NEWS_ORGS: #TODO: parallelize
    try:
      top_articles.extend(news_org.get_query_results(query))
    except TypeError as e:
      logger.log.error('Error getting query results for %s: %s' %
                       (news_org, e))
  return top_articles

def url_to_article(url):
  '''Returns the Article at url if the url is supported.

  Args:
    url: A string.

  Returns:
    The Article that is scraped from url, if the url corresponds to an article
    on a supported news org page. Otherwise, None.
  '''
  if re.search(r'.*aljazeera\.com/((opinions)|(articles)|(news))/.+', url):
    return AL_JAZEERA.get_article(url)
  elif re.search(r'.*bbc\..+', url):
    return BBC.get_article(url)
  elif re.search(r'.*cbc\.ca/news/.+', url):
    return CBC.get_article(url)
  elif re.search(r'.*cnn\.com/.+', url):
    return CNN.get_article(url)
  elif re.search(r'.*theglobeandmail\.com/.+', url):
    return GLOBE_AND_MAIL.get_article(url)
  elif re.search(r'.*theguardian\.com/.+', url):
    return GUARDIAN.get_article(url)
  elif re.search(r'.*huffingtonpost\.c.+/.+', url):
    return HUFF_POST.get_article(url)
  elif re.search(r'.*jpost\.com/.+', url):
    return JPOST.get_article(url)
  elif re.search(r'.*nypost\.com/.+', url):
    return NY_POST.get_article(url)
  elif re.search(r'.*nytimes\.com/.+', url):
    return NY_TIMES.get_article(url)
  elif re.search(r'.*reuters\.com/.+', url):
    return REUTERS.get_article(url)
  elif re.search(r'.*rt\.com/.+', url):
    return RT.get_article(url)
  elif re.search(r'.*timesofisrael\.com/.+', url):
    return TIMES_OF_ISRAEL.get_article(url)
  elif re.search(r'.*todayszaman\.com/.+', url):
    return TODAYS_ZAMAN.get_article(url)
  elif re.search(r'.*usatoday\.com/story/.+', url):
    return USA_TODAY.get_article(url)
  else:
    logger.log.info("Didn't regexp match for %s" % url)
    return None
