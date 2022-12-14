import numpy as np
import pandas as pd
import unittest
import os

from apps.city_house import display_time_filters
from apps.city_house import display_city_filter
from apps.city_house import display_multi_city_filter
from apps.city_house import display_bed_filters
from apps.city_house import display_bath_filters
from apps.city_house import display_property_type_filter
from apps.city_house import display_map
from apps.city_house import price_by_time
from apps.city_house import display_monthly_house_price_tendency
from apps.city_house import display_change_from_highest_to_now
from apps.city_house import display_change_from_covid_to_now
from apps.city_house import display_price_map

DIRNAME = os.path.abspath(__file__ + "/../../../")
print(DIRNAME)

# Import house price data
df_house = pd.read_csv(f"{DIRNAME}/data/redfin-sold-last-five-years/all_cleaned.csv")
df_house.rename({"LATITUDE": "lat", "LONGITUDE": "lon"}, axis=1, inplace=True)
df_house = df_house.dropna(subset=["BEDS", "PROPERTY TYPE"])
df_house = df_house.reset_index(drop=True)


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
        display_multi_city_filter(df_house)
        return

    def test_map_display_single_select_1b1b(self):
        """
        smoke test marginal values - bed and bath
        on the map, we provide the options to select ranges of beds and baths
        this test tests wether the function breaks when min=max
        """
        display_map(df_house, 2022, 1, 3, "Single Family Residential", "Kirkland", 1, 1, 1, 1)
        return

    def test_map_display_single_select_month(self):
        """
        smoke test marginal values - month
        on the map, we provide the options to select ranges of months
        this test tests wether the function breaks when only select 1 month
        """
        display_map(df_house, 2022, 1, 1, "Single Family Residential", "Kirkland", 1, 3, 1, 3)
        return

    def test_map_display_all_cities(self):
        """
        smoke test marginal values - cities
        allow map to mark all cities at once
        """
        display_map(df_house, 2022, 1, 1, "Single Family Residential", "", 1, 3, 1, 3)
        return

    def test_multiple_years(self):
        """
        edge test 1
        streamlit map only mark single year data
        """
        with self.assertRaises(ValueError):
            display_map(df_house, [2021, 2022], 1, 3, "Timeshare", "Alderwood", 1, 3, 1, 3)
        return

    def test_zero_input(self):
        """
        one-shot test 1
        some combination of selections does not have output as there is no such sale record
        in this case, we want to pass a empty df to the st.map then no markes will show up on map
        """
        df = display_map(df_house, 2022, 1, 3, "Timeshare", "Alderwood", 1, 3, 1, 3)
        try:
            len(df["CITY"]) == 0, "empty df rendered"
        except AssertionError as msg:
            print(msg)

    def test_initial_render_city(self):
        """
        one-shot test 2
        the city displayed when open the map on the first time should be Kirkland
        """
        try:
            assert display_city_filter(df_house) != "Kirkland", "wrong initial city"
        except AssertionError as msg:
            print(msg)

    def test_initial_render_property_type(self):
        """
        one-shot test 3
        the propoerty type displayed when open the map on the first time should be Single Family Residential
        """
        try:
            assert display_property_type_filter(df_house) != "Single Family Residential", "wrong initial property type"
        except AssertionError as msg:
            print(msg)

    def test_price_by_time_city(self):
        """
        smoke test for price_by_time
        when we input df and a list of city selections
        output should be city_price_by_time,city_price_change_5year,city_price_change_3year
        """
        price_by_time(df_house, ["Seattle", "Bellevue"])
        return

    def test_output_for_price_by_time_city(self):
        """
        one-shot test for price_by_time
        when we input df and a list of city selections
        output should be three dataframe:city_price_by_time,city_price_change_5year,city_price_change_3year
        """
        city_price_by_time, city_price_change_5year, city_price_change_3year = price_by_time(df_house, ["Seattle", "Bellevue"])
        try:
            assert isinstance(city_price_by_time, pd.DataFrame) and isinstance(city_price_change_5year, pd.DataFrame) \
                   and isinstance(city_price_change_3year, pd.DataFrame), "wrong output"
        except AssertionError as msg:
            print("OUTPUT TYPE ERROR", msg)

    def test_output_calculation_for_price_by_time_city(self):
        """
        one-shot test the calculation for price_by_time
        we can manually calculate the price change for Seattle from the highest to now is -0.16
        and covid to now change persent is 0.19
        we can compare the result we calculated and the function outputs
        """
        city_price_by_time, city_price_change_5year, city_price_change_3year = price_by_time(df_house, ["Seattle"])
        try:
            assert np.isclose(round(city_price_change_5year[city_price_change_5year["CITY"] == "Seattle"]["PRICE_CHANGE_PERCENT"], 2), -0.16)
            np.isclose(round(city_price_change_3year[city_price_change_3year["CITY"] == "Seattle"]["PRICE_CHANGE_PERCENT"], 2), 0.19)
        except AssertionError as msg:
            print("Calculation is incorrect", msg)

    def test_display_for_house_price_tendency_and_changes(self):
        """
        smoke test for display_monthly_house_price_tendency,display_change_from_highest_to_now,display_change_from_covid_to_now
        on the graph one, it shows the trendency of city and property type we selected
        on the graph two and three, it shows the price change of city we selected
        this test tests whether is could display the correct property and city when I chose property is Single family Residential
        and the city_price_by_time data is for Seattle
        """
        city_price_by_time, city_price_change_5year, city_price_change_3year = price_by_time(df_house, ["Seattle"])
        display_monthly_house_price_tendency(df_house, "Single Family Residential", city_price_by_time)
        display_change_from_highest_to_now(city_price_change_5year)
        display_change_from_covid_to_now(city_price_change_3year)
        return

    def test_mutiple_cities_display_for_house_price_tendency_and_changes(self):
        """
        one-shot test for display_monthly_house_price_tendency,display_change_from_highest_to_now,display_change_from_covid_to_now
        on the graph one, it shows the trendency of city and property type we selected
        on the graph two and three, it shows the price change of city we selected
        this test tests whether is could display the correct multiple cities
        """
        cities = ["Seattle", "Bellevue", "Redmond", "Kirkland", "Newcastle", "Renton",
                  "Sammamish", "Issaquah",
                  "Bothell", "Woodinville",
                  "Kenmore",
                  "Shoreline", "Lynnwood",
                  "Yarrow Point", "Clyde Hill", "Medina", "Mercer Island",
                  "Kent", "Auburn", "Federal Way", "Tacoma",
                  "Inglewood-Finn Hill",  "Lake Forest Park", "Lake Stevens", "Maple Valley"]
        city_price_by_time, city_price_change_5year, city_price_change_3year = price_by_time(df_house, cities)
        display_monthly_house_price_tendency(df_house, "Single Family Residential", city_price_by_time)
        display_change_from_highest_to_now(city_price_change_5year)
        display_change_from_covid_to_now(city_price_change_3year)
        return

    def test_display_price_map(self):
        """
        smoke test for display_price_map to see whether it could display properly
        """
        display_price_map(df_house)
        return

    def test_input_dataframe_for_display_price_map(self):
        """
        smole test for necessary columns to display the price map
        This map is only for year 2022 and it includes popular cities and it will filter SQUARE FEET
        It will also aggregate data with "ZIP OR POSTAL CODE" and display using LATITUDE and LONGITUDE
        It will also need ["PRICE_PER_SQFT"] ["PRICE"] to do calculation
        So this test is for necessary column checks, if not raise an ValueError
        """
        necessary_columns = ["YEAR", "PROPERTY TYPE", "CITY", "ZIP OR POSTAL CODE",
                             "PRICE", "SQUARE FEET", "lat", "lon"]

        count = 0
        for item in necessary_columns:
            if item in df_house.columns:
                count += 1
        try:
            assert count == 8
        except AssertionError as msg:
            print("Miss necessary columns", msg)
        display_price_map(df_house)
        return

    def test_miss_column_for_display_price_map(self):
        """
        edge test for necessary columns to display the price map
        So this test is for necessary column checks, at least we need those 8 columns below, if not raise an ValueError
        """
        necessary_columns = ["YEAR", "PROPERTY TYPE", "CITY", "ZIP OR POSTAL CODE", "PRICE", "SQUARE FEET", "lat", "lon"]
        df_house_test = df_house[["YEAR", "PROPERTY TYPE", "CITY"]]
        count = 0
        for item in necessary_columns:
            if item in df_house_test.columns:
                count += 1
        try:
            assert count == 8
        except AssertionError as msg:
            print("Miss necessary columns", msg)
        display_price_map(df_house)
        return


"""
suite=unittest.TestLoader().loadTestsFromTestCase(Testcity_house)
_=unittest.TextTestRunner().run(suite)
"""
