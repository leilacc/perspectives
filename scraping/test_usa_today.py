import unittest
import usa_today

class TestUSAToday(unittest.TestCase):

  def setUp(self):
    self.USAToday = usa_today.USAToday()

  def test_get_query_result(self):
    query = 'charlie+hebdo'
    self.USAToday.get_query_result(query)
    #self.assertEqual( multiply(3,4), 12)

  #def test_strings_a_3(self):
    #self.assertEqual( multiply('a',3), 'aaa')

if __name__ == '__main__':
  unittest.main()
