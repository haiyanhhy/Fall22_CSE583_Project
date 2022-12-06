import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

raw_data = pd.read_csv("data/redfin-sold-last-five-years/all.csv")

data = raw_data.dropna(subset=["SOLD DATE", "CITY", "ZIP OR POSTAL CODE", "PRICE", "STATUS"])
data["ZIP OR POSTAL CODE"] = data["ZIP OR POSTAL CODE"].astype(int)
data["SOLD DATE"] = pd.to_datetime(data["SOLD DATE"])
data["YEAR"] = data["SOLD DATE"].dt.year
# get year and month 
data["YEAR_MONTH"] = data["SOLD DATE"].dt.to_period('M').astype(str)

data.to_csv("data/redfin-sold-last-five-years/all_cleaned.csv")