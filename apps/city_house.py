"""
This is a script making a web app to show interactive analysis
for Seattle Metro Area Housing Prices
"""
import streamlit as st
import pandas as pd
import numpy as np
import folium
import matplotlib.pyplot as plt
import plotly.express as px
from streamlit_folium import st_folium
import sys
import os
# To successfully import prediction_app
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import streamlit.components.v1 as components
DIRNAME = os.path.abspath(__file__ + "/../../")

APP_TITLE = 'Seattle Metro Area Housing Prices'
APP_SUB_TITLE = 'Source: Redfin https://www.redfin.com/city/16163/WA/Seattle/filter/viewport=47.93252:47.29375:-121.83461:-123.42076,no-outline' 
APP_SUB_TITLE2 = 'Data updated: Oct.2022' 

def display_time_filters(df):
    """
    dropdown bar for a year
    double-end slider for monther
    """
    year_list = [2017, 2018, 2019, 2020, 2021, 2022]
    year = st.sidebar.selectbox('Sold Year', year_list, len(year_list) - 1)
    start_month, end_month = st.sidebar.select_slider(
        'Select a range of months',
        options = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        value = (1, 2))
    st.write('Change year and range of months in sidebar')
    st.subheader(f'Houses sold between {start_month}/{year} and {end_month}/{year}')
    return year, start_month, end_month


def display_city_filter(df):
    """
    single select city from dropdown bar
    """
    city_list = [''] + list(df['CITY'].unique())
    city_name = st.sidebar.selectbox('City', city_list, index=2)
    return city_name


def display_bed_filters(df):
    bed_list = list(range(0, 100))
    min_bed, max_bed = st.select_slider(
        '#BEDS',
        options=bed_list,
        value=(1, 3))
    return min_bed, max_bed


def display_bath_filters(df):
    bath_list = list(range(0, 300))
    min_bath, max_bath = st.select_slider(
        '#BATHS',
        options=bath_list,
        value=(1, 3))
    return min_bath, max_bath


def display_property_type_filter(df):
    """
    single select proporty type
    """
    property_type_list = [''] + list(df['PROPERTY TYPE'].unique())
    property_type = st.sidebar.radio('Property Type (option 1 selects all types)', property_type_list, index = 1)
    return property_type


def display_map(df, year, start_month, end_month, property_type, city_name, min_bed, max_bed, min_bath, max_bath):
    # define lat, long for points
    midpoint = (np.average(df['lat']), np.average(df['lon']))
    map = folium.Map(location=[midpoint[0], midpoint[1]], zoom_start=10,
                     scrollWheelZoom=False, tiles='CartoDB positron')

    df2 = df.groupby(['CITY'])['$/SQUARE FEET'].size().reset_index(name='count')
    df3 = df.groupby(['CITY'])['$/SQUARE FEET'].mean().reset_index(name='mean')
    df = df.merge(df2, how='left', on='CITY')
    df = df.merge(df3, how='left', on='CITY')

    DIRNAME = os.path.abspath(__file__ + "/../../")
    # Map base use city boundaries and display info
    choropleth = folium.Choropleth(
        geo_data = f'{DIRNAME}/data/WSDOT_-_City_Limits.geojson',
        data = df,
        columns = ('CITY', 'mean'),
        key_on = 'feature.properties.CityName',
        line_opacity = 0.8,
        highlight = True
    )
    choropleth.geojson.add_to(map)

    df_sub = df[['CITY', 'mean', 'count']]
    df_sub.drop_duplicates(inplace=True)
    df_indexed = df_sub.set_index('CITY')
    # Add display info
    for feature in choropleth.geojson.data['features']:
        city = feature['properties']['CityName']
        feature['properties']['ave_sqft_price'] = 'AveSqftPrices: ' + str(round(df_indexed.loc[city, 'mean'])) if city in list(df_indexed.index) else 'Unknown'
        feature['properties']['total_sales'] = 'TotalSale: ' + str(df_indexed.loc[city, 'count']) if city in list(df_indexed.index) else 'Unknown'
    
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['CityName', 'ave_sqft_price', 'total_sales'], labels=False)
    )

    # Apply filter to df
    df = df[(df['SOLD YEAR'] == year) & (df['SOLD MONTH_Number'] >= start_month) & (df['SOLD MONTH_Number'] <= end_month)]
    if city_name:
        df = df[df['CITY'] == city_name]
    if property_type:
        df = df[df['PROPERTY TYPE'] == property_type]
    df = df[(df['BEDS'] >= min_bed) & (df['BEDS'] <= max_bed)]
    df = df[(df['BATHS'] >= min_bath) & (df['BATHS'] <= max_bath)]

    # Add marker to filled city map
    for i in range(0, len(df)):
        folium.Marker(
            location=[df.iloc[i]['lat'], df.iloc[i]['lon']],
            radius=2,
            tooltip=f"<b>Location: {df.iloc[i]['LOCATION']}</b><br><br>Zip Code: {df.iloc[i]['ZIP OR POSTAL CODE']}",
            icon=folium.Icon(color='orange', icon='home')
        ).add_to(map)

    st_map = st_folium(map, width=700, height=450)
    return df


# define a multiselection bar for top 10 price change cities
def display_multi_city_filter(df):
    """
    mulit select cities
    """
    cities = st.multiselect(
        'Select the cities you are interested',
        ["Seattle", "Bellevue", "Redmond", "Kirkland", "Newcastle", "Renton",
         "Sammamish", "Issaquah",
         "Bothell", "Woodinville",
         "Kenmore",
         "Shoreline", "Lynnwood",
         "Yarrow Point", "Clyde Hill", "Medina", "Mercer Island",
         "Kent", "Auburn", "Federal Way", "Tacoma",
         "Inglewood-Finn Hill",  "Lake Forest Park", "Lake Stevens", "Maple Valley"])
    st.write('You selected:', cities)
    return cities

# def function for display_monthly_house_price_tendency
def price_by_time(df, cities):
    filtered_house_data = df[df["CITY"].isin(cities)]
    filtered_house_data = filtered_house_data[~filtered_house_data["SQUARE FEET"].isna()]
    filtered_house_data = filtered_house_data[filtered_house_data["SQUARE FEET"] > 1500]
    filtered_house_data["PRICE_PER_SQFT"] = filtered_house_data["PRICE"] / filtered_house_data["SQUARE FEET"]
    city_price_by_time = filtered_house_data.groupby(["CITY", "YEAR_MONTH"])["PRICE_PER_SQFT"].median().reset_index().sort_values("PRICE_PER_SQFT", ascending=False).sort_values("YEAR_MONTH")

    temp = filtered_house_data.groupby(["CITY", "YEAR_MONTH"])["PRICE"].median().reset_index().sort_values("PRICE", ascending=False).sort_values("YEAR_MONTH")
    city_price_by_time = city_price_by_time.merge(temp, on = ["CITY", "YEAR_MONTH"])

    temp = filtered_house_data.groupby(["CITY", "YEAR_MONTH"]).size().reset_index().rename(columns = {0: "COUNT"})
    city_price_by_time = city_price_by_time.merge(temp, on = ["CITY", "YEAR_MONTH"])

    city_price_highest_month \
        = city_price_by_time.groupby("CITY")["PRICE_PER_SQFT"].max().reset_index().sort_values("PRICE_PER_SQFT", ascending=False).rename(columns={"PRICE_PER_SQFT": "HIGHEST_PRICE"})
    city_price_2022_10 = \
        city_price_by_time[city_price_by_time["YEAR_MONTH"] == "2022-10"][["CITY", "PRICE_PER_SQFT"]].rename(columns={"PRICE_PER_SQFT": "PRICE_2022_10"})
    city_price_change_5year = pd.merge(city_price_highest_month, city_price_2022_10, on="CITY")
    city_price_change_5year["PRICE_CHANGE"] = city_price_change_5year["PRICE_2022_10"] - city_price_change_5year["HIGHEST_PRICE"]
    city_price_change_5year["PRICE_CHANGE_PERCENT"] = city_price_change_5year["PRICE_CHANGE"] / city_price_change_5year["HIGHEST_PRICE"]
    city_price_change_5year = city_price_change_5year.sort_values("PRICE_CHANGE_PERCENT", ascending=True)

    city_price_2019_10 = \
        city_price_by_time[city_price_by_time["YEAR_MONTH"] == "2019-10"][["CITY", "PRICE_PER_SQFT"]].rename(columns={"PRICE_PER_SQFT": "PRICE_2019_10"})
    city_price_change_3year = pd.merge(city_price_change_5year, city_price_2019_10, on = "CITY")
    city_price_change_3year["PRICE_CHANGE_FROM_2019_10"] = city_price_change_3year["PRICE_2022_10"] - city_price_change_3year["PRICE_2019_10"]
    city_price_change_3year["PRICE_CHANGE_PERCENT_FROM_2019_10"] = city_price_change_3year["PRICE_CHANGE_FROM_2019_10"] / city_price_change_3year["PRICE_2019_10"]
    city_price_change_3year = city_price_change_3year.sort_values("PRICE_CHANGE_PERCENT_FROM_2019_10", ascending=True)

    return city_price_by_time, city_price_change_5year, city_price_change_3year


def display_monthly_house_price_tendency(df, property_type, city_price_by_time):
    df = df[df["PROPERTY TYPE"] == property_type]

    fig = px.line(
        city_price_by_time,
        x="YEAR_MONTH",
        y="PRICE_PER_SQFT",
        color="CITY",
        hover_data=["PRICE_PER_SQFT", "CITY", "YEAR_MONTH", "COUNT"],
        title="Monthly House Price (Per SQFT) Change by City over the Last 5 years",
    )
    fig.update_layout(
        # center the title
        title_x=0.5,
        # set the figure size
        width=700,
        height=450
    )
    return fig


def display_change_from_highest_to_now(city_price_change_5year):
    # plot the price change
    fig = px.bar(
        city_price_change_5year.round(2),
        x="CITY",
        y="PRICE_CHANGE_PERCENT",
        title="Price (PER SQFT) Change from Highest to 2022-10",
        text="PRICE_CHANGE_PERCENT",
        color="CITY",
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    fig.update_layout(
        # center the title
        title_x=0.5,
        # set the figure size
        width=700,
        height=450,
    )
    return fig


def display_change_from_covid_to_now(city_price_change_3year):
    # plot the price change
    fig = px.bar(
        city_price_change_3year.round(2),
        x="CITY",
        y="PRICE_CHANGE_PERCENT_FROM_2019_10",
        title="Price (PER SQFT) Change from 2019-10 to 2022-10",
        text="PRICE_CHANGE_PERCENT_FROM_2019_10",
        color="CITY",
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    fig.update_layout(
        # center the title
        title_x=0.5,
        # set the figure size
        width=700,
        height=450,
    )
    return fig


def display_price_map(df):
    filtered_house_data = df[df["CITY"].isin(["Seattle", "Bellevue", "Redmond", "Kirkland", "Newcastle", "Renton",
                                              "Sammamish", "Issaquah", "Bothell", "Woodinville", "Kenmore", "Shoreline",
                                              "Lynnwood", "Yarrow Point", "Clyde Hill", "Medina", "Mercer Island",
                                              # "Kent", "Auburn", "Federal Way", "Tacoma",
                                              # "Inglewood-Finn Hill",  "Lake Forest Park", "Lake Stevens", "Maple Valley"
                                              ])]
    filtered_house_data = filtered_house_data[filtered_house_data["YEAR"] == 2022]
    filtered_house_data = filtered_house_data[~filtered_house_data["SQUARE FEET"].isna()]
    filtered_house_data = filtered_house_data[filtered_house_data["SQUARE FEET"] > 1500]
    filtered_house_data["PRICE_PER_SQFT"] = filtered_house_data["PRICE"] / filtered_house_data["SQUARE FEET"]

    # zip_prices = filtered_house_data.groupby("ZIP OR POSTAL CODE")["PRICE"].mean().reset_index()
    # zip_prices["PRICE"] = (zip_prices["PRICE"] / 1e6).round(2)
    zip_prices = filtered_house_data.groupby("ZIP OR POSTAL CODE")["PRICE_PER_SQFT"].mean().reset_index()
    zip_prices["PRICE"] = zip_prices["PRICE_PER_SQFT"].round(2)
    zip_prices["ZIP OR POSTAL CODE"] = zip_prices["ZIP OR POSTAL CODE"].astype(str)

    # initiating a Folium map with the average longitude and latitude
    # m = folium.Map(location = [df["LATITUDE"].mean(), df["LONGITUDE"].mean()], zoom_start = 11)
    midpoint = (np.average(df['lat']), np.average(df['lon']))
    m = folium.Map(location=[midpoint[0], midpoint[1]], zoom_start=8, scrollWheelZoom=False, tiles='CartoDB positron')

    # bins = list(zip_prices["PRICE"].quantile([0, 0.15, 0.3, 0.45, 0.6, 0.75, 0.9, 0.95, 0.99, 1]))
    bins = list(zip_prices["PRICE"].quantile([0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1]))

    cp = folium.Choropleth(
        geo_data=f'{DIRNAME}/data/wa_washington_zip_codes_geo.min.json',
        name="choropleth",
        data=zip_prices,
        columns=["ZIP OR POSTAL CODE", "PRICE"],
        key_on="feature.properties.ZCTA5CE10",
        bins=9,
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.4,
        nan_fill_color="white",
        nan_fill_opacity=0.9,
        legend_name="",
        highlight=True,
    ).add_to(m)

    # creating a state indexed version of the dataframe so we can lookup values
    zip_prices_indexed = zip_prices.set_index('ZIP OR POSTAL CODE')

    # looping thru the geojson object and adding a new property(unemployment)
    # and assigning a value from our dataframe
    for s in cp.geojson.data["features"]:
        if s["properties"]["ZCTA5CE10"] in zip_prices_indexed.index:
            s["properties"]["ZIP Code"] = str(s["properties"]["ZCTA5CE10"])
            s["properties"]["PRICE"] = str(zip_prices_indexed.loc[s["properties"]["ZCTA5CE10"]]["PRICE"])
        else:
            s["properties"]["ZIP Code"] = str(s["properties"]["ZCTA5CE10"])
            s["properties"]["PRICE"] = "N/A"

    # and finally adding a tooltip/hover to the choropleth's geojson
    folium.GeoJsonTooltip(
        ["ZIP Code", "PRICE"],
        aliases=["ZIP Code", "Average Price Per Sqft"],
    ).add_to(cp.geojson)

    folium.LayerControl().add_to(m)
    st_m = st_folium(m, width=700, height=450)
    return st_m


def main():
    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)
    st.caption(APP_SUB_TITLE)
    st.caption(APP_SUB_TITLE2)

    # Load Data
    df_house = pd.read_csv(f'{DIRNAME}/data/redfin-sold-last-five-years/all_cleaned.csv')
    df_house.rename({'LATITUDE': 'lat', 'LONGITUDE': 'lon'}, axis=1, inplace=True)
    df_house = df_house.dropna(subset=['BEDS', 'PROPERTY TYPE'])
    df_house = df_house.reset_index(drop=True)

    # Display Filters and Map
    year, start_month, end_month = display_time_filters(df_house)
    property_type = display_property_type_filter(df_house)

    st.write(f'Select number of bedrooms and bathrooms')

    col1, col2 = st.columns(2)
    with col1:
        min_bed, max_bed = display_bed_filters(df_house)
    with col2:
        min_bath, max_bath = display_bath_filters(df_house)
    
    city_name = display_city_filter(df_house)
    display_map(df_house, year, start_month, end_month, property_type, city_name, min_bed, max_bed, min_bath, max_bath)

    #Display Trend Analysis
    st.subheader('Price change analysis by cities')
    st.write('You can change the propery type in side bar and muti-select cities here')
    cities = display_multi_city_filter(df_house)
    city_price_by_time, city_price_change_5year, city_price_change_3year = price_by_time(df_house, cities)
    st.write('Interact with the plot: \n feel free to download, zoom in, zoom out, make it full screen or hide some lines.')
    st.plotly_chart(display_monthly_house_price_tendency(df_house, property_type, city_price_by_time))
    st.plotly_chart(display_change_from_highest_to_now(city_price_change_5year))
    st.plotly_chart(display_change_from_covid_to_now(city_price_change_3year))
    st.subheader('Current price for each zip code in popular cities')
    display_price_map(df_house)
    st.subheader('If you are a home builder,feel free to click the "prediction" button in the sidebar')

    prediction_box = st.sidebar.checkbox('prediction')
    if prediction_box:
        components.iframe('http://127.0.0.1:5000', height=900, scrolling=True)


if __name__ == "__main__":
    main()
