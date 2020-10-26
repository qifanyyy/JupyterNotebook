from selenium import webdriver                              #for web scraping
from selenium.webdriver.support.ui import WebDriverWait     #importing wait method
from bs4 import BeautifulSoup
import time
import pandas as pd

#Allowed airports:
PORTS = ['LAX','SFO','PHX','SEA','DEN','ATL','ORD','BOS','IAD','JFK']   #all nodes in graph
INTERMEDPORTS = ['SFO','PHX','SEA','DEN','ATL','ORD','BOS','IAD']       #all nodes other than source and destination
Sources = ['LAX']+INTERMEDPORTS                                         #all possible source nodes for directed flights
Destinations = INTERMEDPORTS+['JFK']                                    #all possible destination nodes for flights
AIRLINES = ['United','Delta','AA']                                      #all airline names
DEPDATE = '01/06/2020'                                                  #Departure Date


#AA url:
AA_home_url = "https://www.aa.com/travelInformation/flights/schedule"


#Appending all possible flights (edges) to this list
Flightlist = []


###############################################EXTRACTING AA INFORMATION################################################
for source in Sources:
    for dest in Destinations:
        if dest!=source:
            driver = webdriver.Chrome(
                '/Users/ahmedkoptanmacbook/Imp/ASU/Course Content/Fall 2019/CSE 551 Algorithms/Project/chromedriver')

            driver.get(AA_home_url)
            driver.implicitly_wait(100)

            origin = driver.find_element_by_id('originAirport')
            origin.clear()
            origin.send_keys(source)

            destination = driver.find_element_by_id('destinationAirport')
            destination.clear()
            destination.send_keys(dest)

            date = driver.find_element_by_id('departureDateStr')
            date.clear()
            date.send_keys(DEPDATE)


            #showonlyam = driver.find_element_by_xpath(".//*[contains(text(), ' Show only American flights')]")
            #showonlyam.click()

            mysubmit = driver.find_element_by_id('flightSchedulesSearchButton')
            mysubmit.submit()

            # Wait for search to end and then extend search to see all results
            driver.implicitly_wait(200)
            while driver.find_element_by_id('moreFlightsExpanded').get_attribute('value')!='true':
                print('more flights button found')
                more_flights = driver.find_elements_by_id('moreFlightsBtn')
                if not more_flights:
                    print("no more flights to show")
                    break
                else:
                    more_flights[0].click()
                    print('more flights button clicked')
                    time.sleep(5)
                    driver.implicitly_wait(200)


            # Get HTML text to get flight data
            page_soup = BeautifulSoup(driver.page_source, 'html.parser')
            data_soup = page_soup.find_all('tbody',attrs={'id' : 'resultsTableBody'})
            oneseg_soup = page_soup.find_all('tr', attrs={'class': 'oneSegment'})
            #firstseg_soup = page_soup.find_all('tr', attrs={'class': 'firstSegment'})
            #lastseg_soup = page_soup.find_all('tr', attrs={'class': 'lastSegment'})

            # data structure in all seg soups (not just oneseg)
            # 1 carrierIcon info: oneseg_soup[i].contents[1] not needed

            # 3 flightInfo (5 contents, 1 and 3 are flight number and airline) : oneseg_soup[i].contents[3]

            # 5 departure (5 contents, 1 and 3 are departure time and departure airport) : oneseg_soup[0].contents[5]
            # len(lastseg_soup[i].contents[7]) for oneseg_soup and lastseg_soup is 7 for arrival beyond midnight, and 5 for the rest

            # 7 arrival (5 contents, 1 and 3 are arrival time and arrival airport) : oneseg_soup[0].contents[7]

            # 9 carrierInfo not needed

            # 11 aircraft type (1 is aircraft type): oneseg_soup[0].contents[11]

            # 13 useless


            print('Direct flights:\n')
            for i in range(len(oneseg_soup)):
                #check if flight is operated by other airline
                if not oneseg_soup[i].find_all('td',attrs={'class':'flightInfo'})[0].div:
                    # check if flight arrives before midnight on the 6th
                    if len(oneseg_soup[i].contents[7]) < 7:
                        #check if flight dep port and arrive port are equal to source and dest
                        if oneseg_soup[i].contents[5].contents[3].text.strip() == source and oneseg_soup[i].contents[7].contents[3].text.strip() == dest:
                            flight = []
                            # get flight number and airline name
                            flightn = oneseg_soup[i].contents[3].contents[1].text.strip()
                            flight.append(flightn)
                            airline = oneseg_soup[i].contents[3].contents[3].text.strip()
                            flight.append(airline)
                            # get departure airport and departure time
                            dep_time = oneseg_soup[i].contents[5].contents[1].text.strip()
                            flight.append(dep_time)
                            dep_port = oneseg_soup[i].contents[5].contents[3].text.strip()
                            flight.append(dep_port)
                            # get arrival airport and arrival time
                            arr_time = oneseg_soup[i].contents[7].contents[1].text.strip()
                            flight.append(arr_time)
                            arr_port = oneseg_soup[i].contents[7].contents[3].text.strip()
                            flight.append(arr_port)
                            # get aircraft type
                            craft_type = oneseg_soup[i].contents[11].contents[1].text.strip()
                            flight.append(craft_type)
                            print('Flight # is:', flightn)
                            print('Airline is:', airline)
                            print('Departure time is:', dep_time)
                            print('Departure port is:', dep_port)
                            print('Arrival time is:', arr_time)
                            print('Arrival port is:', arr_port)
                            print('Aircraft type is:', craft_type)
                            print('\n')
                            Flightlist.append(flight)
                        else:
                            print("source and destination of flight are not within PORTS")
                else:
                    print("Flight is operated by another airline")
            driver.close()


df = pd.DataFrame(Flightlist,
                         columns=['flightn', 'airline', 'dep_time', 'dep_port', 'arr_time', 'arr_port',
                                  'craft_type'])

df = df.drop(df[df['airline']!='American Airlines'].index,axis=0)
df = df.reset_index(drop = True)

df.to_csv('AAflights.csv',index=False,header=True)

#######dropping off wrong flights, not needed anymore#######
"""
L = []
for p in range(len(df)):
    if(df.iloc[p,3] not in PORTS or df.iloc[p,5] not in PORTS):
        L.append(p)
df = df.drop(L,axis=0)
"""

####Append AA to flight numbers in combined file

























####BACKUP of initial scraping process#########

"""


driver = webdriver.Chrome('/Users/ahmedkoptanmacbook/Imp/ASU/Course Content/Fall 2019/CSE 551 Algorithms/Project/chromedriver')

driver.get(AA_home_url)
driver.implicitly_wait(100)

origin = driver.find_element_by_id('originAirport')
origin.clear()
origin.send_keys('LAX')

destination = driver.find_element_by_id('destinationAirport')
destination.clear()
destination.send_keys('JFK')

date = driver.find_element_by_id('departureDateStr')
date.clear()
date.send_keys('01/06/2020')

showonlyam = driver.find_element_by_xpath(".//*[contains(text(), ' Show only American flights')]")
showonlyam.click()

mysubmit = driver.find_element_by_id('flightSchedulesSearchButton')
mysubmit.submit()

#element = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id('iframe_container'))

#Wait for search to end and then extend search to see all results
driver.implicitly_wait(200)
more_flights = driver.find_element_by_id('moreFlightsBtn')
more_flights.click()
driver.implicitly_wait(200)
time.sleep(10)

#Get HTML text to get flight data
page_soup = BeautifulSoup(driver.page_source,'html.parser')
#data_soup = page_soup.find_all('tbody',attrs={'id' : 'resultsTableBody'})
oneseg_soup = page_soup.find_all('tr',attrs={'class' : 'oneSegment'})
firstseg_soup = page_soup.find_all('tr',attrs={'class' : 'firstSegment'})
lastseg_soup = page_soup.find_all('tr',attrs={'class' : 'lastSegment'})

#data structure in all seg soups (not just oneseg)
# 1 carrierIcon info: oneseg_soup[i].contents[1] not needed

# 3 flightInfo (5 contents, 1 and 3 are flight number and airline) : oneseg_soup[i].contents[3]

# 5 departure (5 contents, 1 and 3 are departure time and departure airport) : oneseg_soup[0].contents[5]
# len(lastseg_soup[i].contents[7]) for oneseg_soup and lastseg_soup is 7 for arrival beyond midnight, and 5 for the rest

# 7 arrival (5 contents, 1 and 3 are arrival time and arrival airport) : oneseg_soup[0].contents[7]

# 9 carrierInfo not needed

# 11 aircraft type (1 is aircraft type): oneseg_soup[0].contents[11]

# 13 useless

#Appending to flight list
Flightlist = []

print('Direct flights:\n')
for i in range(len(oneseg_soup)):
    #check if flight arrives before midnight on the 6th
    if len(oneseg_soup[i].contents[7]) < 7 :
        flight = []
        # get flight number and airline name
        flightn = oneseg_soup[i].contents[3].contents[1].text.strip()
        flight.append(flightn)
        airline = oneseg_soup[i].contents[3].contents[3].text.strip()
        flight.append(airline)
        # get departure airport and departure time
        dep_time = oneseg_soup[i].contents[5].contents[1].text.strip()
        flight.append(dep_time)
        dep_port = oneseg_soup[i].contents[5].contents[3].text.strip()
        flight.append(dep_port)
        # get arrival airport and arrival time
        arr_time = oneseg_soup[i].contents[7].contents[1].text.strip()
        flight.append(arr_time)
        arr_port = oneseg_soup[i].contents[7].contents[3].text.strip()
        flight.append(arr_port)
        # get aircraft type
        craft_type = oneseg_soup[i].contents[11].contents[1].text.strip()
        flight.append(craft_type)
        print('Flight # is:',flightn)
        print('Airline is:', airline)
        print('Departure time is:',dep_time)
        print('Departure port is:', dep_port)
        print('Arrival time is:',arr_time)
        print('Arrival port is:',arr_port)
        print('Aircraft type is:',craft_type)
        print('\n')
        Flightlist.append(flight)


print('One Stop flights: \n')
count = 0
for i in range(len(lastseg_soup)):
    print('iteration is',i)
    #check if flight arrives before midnight on the 6th
    if len(lastseg_soup[i].contents[7]) < 7 and firstseg_soup[i].contents[7].contents[3].text.strip() in INTERMEDPORTS:
        # get flight number and airline name
        flight = []
        flightn1 = firstseg_soup[i].contents[3].contents[1].text.strip()
        flight.append(flightn1)
        airline1 = firstseg_soup[i].contents[3].contents[3].text.strip()
        flight.append(airline1)
        # get departure airport and departure time
        dep_time1 = firstseg_soup[i].contents[5].contents[1].text.strip()
        flight.append(dep_time1)
        dep_port1 = firstseg_soup[i].contents[5].contents[3].text.strip()
        flight.append(dep_port1)
        # get arrival airport and arrival time
        arr_time1 = firstseg_soup[i].contents[7].contents[1].text.strip()
        flight.append(arr_time1)
        arr_port1 = firstseg_soup[i].contents[7].contents[3].text.strip()
        flight.append(arr_port1)
        # get aircraft type
        craft_type1 = firstseg_soup[i].contents[11].contents[1].text.strip()
        flight.append(craft_type1)
        print('First flight is:')
        print('Flight # is:', flightn1)
        print('Airline is:', airline1)
        print('Departure time is:', dep_time1)
        print('Departure port is:', dep_port1)
        print('Arrival time is:', arr_time1)
        print('Arrival port is:', arr_port1)
        print('Aircraft type is:', craft_type1)
        if flight not in Flightlist:
            Flightlist.append(flight)


        # get flight number and airline name
        flight = []
        flightn2 = lastseg_soup[i].contents[3].contents[1].text.strip()
        flight.append(flightn2)
        airline2 = lastseg_soup[i].contents[3].contents[3].text.strip()
        flight.append(airline2)
        # get departure airport and departure time
        dep_time2 = lastseg_soup[i].contents[5].contents[1].text.strip()
        flight.append(dep_time2)
        dep_port2 = lastseg_soup[i].contents[5].contents[3].text.strip()
        flight.append(dep_port2)
        # get arrival airport and arrival time
        arr_time2 = lastseg_soup[i].contents[7].contents[1].text.strip()
        flight.append(arr_time2)
        arr_port2 = lastseg_soup[i].contents[7].contents[3].text.strip()
        flight.append(arr_port2)
        # get aircraft type
        craft_type2 = lastseg_soup[i].contents[11].contents[1].text.strip()
        flight.append(craft_type2)
        print('Second flight is:')
        print('Flight # is:',flightn2)
        print('Airline is:', airline2)
        print('Departure time is:',dep_time2)
        print('Departure port is:', dep_port2)
        print('Arrival time is:',arr_time2)
        print('Arrival port is:',arr_port2)
        print('Aircraft type is:',craft_type2)
        if flight not in Flightlist:
            Flightlist.append(flight)
        print('\n')
        count += 1
        print('count is',count)
print('Done with 1 stop flights')

dataframe = pd.DataFrame(Flightlist,columns=['flightn','airline','dep_time','dep_port','arr_time','arr_port','craft_type'])
print(dataframe.count())
"""

"""
    #comment start here
    print('One Stop flights: \n')
    count = 0
    for i in range(len(lastseg_soup)):
        print('iteration is', i)
        # check if flight arrives before midnight on the 6th
        if len(lastseg_soup[i].contents[7]) < 7 and firstseg_soup[i].contents[7].contents[
            3].text.strip() in INTERMEDPORTS and lastseg_soup[i].contents[5].contents[3].text.strip() in INTERMEDPORTS:
            # get flight number and airline name
            flight = []
            flightn1 = firstseg_soup[i].contents[3].contents[1].text.strip()
            flight.append(flightn1)
            airline1 = firstseg_soup[i].contents[3].contents[3].text.strip()
            flight.append(airline1)
            # get departure airport and departure time
            dep_time1 = firstseg_soup[i].contents[5].contents[1].text.strip()
            flight.append(dep_time1)
            dep_port1 = firstseg_soup[i].contents[5].contents[3].text.strip()
            flight.append(dep_port1)
            # get arrival airport and arrival time
            arr_time1 = firstseg_soup[i].contents[7].contents[1].text.strip()
            flight.append(arr_time1)
            arr_port1 = firstseg_soup[i].contents[7].contents[3].text.strip()
            flight.append(arr_port1)
            # get aircraft type
            craft_type1 = firstseg_soup[i].contents[11].contents[1].text.strip()
            flight.append(craft_type1)
            print('First flight is:')
            print('Flight # is:', flightn1)
            print('Airline is:', airline1)
            print('Departure time is:', dep_time1)
            print('Departure port is:', dep_port1)
            print('Arrival time is:', arr_time1)
            print('Arrival port is:', arr_port1)
            print('Aircraft type is:', craft_type1)
            if flight not in Flightlist:
                Flightlist.append(flight)

            # get flight number and airline name
            flight = []
            flightn2 = lastseg_soup[i].contents[3].contents[1].text.strip()
            flight.append(flightn2)
            airline2 = lastseg_soup[i].contents[3].contents[3].text.strip()
            flight.append(airline2)
            # get departure airport and departure time
            dep_time2 = lastseg_soup[i].contents[5].contents[1].text.strip()
            flight.append(dep_time2)
            dep_port2 = lastseg_soup[i].contents[5].contents[3].text.strip()
            flight.append(dep_port2)
            # get arrival airport and arrival time
            arr_time2 = lastseg_soup[i].contents[7].contents[1].text.strip()
            flight.append(arr_time2)
            arr_port2 = lastseg_soup[i].contents[7].contents[3].text.strip()
            flight.append(arr_port2)
            # get aircraft type
            craft_type2 = lastseg_soup[i].contents[11].contents[1].text.strip()
            flight.append(craft_type2)
            print('Second flight is:')
            print('Flight # is:', flightn2)
            print('Airline is:', airline2)
            print('Departure time is:', dep_time2)
            print('Departure port is:', dep_port2)
            print('Arrival time is:', arr_time2)
            print('Arrival port is:', arr_port2)
            print('Aircraft type is:', craft_type2)
            if flight not in Flightlist:
                Flightlist.append(flight)
            print('\n')
            count += 1
            print('count is', count)
print('Done with 1 stop flights')
#comment end here
"""