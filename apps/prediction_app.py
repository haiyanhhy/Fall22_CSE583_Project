from flask import Flask, request, render_template
import pickle
from datetime import datetime
import os
DIRNAME = os.path.abspath(__file__ + "/../")


app = Flask(__name__)

# loading the model

with open(f'{DIRNAME}/ML_model/Price_Model', 'rb') as f:
    model = pickle.load(f)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def predict():
   try:
      """
      Required input for machine learning model
      1. PRICE
      2. SOLD MONTH_Number
      3. SOLD DATE_DAY
      4. SOLD YEAR
      5. PROPERTY TYPE
      6. BEDS
      7. BATHS
      8. LOCATION
      9. SQUARE FEET
      10. LOT SIZE
      11.YEAR BUILT
      """
      # syntax-->  var_name=request.form['<name which in present in html form(index.html)>']
      query_YEAR_BUILT = int(request.form['YEAR_BUILT'])
      query_SOLD_MONTH_Number = int(request.form['SOLD_MONTH_Number'])
      query_SOLD_DATE_DAY = int(request.form['SOLD_DATE_DAY'])
      query_SOLD_YEAR = request.form['SOLD_YEAR']
      query_BEDS = int(request.form['BEDS'])
      query_BATHS = int(request.form['BATHS'])
      query_LOT_SIZE = int(request.form['LOT_SIZE'])
      query_SQUARE_FEET = int(request.form['SQUARE_FEET'])
      query_LOCATION = request.form['LOCATION']  # multipul-selection
      query_PROPERTY_TYPE = request.form['PROPERTY_TYPE']  # multipul-selection
      
      # For renovation condition
      if query_SOLD_YEAR == "SOLD_YEAR_1":  # 2017
         SOLD_YEAR = 2017
      elif query_SOLD_YEAR == "SOLD_YEAR_2":  # 2018
         SOLD_YEAR = 2018
      elif query_SOLD_YEAR == "SOLD_YEAR_3":  # 2019
         SOLD_YEAR = 2019
      elif query_SOLD_YEAR == "SOLD_YEAR_4": # 2020
         SOLD_YEAR = 2020
      elif query_SOLD_YEAR == "SOLD_YEAR_5": # 2021
         SOLD_YEAR = 2021
      else:                 # SOLD_YEAR_6  # 2022
         SOLD_YEAR = 2022
      
      if SOLD_YEAR < query_YEAR_BUILT:
         return render_template('index.html')

      # For LOCATION
      LOCATION = int(query_LOCATION.split('_')[-1])

      # For PROPERTY TYPE
      PROPERTY_TYPE = int(query_PROPERTY_TYPE.split('_')[-1])
      model_data = [[query_SOLD_MONTH_Number, query_SOLD_DATE_DAY, SOLD_YEAR,
                     PROPERTY_TYPE, query_BEDS, query_BATHS,
                     query_SQUARE_FEET, query_LOT_SIZE, query_YEAR_BUILT, LOCATION]]
      result = model.predict(model_data)
      x = float(result)
      y = "{:.3f}".format(x)
      return render_template('index.html', results=y)
   except ValueError as v:
      print(v)
      return render_template('index.html')


if __name__ == "__main__":
   app.run()
