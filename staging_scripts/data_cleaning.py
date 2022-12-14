import pandas as pd

raw_data = pd.read_csv("data/redfin-sold-last-five-years/all.csv")

data = raw_data.dropna(subset=["SOLD DATE", "CITY", "ZIP OR POSTAL CODE", "PRICE", "STATUS"])
data["ZIP OR POSTAL CODE"] = data["ZIP OR POSTAL CODE"].astype(int)
data["SOLD DATE"] = pd.to_datetime(data["SOLD DATE"])
data["YEAR"] = data["SOLD DATE"].dt.year
# get year and month
data["YEAR_MONTH"] = data["SOLD DATE"].dt.to_period('M').astype(str)

# categorize propoerty types
data['PROPERTY TYPE RAW'] = data['PROPERTY TYPE']


def categorise(row):
    if row['PROPERTY TYPE RAW'] == 'Single Family Residential':
        return 'Single Family Residential'
    elif row['PROPERTY TYPE RAW'] == 'Multi-Family (2-4 Unit)' or row['PROPERTY TYPE RAW'] == 'Multi-Family (5+ Unit)':
        return 'Multi-Family Residential'
    elif row['PROPERTY TYPE RAW'] == 'Condo/Co-op' or row['PROPERTY TYPE RAW'] == 'Co-op':
        return 'Condo/Co-op'
    elif row['PROPERTY TYPE RAW'] == 'Townhouse':
        return 'Townhouse'
    elif row['PROPERTY TYPE RAW'] == 'Mobile/Manufactured Home' or row['PROPERTY TYPE RAW'] == 'Ranch' or \
    row['PROPERTY TYPE RAW'] == 'Timeshare' or row['PROPERTY TYPE RAW'] == 'Parking':
        return 'Business/Industry'
    elif row['PROPERTY TYPE RAW'] == 'Other' or row['PROPERTY TYPE RAW'] == 'Vacant Land':
        return 'Land/Other'
    elif row['PROPERTY TYPE RAW'] == 'Unknown':
        return 'Unknown'
    return


data['PROPERTY TYPE'] = data.apply(lambda row: categorise(row), axis=1)

data.to_csv("data/redfin-sold-last-five-years/all_cleaned.csv")
