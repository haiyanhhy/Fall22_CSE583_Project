# This is a file for initail data setting up, we can download data from Redfin by seperate URLs.
# We need to preprocess and combine all the dataset together.

import pandas as pd
import glob

# generate the link for downloading the data
for i in range(40814, 40878):
    print(f"https://www.redfin.com/stingray/api/gis-csv?al=3&has_dishwasher=false&has_laundry_facility=false&has_laundry_hookups=false&has_parking=false&has_pool=false&has_short_term_lease=false&include_pending_homes=false&isRentals=false&is_furnished=false&market=seattle&num_homes=20000&ord=redfin-recommended-asc&page_number=1&region_id={i}&region_type=2&sold_within_days=1825&status=1&travel_with_traffic=false&travel_within_region=false&uipt=1,2,3,4,5,6,7,8&utilities_included=false&v=8")


# preprocessing the data
for file in glob.glob("data/redfin-sold-last-five-years/seattle/*.csv"):
    data = open(file, "r").read()
    data = data.strip()
    if data.endswith("Over 500 results. Try zooming in or modifying your search options."):
        data = data.rstrip("Over 500 results. Try zooming in or modifying your search options.")
    with open(file, "w") as fout:
        fout.write(data)

# preprocessing the seattle data
seattle_data_lines = []
lines_set = set()
header_line = None
for file in glob.glob("data/redfin-sold-last-five-years/seattle/*.csv"):
    lines = [l.strip() for l in open(file, "r").readlines()]
    if header_line is None:
        header_line = lines[0]
    else:
        assert header_line == lines[0], header_line + " != " + lines[0]
    for line in lines[1:]:
        if line not in lines_set:
            seattle_data_lines.append(line)
            lines_set.add(line)
with open("data/redfin-sold-last-five-years/seattle.csv", "w") as fout:
    fout.write(header_line + "\n")
    fout.write("\n".join(seattle_data_lines))

# merge all the dataset together
all_data_lines = []
lines_set = set()
header_line = None
for file in glob.glob("data/redfin-sold-last-five-years/*.csv"):
    lines = [x.strip() for x in open(file, "r").readlines()]
    if header_line is None:
        header_line = lines[0]
    else:
        assert header_line == lines[0], header_line + " != " + lines[0]
    for line in lines[1:]:
        if line not in lines_set:
            all_data_lines.append(line)
            lines_set.add(line)
with open("data/redfin-sold-last-five-years/all.csv", "w") as fout:
    fout.write(header_line + "\n")
    fout.write("\n".join(all_data_lines))

raw_data = pd.read_csv("data/redfin-sold-last-five-years/all.csv")
