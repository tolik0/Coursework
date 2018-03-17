"""
Function get_data_from_URL takes in a URL and parameters
for an API request and then returns the data (json).
Parameters must be passed in as a dictionary of key value pairs.
"""
import urllib.request
import urllib.parse
import json
from hidden import oauth


def get_data_from_URL(base_url, params):
    """
    This function return dictionary with recipes
    Params - search query
    Base_url - url of API
    """
    # Information to authenticate
    params.update(oauth())
    params_str = urllib.parse.urlencode(params)
    # create url to look for recipes
    request_url = base_url + params_str
    connection = urllib.request.urlopen(request_url)
    data = connection.read().decode()
    js = json.loads(data)
    new_data = {}
    # take useful for us information - name, url of recipe and ingredients
    # with their weight
    for i in js["hits"]:
        label = i["recipe"]["label"]
        new_data[label] = {}
        new_data[label]["url"] = i["recipe"]["url"]
        new_data[label]["ingredients"] = i["recipe"]["ingredients"]
    # write information to file
    with open("file.json", "w", encoding="utf-8") as file:
        json.dump(new_data, file, ensure_ascii=False, indent=4)
    return new_data


def find_recipe():
    """
    Function to look for recipes
    """
    # url of API
    BASE_URL = "https://api.edamam.com/search?"
    # what we want to look for
    search = input("Input what you want to look for: ")
    params = {"q": search}
    # create dictionary with recipes
    data = get_data_from_URL(BASE_URL, params)
    # if we didn't find anything
    if len(data) == 0:
        print("Sorry we can't find this. Try one more time")
        find_recipe()

    # create dictionary with number of recipe as key and
    names = {}
    num = 1
    for name in data:
        names[num] = name
        num += 1

    # print list of recipes
    print("We find this recipes:")
    for number in names:
        print(str(number) + ".", names[number])

    # user choose one recipe
    input_number = 0
    while input_number not in names:
        try:
            input_number = int(
                input("Input number of recipe to see details: "))
        except:
            print("Try one more time.")

    # print detailed information about some recipe
    recipe = data[names[input_number]]
    print("You can look for this recipe here:", recipe["url"])
    print("Ingredients: ")
    for ingredient in recipe["ingredients"]:
        print("\t" + ingredient["text"] + ". Weight: " + str(ingredient[
                                                                 "weight"]))


find_recipe()
