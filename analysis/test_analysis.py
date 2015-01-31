import unittest

import extract_keywords
import analysis

class TestAnalysis(unittest.TestCase):

  def test_extract_keywords(self):
    headline = 'What really happened with NBC and Ayman Mohyeldin?'
    res = extract_keywords.extract_keywords(headline)
    self.assertEqual(res, 'nbc ayman mohyeldin')

if __name__ == '__main__':
  unittest.main()
