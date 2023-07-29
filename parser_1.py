import requests
from bs4 import BeautifulSoup
import numpy as np


class Parser:
    def __init__(self, selectedState: str, stateStationLinks: dict):
        self.stationLink = stateStationLinks[selectedState]
        self.selectedState = selectedState

    def _parseTab(self, dateTab, dataTab):
        listOfYears = []
        listOfVal = []
        rows = dateTab.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            for col in cols:
                listOfYears.append(col.text)
        column_number = 12
        rows = dataTab.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) > column_number:
                if cols[column_number].text == "за год":
                    listOfVal.append(cols[column_number].text)
                    continue
                if float(cols[column_number].text) != 999.9:
                    listOfVal.append(float(cols[column_number].text))
                else:
                    listOfVal.append(None)
        del listOfYears[0]
        del listOfVal[0]
        return listOfYears, listOfVal

    def getStateTemps(self) -> dict:
        data = {}
        for link in self.stationLink.values():
            req = requests.get("http://www.pogodaiklimat.ru" + link)
            req.encoding = 'utf-8'
            soup = BeautifulSoup(req.text, "html.parser")
            dateTab = soup.findAll("table")[0]
            dataTab = soup.findAll("table")[1]
            listOfYears, listOfVal = self._parseTab(dateTab, dataTab)
            for i in range(len(listOfYears)):
                if listOfYears[i] not in data and listOfVal[i] != None:
                    data[listOfYears[i]] = []
                if listOfVal[i] != None:
                    data[listOfYears[i]].append(listOfVal[i])
            
        for key, val in data.items():
            data[key] = np.mean(val)
       
        mean_temp = np.mean(list(data.values()))
        for key, val in data.items():
            data[key] = [val, val - mean_temp]
        mean_dev = np.mean([i[1] for i in data.values()])
        data = dict(sorted(data.items()))
        return {self.selectedState: [data, mean_temp, mean_dev]}
