import numpy as np
import pandas as pd
import unittest
import sys, os
DIRNAME = os.path.abspath(__file__ + "/../../../")
print(DIRNAME)

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

#Import house price data
df_house=pd.read_csv (f'{DIRNAME}/data/redfin-sold-last-five-years/all_cleaned.csv')
df_house.rename({'LATITUDE': 'lat', 'LONGITUDE': 'lon'}, axis=1, inplace=True)
df_house=df_house.dropna(subset=['BEDS', 'PROPERTY TYPE'])
df_house=df_house.reset_index(drop=True)

class Testcity_house(unittest.TestCase):
    def test_dataframe_filters(self):
        """
        smoke tests for dataframe filter
        """
        display_time_filters(df_house)
        display_bath_filters(df_house)
        display_bed_filters(df_house)
        display_city_filter(df_house)
        display_property_type_filter(df_house)
        return
    
    def test_map_display_single_select_1b1b(self):
        """
        smoke test marginal values - bed and bath
        on the map, we provide the options to select ranges of beds and baths
        this test tests wether the function breaks when min=max
        """
        display_map(df_house, 2022, 1, 3, 'Single Family Residential', 'Kirkland', 1, 1, 1, 1)
        return

    def test_map_display_single_select_month(self):
        """
        smoke test marginal values - month
        on the map, we provide the options to select ranges of months
        this test tests wether the function breaks when only select 1 month
        """
        display_map(df_house, 2022, 1, 1, 'Single Family Residential', 'Kirkland', 1, 3, 1, 3)
        return

    def test_map_display_all_cities(self):
        """
        smoke test marginal values - cities
        allow map to mark all cities at once
        """
        display_map(df_house, 2022, 1, 1, 'Single Family Residential', '', 1, 3, 1, 3)
        return
    
    def test_multiple_years(self):
        """
        edge test 1
        streamlit map only mark single year data
        """
        with self.assertRaises(ValueError):
            display_map(df_house, [2021, 2022], 1, 3, 'Timeshare', 'Alderwood', 1, 3, 1, 3)
        return

    def test_zero_input(self):
        """
        one-shot test 1
        some combination of selections does not have output as there is no such sale record
        in this case, we want to pass a empty df to the st.map then no markes will show up on map
        """
        df=display_map(df_house, 2022, 1, 3, 'Timeshare', 'Alderwood', 1, 3, 1, 3)
        try:
            len(df['CITY'])==0, "empty df rendered"
        except AssertionError as msg:
            print(msg)
        
    def test_initial_render_city(self):
        """
        one-shot test 2
        the city displayed when open the map on the first time should be Kirkland
        """
        try:
            assert display_city_filter(df_house)!="Kirkland", "wrong initial city"
        except AssertionError as msg:
            print(msg)

    def test_initial_render_property_type(self):
        """
        one-shot test 3
        the propoerty type displayed when open the map on the first time should be Single Family Residential
        """
        try:
            assert display_property_type_filter(df_house)!="Single Family Residential", "wrong initial property type"
        except AssertionError as msg:
            print(msg)

"""
suite=unittest.TestLoader().loadTestsFromTestCase(Testcity_house)
_=unittest.TextTestRunner().run(suite)
"""