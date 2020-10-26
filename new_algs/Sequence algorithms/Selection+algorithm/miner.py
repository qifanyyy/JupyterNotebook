from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd


class OuterMiner:
    @staticmethod     
    def datasetCount(driver):
        countInfo = driver.find_element_by_xpath("//input[@class='jss24 jss9 input jss29 jss12 jss30 jss13']")
        placeholder = countInfo.get_attribute('placeholder')
        count = [int(s) for s in placeholder.split() if s.isdigit()]
        return count[0]

    @staticmethod
    def scrollDown(driver):
        SCROLL_PAUSE_TIME = 0.5
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    @staticmethod
    def start(link=""):
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
        driver = webdriver.Firefox(firefox_profile=firefox_profile)
        driver.get(link)
        driver.implicitly_wait(20)
        datasetCounter = OuterMiner.datasetCount(driver)
        linkDrivers = []
        while True:
            linkDrivers = driver.find_elements_by_xpath("//a[@class='sc-hycgNl dQUVSX']")
            if(len(linkDrivers)) >= datasetCounter:
                break
            else:
                OuterMiner.scrollDown(driver)
        datasetLinks = []
        for linkDriver in linkDrivers:
            datasetLinks.append(linkDriver.get_attribute("href"))
        driver.quit()
        return (datasetLinks,datasetCounter)

class InnerMiner:
    @staticmethod
    def start(link=""):
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference("browser.privatebrowsing.autostart", True)

        driver = webdriver.Firefox(firefox_profile=firefox_profile)
        driver.get(link)
        driver.implicitly_wait(20)
        try:
            driver.find_element_by_xpath("//div[contains(@class, 'sc-eQkpkc ocQYf')]").click()
        except:
            pass
        try:
            continue_link = driver.find_element_by_xpath("//div[contains(@class, 'markdown-converter__text--rendered')]")
            save = continue_link.text
        except:
            save = link
        driver.quit()
        return save

links = [
    'https://www.kaggle.com/datasets?tags=13302-classification%2C14202-multiclass+classification%2C14201-binary+classification%2C6603-categorical+data%2C13404-logistic+regression',
    'https://www.kaggle.com/datasets?tags=13303-regression+analysis%2C13405-linear+regression%2C14203-regression'
]
container = []
for link in links:
    container.append(OuterMiner.start(link))
LinkCollection = container[0][0] + container[1][0]
print(len(LinkCollection))
ContentCollection = []
TypeCollection = []
for i in range(len(LinkCollection)):
    print(i)
    ContentCollection.append(InnerMiner.start(LinkCollection[i]))
    if i<container[0][1]:
        TypeCollection.append(1)
    else:
        TypeCollection.append(0)

finalDict = {
    "Link":LinkCollection,
    "Content":ContentCollection,
    "Type":TypeCollection
}

df = pd.DataFrame(finalDict)

df.to_csv("C:/Users/Rohan/COMP167/Algorithm-Selection-Tool/Algorithm-Selection-Tool-master/src/Algorithm Selection/Data.csv",sep="\t")