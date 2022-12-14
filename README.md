# Problem statement and project overview:
First-time house buyers might not have a good understanding about the housing market and need a visualization tool to easily identify market trend and choose a right neighborhood for them.
Leading real estate platforms such as Redfin and Zillow are providing users with home price prediction. However, users don’t have access to the assumptions and predictor variables used in the prediction model to evaluate its accuracy and reliability. 
Our project provides an interactive dashboard & open-source tool for house buyers to visualize and predict house prices in the next 3 months or based on the selected features. Even though our analysis focuses on house prices in Greater Seattle Area, users can access to our code and make changes accordingly to enhance the dashboard and the prediction model. 
# Organization of our project
<img width="970" alt="image" src="https://user-images.githubusercontent.com/115179760/207680372-9a10cf99-e484-47fb-8b9a-708931737963.png">

# Installation & Instruction
1.use visual environment environment.yml run commands:  
**python apps/prediction_app.py**  
2.open up a new terminal *without exiting* the previous process. \
3.input in the new terminal:  
**streamlit run apps/city_house.py**  
the streamlit visualization board will automatically popup in your the web browser  

To follow this project, please install the following locally:

JupyerLab
Python 3.8+
Python packages
pandas
yfinance
scikit-learn    
(we are supposed to install everything in visual env instead of asking users to install on their local drive)

Notice: \
1.It may take some time loading the website page and the visualization boards, please be patient :D \
2.When playing with the 'Price change analysis by cities' part, you should first choose the cities you are interested in the mult-selection bar, then the graphs will display successfully.

# Main technology used:
[![Python Package using Conda](https://github.com/haiyanhhy/Fall22_CSE583_Project/actions/workflows/python-package-conda.yml/badge.svg)](https://github.com/haiyanhhy/Fall22_CSE583_Project/actions/workflows/python-package-conda.yml)

Python, Streamlit, Folium, Flask, HTML, Plotly, Matplobib

# Data Source
For visualization workstream and house price prediction for home-builders, we use data downloaded from Redfin for Greater Seattle Area  for the last 5 years (2018-2022) (Link: https://github.com/haiyanhhy/Fall22_CSE583_Project/blob/main/data/redfin-sold-last-five-years/all_cleaned.csv)
For price prediction in the next 3 months workstream, we use a combination data set downloaded from FRED (Federal Reserve Economic Data) and Zillow. 
Link: https://github.com/haiyanhhy/Fall22_CSE583_Project/tree/main/Van%20Prediction%20Test/house_prices
Those are housing price and housing info data of Seattle and the nearby cities. Data are all downloaded from Redfin.\
All.csv is a file union all the seperate csv files, analysis could based on this single file.

# Use cases
Targeted users: Young professionals who are going to buy their first homes in Greater Seattle Area. 
Through our application, Uusers can: 
1. Look for historical house prices/sqft by city in Greater Seattle Area, depending on their search criteria (e.g. types of houses, sold year, city, # of bathrooms,...). Data is shown on a heatmap to assist buyers with a quick identification of the potential focused neighborhood which matches with their budgets
2. Grasp house prices changes in the last 5 years by city
3. Estimate house prices using random forest algorithm, based on the conditions selected by users (e.g. property type, number of rooms, lot size and the year the house was built, etc.) We also embedded the prediction model framework into the main page for ease of use. The algorithm achieved an accuracy rate of 76.8%.

5. (Xuqing to elaborate how to use the prediction here....)
In addition to that, we also predict house price trend in the next 3 months, using macro economic data such as CPI index in the US, median house sales price and mortgage interest rate to predict the change in house price. 
Instructions
# Addressing key challenges & Future work
1. Our dashboard and analysis are using historical data which we downloaded from Redfin, Fred and Zillow. Therefore, the dashboard is not automatically updated to show the latest data to users.
2. Streamlit has speed issues. The entire Python script is re-run in the browser every time users interact with the application.
3. There is room for improvement in terms of User interface: number of bathrooms in the side bar should be 1,2,3 and 4+ instead of 1 to 299 like at the moment
4. Regarding house price prediction part, users need to run a separate command line within the terminal to load the prediction part.

Future work: if time allows, we would love to have an API integration so that the dashboard can be automatically updated and show latest data. We also want to explore new tools which provides more flexibility and better loading speed than Streamlit and optimize the user interface of the tool.
# References
When predicting house price in the next 3 months, we follow instructions in a video made by Dataquest on Youtube. 
Link: https://www.youtube.com/watch?v=IsoW7_X3j5A&t=778s
We then customize the data to focus the analysis on Seattle area and using the latest data till Oct 2022.
**
(Everyone to review and add sources we use for references)**
