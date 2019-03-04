import unittest
from app.models import Blog


class BlogTest(unittest.TestCase):
    '''
    Test Class to test the behaviour of the Pitch class
    '''

    def setUp(self):
        '''
        Set up method that will run before every Test
        '''
        self.new_blog = Blog(1, 'Python Must Be Crazy',
                             'A thrilling new Python Series', 'wecode', 2018)

    def test_instance(self):
        self.assertTrue(isinstance(self.new_blog, Blog))