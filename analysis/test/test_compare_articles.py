import json
import unittest

import analysis
import extract_keywords
from scraping import news_interface

class TestAnalysis(unittest.TestCase):

  def setUp(self):
    with open('test_articles/full_test.json') as json_articles:
      json_articles = json.load(json_articles)['results']['news_sources']
      self.articles = []
      for article in json_articles:
        self.articles.append(news_interface.Article(
          article['title'], article['article_text'], article['url'], 0))

  def test_extract_keywords(self):
    headline = 'What really happened with NBC and Ayman Mohyeldin?'
    res = extract_keywords.extract_keywords(headline)
    self.assertEqual(res, 'nbc ayman mohyeldin')

  def test_compare_to_all_articles(self):
    diff = analysis.compare_to_all_articles(self.articles[0], self.articles[1:])
    diff = json.loads(diff)
    self.assertEqual(len(diff), 4, 'Expected 4 comparison articles')
    self.assertEqual(diff[0]['sentences'][0],
        'On May 31, 2010, a group of ships attempted to reach the Gaza Strip but were prevented from reaching their **destination** when members of the Israeli military attacked them in international waters.',
        'Expected a different sentence to have been extracted.')

if __name__ == '__main__':
  unittest.main()
