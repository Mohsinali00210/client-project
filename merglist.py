import pandas as pd
list1 = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Charlie"}
]

list2 = [
    {"id": 2, "age": 30},
    {"id": 3, "age": 22},
    {"id": 1, "age": 25}
]
# Create pandas DataFrames from the lists
df1 = pd.DataFrame(list1)
df2 = pd.DataFrame(list2)

# Perform the join (merge) on the "id" column
joined_df = pd.merge(df1, df2, on="id")

# Convert the result back to a list of dictionaries
joined_list = joined_df.to_dict(orient="records")

print(joined_list)