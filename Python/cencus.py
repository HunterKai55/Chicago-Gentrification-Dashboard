import pandas as pd
import requests
import time

# Reads API key file
def read_api_key(filepath):
    with open(filepath, 'r') as f:
        return f.read().replace('\n','')

def get_columns(year, table):
    url = f'https://api.census.gov/data/{year}/acs/acs5/groups/{table}.json'
    columns = requests.get(url).json()['variables']
    return [c for c in columns]

# Builds the url and parameters
def request_build(api_key, year, columns, **kwargs):
    url = f'https://api.census.gov/data/{year}/acs/acs5'
    url_params = {'get':','.join(columns), **kwargs, 'key': api_key}
    return url, url_params

def get_request(url, url_params):
    response = requests.get(url, params=url_params)
    return response.json()

# Table giving race divided by hispanic heritage
# Table giving the income bracket
# Table giving sex by age
tables = ['B03002', 'B19001', 'B01001']
args  = {'for': 'tract:*', 'in': 'state:17 county:031'}

api_key = read_api_key('cbgov.txt') # Replace with your own apikey txt file [You will also get an email in which you need to activate the key for it to work]

# Sends requests as chunks
data = {}
for table in tables:
    for year in range(2009, 2024):
        columns = get_columns(year, table)
        chunks = []
        for i in range(0, len(columns), 45):
            chunks.append(columns[i:i+45])
        dataframes = []
        for chunk in chunks:
            url, url_params = request_build(api_key, year, chunk, **args)
            response = get_request(url, url_params)
            dataframes.append(pd.DataFrame(response[1:], columns=response[0]).set_index(['state', 'county', 'tract']))
            time.sleep(0.2)
        data[(table, year)] = pd.concat(dataframes, axis=1).reset_index()

# Combines the tables for each year by the type of table
dfs = {}
for table in tables:
    responses = []
    for year in range(2009, 2024):
        response = data[(table, year)]
        df = data[(table, year)]
        df['year'] = year
        responses.append(df)
    dfs[table] = pd.concat(responses, ignore_index=True)

for table in tables:
    filename = f"{table}.csv"
    dfs[table].to_csv(filename, index=False)
    print("saved " + table)