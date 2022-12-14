import unittest
from flask import current_app
import sys
import os
BASE_DIR= os.path.dirname(os.path.dirname( os.path.abspath(__file__) ))    
sys.path.append( BASE_DIR  )
from prediction_app import app

class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        
        self.app_context=self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
    def tearDown(self):
        self.app_context.pop()
    def test_app_exits(self):
        self.assertFalse(current_app is None)
    def test_testing(self):
        self.assertTrue(self.app.config['TESTING'])

if __name__ == '__main__':
    tests=unittest.TestLoader().loadTestsFromTestCase(BasicTestCase)
    unittest.TextTestRunner(verbosity=2).run(tests)

