import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import sys, os

APP_TITLE = 'Seattle Metropolitan Area Housing Prices'
APP_SUB_TITLE = 'Source: Redfin' # Need to further specify datasource

def display_time_filters(df):
    """
    dropdown bar for a year
    double-end slider for monther
    """
    #year_list = [list(df['SOLD YEAR'].unique())]
    #year_list.sort()
    year_list = [2017, 2018, 2019, 2020, 2021]
    year = st.sidebar.selectbox('Sold Year', year_list, len(year_list)-1)
    start_month, end_month = st.select_slider(
        'Select a range of months',
        options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        value=(1, 2))
    st.write('Sold between', start_month,'/',year, 'and', end_month,'/',year)
    st.header(f'{year} month {start_month}-{end_month}')
    return year, start_month, end_month

def display_city_filter(df):
    """
    single select city from dropdown bar
    """
    city_list = [''] + list(df['CITY'].unique())
    #city_index = city_list.index(city_name) if city_name and city_name in city_list else 0
    city_name = st.sidebar.selectbox('City', city_list, len(city_list)-1)
    return city_name

def display_bed_filters(df):
    #top_bed=df['BEDS'].max()
    bed_list = list(range(0,100))
    min_bed, max_bed = st.select_slider(
        'Select a range of bedrooms',
        options=bed_list,
        value=(1, 3))
    return min_bed, max_bed

def display_bath_filters(df):
    #top_bath=df['BATHS'].max()
    bath_list = list(range(0,300))
    min_bath, max_bath = st.select_slider(
        'Select a range of bathrooms',
        options=bath_list,
        value=(1, 3))
    return min_bath, max_bath

def display_property_type_filter(df):
    """
    single select proporty type
    """
    property_type_list = [''] + list(df['PROPERTY TYPE'].unique())
    #property_type_index = property_type_list.index(property_type) if property_type and property_type in property_type else 0
    property_type = st.sidebar.radio('Property Type', property_type_list, len(property_type_list)-1)
    return property_type

def display_map(df, year, start_month, end_month, property_type, city_name, min_bed, max_bed, min_bath, max_bath):
    # define lat, long for points
    midpoint = (np.average(df['lat']), np.average(df['lon']))
    map = folium.Map(location=[midpoint[0], midpoint[1]], zoom_start=8, scrollWheelZoom=False, tiles='CartoDB positron')

    df2 = df.groupby(['CITY'])['$/SQUARE FEET'].size().reset_index(name='count')
    df3 = df.groupby(['CITY'])['$/SQUARE FEET'].mean().reset_index(name='mean')
    #df2=df.groupby(['CITY'])['$/SQUARE FEET'].describe()[['count', 'mean']]
    #df2_indexed = df2.set_index('City')
    df=df.merge(df2, how="left", on='CITY',)
    df=df.merge(df3, how="left", on='CITY',)

    DIRNAME = os.path.abspath(__file__ + "/../../")
    #Map base use city boundaries and display info
    choropleth = folium.Choropleth(
        geo_data=f'{DIRNAME}/data/WSDOT_-_City_Limits.geojson',
        data=df,
        columns=('CITY', 'mean'),
        key_on='feature.properties.CityName',
        line_opacity=0.8,
        highlight=True
    )
    choropleth.geojson.add_to(map)
    
    df_sub = df[['CITY', 'mean', 'count']]
    df_sub.drop_duplicates(inplace=True)
    df_indexed = df_sub.set_index('CITY')
    #Add display info 
    for feature in choropleth.geojson.data['features']:
        city = feature['properties']['CityName']
        feature['properties']['ave_sqft_price'] = 'AveSqftPrices: ' + str(round(df_indexed.loc[city, 'mean'])) if city in list(df_indexed.index) else 'Unknown'
        feature['properties']['total_sales'] = 'TotalSale: ' + str(df_indexed.loc[city, 'count']) if city in list(df_indexed.index) else 'Unknown'
    
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['CityName', 'ave_sqft_price', 'total_sales'], labels=False)
    )
    
    #Apply filter to df 
    df = df[(df['SOLD YEAR'] == year) & (df['SOLD MONTH_Number'] >= start_month) & (df['SOLD MONTH_Number'] <= end_month)]
    if city_name:
        df = df[df['CITY'] == city_name]
    if property_type:
        df = df[df['PROPERTY TYPE'] == property_type]
    df = df[(df['BEDS'] >= min_bed) & (df['BEDS'] <= max_bed)]
    df = df[(df['BATHS'] >= min_bath) & (df['BATHS'] <= max_bath)]
    
    #Add marker to filled city map
    for i in range(0, len(df)):
        folium.Marker(
            location=[df.iloc[i]['lat'], df.iloc[i]['lon']],
            popup=df.iloc[i]['LOCATION']
        ).add_to(map)

    st_map = st_folium(map, width=700, height=450)
    
    city_name = 'Seattle'
    if st_map['last_active_drawing']:
        city_name = st_map['last_active_drawing']['properties']['CityName']
    
    return 

def display_house_facts(df, year, start_month, end_month, property_type, city_name, min_bed, max_bed, min_bath, max_bath, title, string_format='${:,}', is_prediction=False):
    df = df[(df['SOLD YEAR'] == year) & (df['SOLD MONTH_Number'] >= start_month) & (df['SOLD MONTH_Number'] <= end_month)]
    df = df[(df['BEDS'] >= min_bed) & (df['BEDS'] <= max_bed)]
    df = df[(df['BATHS'] >= min_bath) & (df['BATHS'] <= max_bath)]
    if city_name:
        df = df[df['CITY'] == city_name]
    if property_type:
        df = df[df['PROPERTY TYPE'] == property_type]
    df.drop_duplicates(inplace=True)
    ave_price = df['$/SQUARE FEET'].sum() / len(df['$/SQUARE FEET']) if len(df) else 0
    total_sale = df['$/SQUARE FEET'].count()
    st.metric(title, string_format.format(round(ave_price)), string_format.format(round(total_sale)))


def main():
    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)
    st.caption(APP_SUB_TITLE)

    #Load Data
    DIRNAME = os.path.abspath(__file__ + "/../../")
    df_house=pd.read_csv (f'{DIRNAME}/data/redfin-sold-last-five-years/all.csv')
    df_house.rename({'LATITUDE': 'lat', 'LONGITUDE': 'lon'}, axis=1, inplace=True)
    df_house=df_house.dropna(subset=['BEDS', 'PROPERTY TYPE'])
    df_house=df_house.reset_index(drop=True)

    #Display Filters and Map
    year, start_month, end_month = display_time_filters(df_house)
    property_type = display_property_type_filter(df_house)
    min_bed, max_bed = display_bed_filters(df_house)
    min_bath, max_bath = display_bath_filters(df_house)
    city_name = display_city_filter(df_house)
    display_map(df_house, year, start_month, end_month, property_type, city_name, min_bed, max_bed, min_bath, max_bath)

    #Display Metrics
    st.subheader(f'{city_name} {property_type} Housing Facts')
    st.write(f'for #beds ranges from {min_bed} to {max_bed} and #baths ranges from {min_bath} to {max_bath} from {start_month}/{year} to {end_month}/{year}')

    col1, col2, col3 = st.columns(3)
    with col1:
        display_house_facts(df_house, year, start_month, end_month, property_type, city_name, min_bed, max_bed, min_bath, max_bath, 'Selected City', string_format='${:,}')
    with col2:
        display_house_facts(df_house, year, start_month, end_month, property_type, city_name, min_bed, max_bed, min_bath, max_bath, 'Ave $/Sqaure Feet', string_format='${:,}')
    with col3:
        display_house_facts(df_house, year, start_month, end_month, property_type, city_name, min_bed, max_bed, min_bath, max_bath, 'Total # Sales', string_format='${:,}')        


if __name__ == "__main__":
    main()