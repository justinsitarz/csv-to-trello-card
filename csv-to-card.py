import requests
import csv
from serpapi import GoogleSearch
import pandas as pd
from google_images_search import GoogleImagesSearch
import math
import yaml


## Import large list of schools and school information from CSV to Trello



def read_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

def create_card(school, url):
    trello_url = "https://api.trello.com/1/cards"
    name = sanitize(school.get("School Name"))
    city = sanitize(school.get("City"))
    state =  sanitize(school.get("State"))
    loc = city + " ," + state
    grades = sanitize(school.get("Grades in 2021-2022"))
    notes = sanitize(school.get("Notes"))
    district = sanitize(school.get("District or CMO Name"))
    contacts = set_contacts(school.get("Contact 1"), school.get("Contact 2"), school.get("Contact 3"))
    query = {
        'key': config["CONFIG"]["TRELLO_KEY"],
        'token': config["CONFIG"]["TRELLO_TOKEN"],
        'idList': config["CONFIG"]["TRELLO_ID_LIST"],
        'name': name,
        'desc': 
            "**Location:** {} \x0A **Grades:** {} \x0A **Contacts:** {} \x0A**District:** {} \x0A**Notes:** {}".format(loc, grades, contacts, district, notes),
        'urlSource': get_image(name)
        }
    response = requests.request("POST", trello_url, params=query)

def sanitize(value):
    if isinstance(value, str):
        return value
    else:
        return 'N/A'

def set_contacts(c1, c2, c3):
    contact1 = sanitize(c1)
    contact2 = sanitize(c2)
    contact3 = sanitize(c3)
    contacts = ''
    if contact1 != 'N/A':
        contacts += contact1
    if contact2 != 'N/A':
        contacts += ', ' + contact2
    if contact3 != 'N/A':
        contacts += ', ' + contact3
    return contacts


# Retrieve the first hit from a google image search for the school name, to set as card cover pic

def get_image(query):
  gis = GoogleImagesSearch(google_api_key, project_key)
  _search_params = {'q': query,'num': 1,}
  gis.search(search_params = _search_params)
  res = gis.results()
  return res[0]._url

# Loop through all csv rows and create a card for each

def create_cards(data):
    for key, value in data.items():
      create_card(value)

def import_csv(filename):
    return pd.read_csv(filename).to_dict('index')

def main():
    config_filepath = 'config.yaml'
    config = read_yaml(config_filepath)
    csv_filepath = config["CONFIG"]["FILEPATH"]
    data = import_csv(csv_filepath)
    create_cards(data)


if __name__ == '__main__':
    main()