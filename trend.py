from pytrends.request import TrendReq

# Initialize pytrends
pytrends = TrendReq(hl='en-US', tz=360)

# Build the payload for a specific keyword
keyword = 'data science'
pytrends.build_payload([keyword], cat=0, timeframe='today 12-m', geo='', gprop='')

# Retrieve interest over time
interest_over_time_df = pytrends.interest_over_time()

# Display the results
print(interest_over_time_df)
