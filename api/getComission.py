import pandas as pd
import difflib
import re
import json

def flatten_categories(data):
    rows = []
    
    for entry in data:
        for level2 in entry['level2TabList']:
            level2_id = level2['categoryId']
            level2_name = level2['categoryName']
            level2_url = level2['categoryUrl']
            
            # Append Level 2 info
            rows.append({
                "category_id": level2_id,
                "category_name": level2_name,
                "category_url": level2_url
            })
            
            # Append Level 3 info if available
            if 'level3TabList' in level2:
                for level3 in level2['level3TabList']:
                   
                    rows.append({
                        "category_id": level3['categoryId'],
                        "category_name": level2_name+" "+level3['categoryName'],
                        "category_url": level3['categoryUrl']
                    })
    
    return pd.DataFrame(rows)

# Function to preprocess both the query and data (remove spaces and '--' and convert to lowercase)
def preprocess_string(s):
    # Remove spaces and '--' by using separate regex replacements
    s = re.sub(r'-', ' ', s)  # Remove all spaces
    return s



def find_best_match(query, df):
    """Find the best match ignoring spaces and '--'."""
    query = preprocess_string(query)
    
    # Use difflib to find all close matches
    all_matches = difflib.get_close_matches(query, df['Processed_Category'], n=5, cutoff=0.5)  # Increase n to get more matches
    
    if all_matches:
        
        # Calculate similarity score for each match
        match_scores = []
        for match in all_matches:
            score = difflib.SequenceMatcher(None, query, match).ratio()
            
            match_scores.append((match, score))
        
        # Sort matches by the similarity score (higher is better)
        match_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Return the most similar match
        best_match = match_scores[0]
        # Find the original category and value based on the processed match
        matched_row = df[df['Processed_Category'] == best_match[0]]
        return matched_row['Category'].iloc[0], matched_row['Value'].iloc[0], best_match[1]
    
    return None, None, None
def findCategoriesCommision(category_array):

    total_categories=0
    matched_categories=0
    mydata=[]
        
    data=[]
    with open('./api/daraz_category.json', 'r',encoding='utf-8') as file:
        data = json.load(file)
    data_dict=[]
    with open('./api/daraz_commission.json', 'r',encoding='utf-8') as file:
        data_dict = json.load(file)
    # Create DataFrame
    category_df = flatten_categories(data)
    filtered_df = category_df.loc[category_df['category_id'].isin(category_array)]
    print(filtered_df)

    # Convert to a pandas DataFrame for easier manipulation
    df = pd.DataFrame(list(data_dict.items()), columns=['Category', 'Value'])

    # Preprocess the data
    df['Processed_Category'] = df['Category'].apply(preprocess_string)
    SumCategoryUrls = " ".join(filtered_df["category_url"])
    print("category urls ",SumCategoryUrls)
    for index,category in filtered_df.iterrows():
        query=category["category_url"]
        print(query)
        best_match_category, best_match_value, similarity_score = find_best_match(query, df)
        total_categories+=1
        if best_match_category:
            matched_categories+=1
            mydata.append({
                "category_id":category["category_id"],
                "category_url":category["category_url"],
                "commission":best_match_value,
            })
            print(f"index: {index} Best match found: {best_match_category} with value {best_match_value}, similarity score: {similarity_score}")
        else:
            query = category["category_name"]
            print("category Name is",query)
            best_match_category, best_match_value, similarity_score = find_best_match(query, df)
            
            if best_match_category:
                mydata.append({
                    "category_id":category["category_id"],
                    "category_url":category["category_url"],
                    "commission":best_match_value,
                })
                print(f"index: {index} Best match found: {best_match_category} with value {best_match_value}, similarity score: {similarity_score}")
            
            print("No relevant match found.")
    print("total categories: ",total_categories)
    print("matched categories: ",matched_categories)
    print("my data",mydata)
    print("category array ",category_array)
    return mydata

                    