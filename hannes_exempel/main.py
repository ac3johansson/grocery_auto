import json
import re

import requests
from bs4 import BeautifulSoup


def get_ld_json(url: str) -> dict:
    parser = "html.parser"
    req = requests.get(url)
    soup = BeautifulSoup(req.text, parser)
    return json.loads("".join(soup.find("script", {"type": "application/ld+json"}).contents))

# Function to parse a row and create a dictionary


def parse_row(row):
    # Join the row into a single string for easier regex matching
    row_str = ' '.join(row)

    # Regex to capture amounts (e.g., 1, 1 1/2), units (e.g., dl, tsk), and ingredient
    # This will match 1, 1 1/2, 1/2, etc.
    amount_pattern = r'(\d+\s\d/\d|\d+/\d+|\d+(\s\d+)?|\d+(\.\d+)?)'
    # This will match a word (likely units like dl, msk)
    unit_pattern = r'(\b[a-zA-Zåäö]+\b)'

    # Try to find the amount (can be fraction or whole number)
    amount_match = re.search(amount_pattern, row_str)
    amount = amount_match.group(0) if amount_match else None

    # Find the unit (could be something like dl, tsk, or something else)
    unit_match = re.search(unit_pattern, row_str)
    unit = unit_match.group(0) if unit_match else None

    # Everything after the amount and unit is the ingredient description
    if amount and unit:
        start_idx = row_str.find(amount) + len(amount)
        start_idx = row_str.find(unit, start_idx) + len(unit)
        ingredient = row_str[start_idx:].strip()
    else:
        ingredient = ' '.join(row).strip()

    return {'vad': ingredient, 'antal': amount, 'enhet': unit}


def create_dict(url):
    data = get_ld_json(url)

    d = {"url": url}
    d['name'] = data['name']
    d['description'] = data['description']
    d['image'] = data['image']

    i = []
    for ingrediens in data['recipeIngredient']:
        temp_row = ingrediens.split()
        i.append(parse_row(temp_row))

    d['ingredienser'] = i
    return d


urls = [
    "https://www.ica.se/recept/pasta-med-kramig-ost-och-skinksas-725815/",
    "https://www.ica.se/recept/kottfarssas-med-spaghetti-720707/",
    "https://www.ica.se/recept/klassisk-lasagne-679675/",
    "https://www.ica.se/recept/kladdig-kladdkaka-722982/",
    "https://www.ica.se/recept/kramig-kycklinggryta-med-soltorkade-tomater-723346/",
    "https://www.ica.se/recept/kryddstekt-rostbiff-med-kaprisgremolata-och-aioli-750294/",
    "https://www.ica.se/recept/bakade-betor-med-miso-750286/",
    "https://www.ica.se/recept/hel-kyckling-med-linser-och-salsa-verde-750367/"
        ]
recipes = {"recipes": []} 
for url in urls:
    d = create_dict(url)
    recipes['recipes'].append(d)
    
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(recipes,f)