import requests
from bs4 import BeautifulSoup
import threading
import json

#fahrenheit to celcius T(C) = (T(F) - 32) * 5/9


class Classifier:
    def __init__(self):
        self.countries_url = "https://www.climatestotravel.com/world-climates/countries"
        self.session = None
        self.soup = None

        self.countries = []

    def getPage(self, url):
        self.session = requests.Session()
        page = self.session.get(url)
        self.soup = BeautifulSoup(page.content, "html.parser")
    
    def getCountries(self):
        self.getPage(self.countries_url)
        return [Country(a.text[1:]) for a in self.soup.find("div", class_="ElencoPaesi").find_all("a") if a["href"].count("/") == 2]
    
    def main(self):
        self.countries = self.getCountries()
        for country in self.countries:
            try:
                x = threading.Thread(target=country.getClimate, args=())
                x.start()
            except:
                pass
        
        for country in self.countries:
            country.riskAssessment()
        
        with open("countries.json", "r") as countries:
            countries = json.load(countries)
        
        for i in range(len(countries)):
            #print(str(countries[i]["Country"]) + self.countries[i])
            if str(countries[i]["Country"]) == self.countries[i].name:
                print(countries[i]["Country Code"])
            else:
                break


class Country(Classifier):
    def __init__(self, name):
        self.name = name
        self.climate_url = "https://www.climatestotravel.com" + "/climate/" + self.name
        self.climate = {}

    def getClimate(self):
        t = 0
        while t < 3:
            try:
                self.getPage(self.climate_url)
                
                avg_temperature = self.soup.find("table", class_="cities")
                avg_precipitation = self.soup.find("table", class_="precipit")
                sunshine = self.soup.find("table", class_="sole")

                months = [a.text for a in avg_temperature.find("tr", class_="title-table-new").find_all("th") if not a.text == "Month"]
                
                avg_temperature = dict(zip(months, list(zip([int(a.text) for a in avg_temperature.find("tr", class_="min-table").find_all("td")], [int(a.text) for a in avg_temperature.find("tr", class_="max-table").find_all("td")]))))
                avg_precipitation = dict(zip(months, list(zip([int(a.text) for a in avg_precipitation.find_all("tr", class_="precipit-table")[0].find_all("td")[:-1]], [int(a.text) for a in avg_precipitation.find_all("tr", class_="precipit-table")[2].find_all("td")[:-1]]))))
                sunshine = dict(zip(months, [int(a.text) for a in sunshine.find("tr", class_="sole-table").find_all("td")]))
                
                self.climate = {"Average Temperature" : avg_temperature,
                        "Average Precipitation" : avg_precipitation,
                        "Sunshine" : sunshine}
                #print(self.name + ": " + str(self.climate))
                return self.climate
            except:
                t += 1
    
    def riskAssessment(self):
        self.risk = 1
        print("Risk for " + self.name + ": " + str(self.risk))
 
if __name__ == "__main__":
    c = Classifier()
    c.main()