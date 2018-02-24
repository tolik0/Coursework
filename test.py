"""
Function get_data_from_URL takes in a URL and parameters
for an API request and then returns the data (json).
Parameters must be passed in as a dictionary of key value pairs.
"""
import urllib.request
import urllib.parse
import json
from hidden import oauth
BASE_URL = "https://api.edamam.com/search?"
params = {"q": "chicken"}
def get_data_from_URL(base_url, params):
    params.update(oauth())
    params_str = urllib.parse.urlencode(params)
    request_url = base_url + params_str
    connection = urllib.request.urlopen(request_url)
    data = connection.read().decode()
    js = json.loads(data)
    new_data = {}
    for i in js["hits"]:
        new_data[i["recipe"]["label"]] = i["recipe"]["ingredientLines"]
    with open("file.json", "w", encoding = "utf-8") as file:
        json.dump(new_data, file, ensure_ascii = False, indent = 4)
    return new_data
data = get_data_from_URL(BASE_URL, params)