import requests
from bs4 import BeautifulSoup
import json


url = "http://techslides.com/list-of-countries-and-capitals"


session = requests.Session()
page = session.get(url)
soup = BeautifulSoup(page.content, "html.parser")

table = soup.find("table")

countries = table.find_all("tr")[1:]

labels = ["Country", "Capital", "Country Code", "Continent"]
for i in range(len(countries)):
    r = [a.text for a in countries[i].find_all("td")]
    countries[i] = dict(zip(labels, r[:2] + r[4:]))
    
print(countries[-1])

with open("countries.json", "w") as out_file:
    json.dump(countries, out_file, indent = 6)
