from selenium import webdriver                              #for web scraping
from selenium.webdriver.support.ui import WebDriverWait     #importing wait method
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import re
import time
import pandas as pd
import sys
import requests
from selenium.webdriver.common.action_chains import ActionChains


####DEFINING CONSTANTS######
#Allowed airports:
PORTS = ['LAX','SFO','PHX','SEA','DEN','ATL','ORD','BOS','IAD','JFK']   #all nodes in graph
INTERMEDPORTS = ['SFO','PHX','SEA','DEN','ATL','ORD','BOS','IAD']       #all nodes other than source and destination
#Sources = ['LAX']+INTERMEDPORTS                                         #all possible source nodes for directed flights
Destinations = INTERMEDPORTS+['JFK']                                    #all possible destination nodes for flights
AIRLINES = ['United','Delta','AA']                                      #all airline names
DEPDATE = '01/06/2020'                                                  #Departure Date


#LAX to SFO
#United_Url = 'https://www.united.com/ual/en/us/flight-search/book-a-flight/results/rev?f='+source+'&t='+dest+'&d=2020-01-06&EditSearchCartId=39F28944-0DF5-4521-850D-4BBDBE51ED60&tt=1&st=bestmatches&cbm=-1&cbm2=-1&sc=1&px=1&taxng=1&idx=1'
#United_Url = 'https://www.united.com/ual/en/us/flight-search/book-a-flight/results/rev?f=LAX&t=SFO&d=2020-01-06&tt=1&st=bestmatches&cbm=-1&cbm2=-1&cp=1&sc=1&px=1&taxng=1&idx=1'


#United url:
United_home_url = 'https://www.united.com/web/en-US/apps/travel/timetable/default.aspx'

Flightlist = []





Sources = ['ORD','BOS','IAD']
for source in Sources:
    for dest in Destinations:
        if source!=dest:
            driver = webdriver.Chrome('/Users/ahmedkoptanmacbook/Imp/ASU/Course Content/Fall 2019/CSE 551 Algorithms/Project/chromedriver')
            driver.get(United_home_url)
            driver.implicitly_wait(100)
            time.sleep(1)

            #print(driver.current_url)

            s = driver.find_element_by_id('ctl00_ContentInfo_OandD_Origin_txtOrigin')
            driver.implicitly_wait(100)
            s.send_keys(source)
            time.sleep(1)
            d = driver.find_element_by_id('ctl00_ContentInfo_OandD_Destination_txtDestination')
            driver.implicitly_wait(100)
            d.send_keys(dest)
            time.sleep(1)
            driver.find_element_by_id('ctl00_ContentInfo_Depdate1_txtDptDate').clear()
            driver.implicitly_wait(100)
            date = driver.find_element_by_id('ctl00_ContentInfo_Depdate1_txtDptDate')
            driver.implicitly_wait(100)
            date.send_keys(DEPDATE)
            time.sleep(1)
            nonstop = driver.find_element_by_id('ctl00_ContentInfo_Direct1_chkFltOpt')
            driver.implicitly_wait(100)
            nonstop.click()
            time.sleep(1)
            search = driver.find_element_by_id('ctl00_ContentInfo_searchbutton')
            driver.implicitly_wait(100)
            search.click()
            driver.implicitly_wait(100)
            time.sleep(5)
            page_soup = BeautifulSoup(driver.page_source,'html.parser')
            data_soup = page_soup.find_all('tbody')
            data_soup = data_soup[7:]



            #if len(data_soup[i])<= 2:, then flight is operated by United, and is non stop

            #if data_soup[i].find_all('strong', attrs={'class': 'timeArrive'})[-1].parent.contents[1] != ' ':, then flight arrives after midnight on the 7th



            #arrival time is
            # arr_time = data_soup[i].find_all('strong', attrs={'class': 'timeArrive'})[0].text

            #arrival port is
            #data_soup[i].find_all('td', attrs={'class': 'tdArrive'})[-1].contents[5].text.strip()
            # arr_port = re.search('\(([A-Z]+)\)',data_soup[0].find_all('td', attrs={'class': 'tdArrive'})[-1].contents[5].text.strip()).group(1)

            #departure time is
            # dep_time = data_soup[5].find_all('strong', attrs={'class':'timeDepartItitial'})[0].text

            #departure port is
            # dep_port = re.search('\(([A-Z]+)\)',data_soup[i].find_all('td', attrs={'class': 'tdDepart'})[0].contents[5].text.strip()).group(1)

            #craft type is
            # craft_type = re.search('Aircraft: ([\w\d\s-]+)',data_soup[i].find_all('td',attrs={'class':'tdSegmentDtl'})[-1].text.strip()).group(1)

            #flight number is
            # flightn = re.search('Flight: ([\w\d-]+)',data_soup[i].find_all('td',attrs={'class':'tdSegmentDtl'})[0].text.strip()).group(1)

            if not data_soup:
                print('No data found on page')

            for i in range(len(data_soup)):
                # then flight is operated by United, and is non stop
                if len(data_soup[i]) <= 2:
                    #check if flight doesn't arrives after midnight on the 7th
                    if data_soup[i].find_all('strong', attrs={'class': 'timeArrive'})[-1].parent.contents[1] == ' ':
                        # check if dep port and arr port are within our PORTS
                        if re.search('\(([A-Z]+)\)',data_soup[i].find_all('td', attrs={'class': 'tdDepart'})[0].contents[5].text.strip()).group(1) == source\
                            and re.search('\(([A-Z]+)\)',data_soup[0].find_all('td', attrs={'class': 'tdArrive'})[-1].contents[5].text.strip()).group(1)==dest:
                            flight = []
                            # get flight number and airline name
                            flightn = re.search('Flight: ([\w\d-]+)',data_soup[i].find_all('td',attrs={'class':'tdSegmentDtl'})[0].text.strip()).group(1)
                            flight.append(flightn)
                            # Airline name is Delta Airlines
                            airline = "United Airlines"
                            flight.append(airline)
                            # get departure airport and departure time
                            dep_time = data_soup[i].find_all('strong', attrs={'class':'timeDepartItitial'})[0].text
                            flight.append(dep_time)
                            dep_port = re.search('\(([A-Z]+)\)',data_soup[i].find_all('td', attrs={'class': 'tdDepart'})[0].contents[5].text.strip()).group(1).strip()
                            flight.append(dep_port)

                            # get arrival airport and arrival time
                            arr_time = data_soup[i].find_all('strong', attrs={'class': 'timeArrive'})[0].text
                            flight.append(arr_time)
                            arr_port = re.search('\(([A-Z]+)\)',data_soup[i].find_all('td', attrs={'class': 'tdArrive'})[-1].contents[5].text.strip()).group(1).strip()
                            flight.append(arr_port)

                            # get aircraft type
                            craft_type = re.search('Aircraft: ([\w\d\s-]+)',data_soup[i].find_all('td',attrs={'class':'tdSegmentDtl'})[-1].text.strip()).group(1).strip()
                            flight.append(craft_type)

                            print('Flight # is:', flightn)
                            print('Airline is:', airline)
                            print('Departure time is:', dep_time)
                            print('Departure port is:', dep_port)
                            print('Arrival time is:', arr_time)
                            print('Arrival port is:', arr_port)
                            print('Aircraft type is:', craft_type)
                            print('\n')

                            if flight not in Flightlist:
                                Flightlist.append(flight)

                        else:
                            print('Departure port or arrival port are not within our ports\n')
                    else:
                        print("Flight arrives after midnight\n")
                else:
                    print("Flight is not operated by United, or has 1 stop")
            time.sleep(5)
            driver.close()
    df = pd.DataFrame(Flightlist,columns=['flightn', 'airline', 'dep_time', 'dep_port', 'arr_time','arr_port','craft_type'])
    df.to_csv('Unitedflights.csv', index=False, header=True)

df['dep_time'] = df['dep_time'].replace(to_replace='([p])[.]([m])[.]',value='PM',regex=True).replace(to_replace='([a])[.]([m])[.]',value='AM',regex=True)
df['arr_time'] = df['arr_time'].replace(to_replace='([p])[.]([m])[.]',value='PM',regex=True).replace(to_replace='([a])[.]([m])[.]',value='AM',regex=True)
