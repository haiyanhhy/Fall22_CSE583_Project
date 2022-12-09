import numpy as np
import unittest

from city_house import display_time_filters
from city_house import display_city_filter
from city_house import display_city_multi_filter
from city_house import display_bed_filters
from city_house import display_bath_filters
from city_house import display_property_type_filter
from city_house import display_map
from city_house import display_multi_city_filter
from city_house import price_by_time
from city_house import monthly_house_price_tendency
from city_house import house_price_change_from_highest_to_now_5years
from city_house import house_price_change_from_highest_to_now_3years
from city_house import price_map
#from city_house import main

class TestKnn(unittest.TestCase):

    def test_smoke(self):
        """
        smoke test
        """
        knn_regression(3, 
                       np.array([[3, 1, 230],
                                 [6, 2, 745],
                                 [6, 6, 1080],
                                 [4, 3, 495],
                                 [2, 5, 260]]),
                       np.array([5, 4]))
        return
    
    def test_3_neighbors(self):
        """
        one-shot test 1
        """
        assert np.isclose(knn_regression(3, 
                                         np.array([[3, 1, 230],
                                                   [6, 2, 745],
                                                   [6, 6, 1080],
                                                   [4, 3, 495],
                                                   [2, 5, 260]]),
                                         np.array([5, 4])),
                          773.33)
        return
    
    def test_4_neighbors(self):
        """
        one-shot test 2
        """
        knn_pred_y=knn_regression(4, 
                                  np.array([[3, 1, 230],
                                            [6, 2, 745],
                                            [6, 6, 1080],
                                            [4, 3, 495],
                                            [2, 5, 260]]),
                                  np.array([5, 4]))
        assert np.isclose(knn_pred_y, 645.0)
        return
    
    def test_3D_arrey_query(self):
        """
        edge test 1
        """
        with self.assertRaises(ValueError):
            knn_regression(3, 
                           np.array([[3, 1, 230],
                                     [6, 2, 745],
                                     [6, 6, 1080],
                                     [4, 3, 495],
                                     [2, 5, 260]]),
                           np.array([5, 4, 3])) 
        return

    def test_missing_data(self):
        """
        edge test 2
        """
        with self.assertRaises(ValueError):
            knn_regression(3, 
                           np.array([[3, 1, 230],
                                     [6, 2, 745],
                                     [6, 6],
                                     [4, 3, 495],
                                     [2, 5, 260]]),
                           np.array([5, 4])) 
        return

"""
suite=unittest.TestLoader().loadTestsFromTestCase(TestKnn)
_=unittest.TextTestRunner().run(suite)
"""