from selenium import webdriver                              #for web scraping
from selenium.webdriver.support.ui import WebDriverWait     #importing wait method
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import re
import time
import pandas as pd
import sys

####DEFINING CONSTANTS######
#Allowed airports:
PORTS = ['LAX','SFO','PHX','SEA','DEN','ATL','ORD','BOS','IAD','JFK']   #all nodes in graph
INTERMEDPORTS = ['SFO','PHX','SEA','DEN','ATL','ORD','BOS','IAD']       #all nodes other than source and destination
Sources = ['LAX']+INTERMEDPORTS                                         #all possible source nodes for directed flights
Destinations = INTERMEDPORTS+['JFK']                                    #all possible destination nodes for flights
AIRLINES = ['United','Delta','AA']                                      #all airline names
DEPDATE = '01/06/2020'                                                  #Departure Date


#source = "LAX"
#dest = "ORD"
#Sources = ['LAX']
#Destinations = ['SEA']


#Delta url:
Delta_home_url = "https://www.delta.com/flight-search-2/book-a-flight?cacheKeySuffix=8adce384-e7c7-442c-a36d-ecd926c21a74"
Flightlist = []




for source in Sources:
    for dest in Destinations:
        if source!=dest:
            driver = webdriver.Chrome('/Users/ahmedkoptanmacbook/Imp/ASU/Course Content/Fall 2019/CSE 551 Algorithms/Project/chromedriver')
            driver.get(Delta_home_url)
            driver.implicitly_wait(100)

            origin = driver.find_element_by_id('fromAirportName')
            origin.click()
            driver.implicitly_wait(100)

            origin_input = driver.find_element_by_id('search_input')
            origin_input.clear()
            origin_input.send_keys(source)
            time.sleep(2)
            origin_input.send_keys(Keys.ENTER)


            destination = driver.find_element_by_id('toAirportName')
            destination.click()
            driver.implicitly_wait(100)

            destination_input = driver.find_element_by_id('search_input')
            destination_input.clear()
            destination_input.send_keys(dest)
            time.sleep(2)
            destination_input.send_keys(Keys.ENTER)



            trip_type = driver.find_element_by_id('selectTripType-val')
            trip_type.click()
            driver.implicitly_wait(100)
            driver.find_element_by_id('ui-list-selectTripType1').click()


            depdate = driver.find_element_by_id('input_departureDate_1')
            depdate.click()
            driver.implicitly_wait(100)
            driver.find_element_by_class_name('dl-datepicker-1').click()
            driver.implicitly_wait(100)
            time.sleep(1)
            driver.find_element_by_xpath("//a[@aria-label='6 January 2020, Monday']").click()
            time.sleep(1)
            driver.find_element_by_class_name('donebutton').click()
            time.sleep(1)
            driver.find_element_by_id('btnSubmit').submit()
            driver.implicitly_wait(100)
            time.sleep(5)

            driver.implicitly_wait(100)
            driver.find_element_by_xpath(".//*[contains(text(), 'Sort & Filter')]").click()
            time.sleep(1)


            stop = driver.find_elements_by_xpath("//label[@for='stopType_1']")
            if not stop:
                print('No 1 stop button found')
                ##########slider###########
            else:
                stop[0].click()
                driver.implicitly_wait(100)
                time.sleep(2)

            driver.implicitly_wait(100)
            time.sleep(1)
            page_soup = BeautifulSoup(driver.page_source, 'html.parser')
            data_soup = page_soup.find_all('grid-flight-result-container', attrs={'class': 'ng-star-inserted'})

            if data_soup[0].find_all('div', attrs={'class': 'flightSecFocus'})[0].contents[1].strip() != source \
                    or data_soup[0].find_all('div', attrs={'class': 'flightSecFocus'})[1].contents[
                3].strip() != dest:
                print("Results have only 1+ stop flights")
            else:
                exists=True
                while exists:
                    more = driver.find_elements_by_xpath(".//*[contains(text(), ' see more results ')]")
                    if not more:
                        print("No elements found")
                        exists=False
                    else:
                        element = more[0]
                        element.click()
                        driver.implicitly_wait(100)
                        time.sleep(2)

                driver.implicitly_wait(100)
                time.sleep(2)
                # Get HTML text to get flight data
                page_soup = BeautifulSoup(driver.page_source, 'html.parser')
                data_soup = page_soup.find_all('grid-flight-result-container', attrs={'class': 'ng-star-inserted'})

                # data structure in data_soup
                # 1 = a (class 'upsellpopupanchor', haspopup "true" ), Flight number : data_soup[i].find_all('a',attrs={'class':'upsellpopupanchor','aria-haspopup':"true"})[0].contents[0].strip()

                # 2 = span (class 'trip-time pr0-sm-down') , Departure Time: data_soup[i].find_all('span',attrs={'class':'trip-time pr0-sm-down'})[0].text.strip()

                # 3 = span (class 'trip-time pl0-sm-down') , Arrival Time: data_soup[i].find_all('span',attrs={'class':'trip-time pl0-sm-down'})[0].tdataext.strip()
                ### if len(data_soup[0].find_all('span',attrs={'class':'trip-time pl0-sm-down'})[0].contents) == 4, arrives before 7 JAN
                ### if len(data_soup[0].find_all('span',attrs={'class':'trip-time pl0-sm-down'})[0].contents) == 5, arrives on or after 7 JAN

                # 4 Dep port = source
                #or
                #data_soup[i].find_all('div',attrs={'class':'flightSecFocus'})[0].contents[1].strip()

                # Arr port = destination
                #or
                #data_soup[i].find_all('div',attrs={'class':'flightSecFocus'})[1].contents[3].strip()

                # convert dep and arr times to have space in the middle
                # data_soup[i].find_all('span',attrs={'class':'trip-time pl0-sm-down'})[0].text.strip().replace('AM',' AM').replace('PM',' PM')

                driver.implicitly_wait(100)
                time.sleep(2)
                print('Finding Details buttons')
                details = driver.find_elements_by_xpath("//div[@class='text-left col-lg-2 col-sm-2 expandDetailsTab flightcardDetails ']")
                driver.implicitly_wait(100)

                if not data_soup:
                    print('No data found on page')

                if not details:
                    print('No results found')
                elif len(details)!=len(data_soup):
                    print('Different sizes of html list and detail button list found')
                    sys.exit()#!!!!
                else:
                    print("buttons and data found. Starting to iterate over data")
                    for i in range(len(data_soup)):
                        #check if dep port and arr port are within our PORTS
                        if data_soup[i].find_all('div',attrs={'class':'flightSecFocus'})[0].contents[1].strip() == source \
                            and data_soup[i].find_all('div',attrs={'class':'flightSecFocus'})[1].contents[3].strip() == dest:
                            # check if flight arrives before or on midnight of the 7th
                            if len(data_soup[i].find_all('span', attrs={'class': 'trip-time pl0-sm-down'})[0].contents) <= 4:
                                flight = []
                                # get flight number and airline name
                                flightn = \
                                data_soup[i].find_all('a', attrs={'class': 'upsellpopupanchor', 'aria-haspopup': "true"})[0].contents[
                                    0].strip()
                                flight.append(flightn)
                                # Airline name is Delta Airlines
                                airline = "Delta Airlines"
                                flight.append(airline)

                                # get departure airport and departure time
                                dep_time = data_soup[i].find_all('span', attrs={'class': 'trip-time pr0-sm-down'})[
                                    0].text.strip().replace('AM', ' AM').replace('PM', ' PM')
                                flight.append(dep_time)
                                dep_port = source
                                flight.append(dep_port)

                                # get arrival airport and arrival time
                                arr_time = data_soup[i].find_all('span', attrs={'class': 'trip-time pl0-sm-down'})[
                                    0].text.strip().replace('AM', ' AM').replace('PM', ' PM')
                                flight.append(arr_time)
                                arr_port = dest
                                flight.append(arr_port)

                                # get aircraft type
                                details[i].click()
                                driver.implicitly_wait(100)
                                time.sleep(2)
                                detail_soup = BeautifulSoup(driver.page_source, 'html.parser')
                                craft_type = detail_soup.find_all('div', attrs={'class': 'aircraft-type mt-2'})[0].text.strip()
                                flight.append(craft_type)
                                time.sleep(1)
                                driver.implicitly_wait(100)
                                exit = driver.find_element_by_class_name('exit-button')
                                exit.click()
                                driver.implicitly_wait(100)
                                time.sleep(2)
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
                                    df = pd.DataFrame(Flightlist,
                                                      columns=['flightn', 'airline', 'dep_time', 'dep_port', 'arr_time',
                                                               'arr_port',
                                                               'craft_type'])
                                    df.to_csv('Deltaflights.csv', index=False, header=True)
                        else:
                            print("Flight source and destination are not in our list for",source,"and",dest)
                driver.close()







"""


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


"""slider
                driver.implicitly_wait(100)
                slider = driver.find_elements_by_xpath(
                    "//div[@aria-label='Maximum value modifier of CONNECTION TIME slider, value ranges between 0 hour to 4 hour, Use left and right arrow to change range selection or use tab to change handle selector']")
                if not slider:
                    print("no slider found")
                else:
                    for i in range(5):
                        slider[0].send_keys(Keys.LEFT)
                        driver.implicitly_wait(100)
                        time.sleep(1)
                    click1 = driver.find_element_by_xpath("//label[@class='checkboxLabel hide-onlyLink']")
                    click1.click()
                    driver.implicitly_wait(100)
                    time.sleep(1)
                    click1.click()
                    driver.implicitly_wait(100)
                    time.sleep(1)
                    #slider = driver.find_elements_by_xpath(
                    #    "//div[@aria-label='Maximum value modifier of CONNECTION TIME slider, value ranges between 0 hour to 4 hour, Use left and right arrow to change range selection or use tab to change handle selector']")
                    #if not slider:
                    #    print()
                    #else:
                    slider[0].click()
                """