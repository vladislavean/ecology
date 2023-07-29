import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import numpy as np

class GetLinks:
    def __init__(self):
        req_country = requests.get("http://www.pogodaiklimat.ru/history.php?id=au")
        req_country.encoding = 'utf-8'
        soup_country = BeautifulSoup(req_country.text, "html.parser")
        self.states = soup_country.find(class_="big-blue-billet__list").find_all("a")  # <li class="big-blue-billet__list_link"></li>
        # подключение к сайту на странице Австралии и нахождение всех ссылок на cтранице
        
        
    def getStatesLinks(self) -> dict: # возвращение ссылок на все штаты
        states_links = {}
        for state in self.states:
            # <a href="/history.php?id=au&amp;region=vic">Виктория</a>
            state_name = re.search(r'>(.*?)<', str(state))
            state_link = re.search(r'href="(.+?)"', str(state))
            states_links[state_name.group(1)] = state_link.group(1).replace('®', '&reg')
        return states_links


    def getStationsLinks(self) -> dict: # возвразение ссылок на все станции, сортированных по штатам
        stations_links = {}
        for name in self.getStatesLinks():
            req_state = requests.get(f"http://www.pogodaiklimat.ru" + self.getStatesLinks()[name])
            req_state.encoding = 'utf-8'
            soup_state = BeautifulSoup(req_state.text, "html.parser")
            # http://www.pogodaiklimat.ru/history/au01297.htm 
            stations = soup_state.find(class_="big-blue-billet__list").find_all("a")
            d = {}
            for station in stations:
                station_link = re.search(r'href="(.+?)"', str(station)).group(1)
                station_name = re.search(r'>(.*?)<', str(station)).group(1)
                d[station_name] = station_link
            stations_links[name] = d
        return stations_links