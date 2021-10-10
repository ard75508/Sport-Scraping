from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import json
#test

# userCity = input("Enter a city: ")
userCity = "los angeles"

# creating team object to store in teamList array


class Team:
    def __init__(self, name, league, schedule):
        self.name = name
        self.league = league
        self.schedule = schedule
        #test Team


teamList = []

options = Options()
options.headless = True
#PATH = "/Users/braddodds/Documents/chromedriver"
PATH = "/Users/ard75508/Documents/chromedriver"    # Path of chrome driver
driver = webdriver.Chrome(PATH, options=options)    # headless driver options


# driver.get("https://espn.com")
# driver clicks on search bar and searches for city
# driver.find_element_by_class_name("search").click()
# search = driver.find_element_by_id("global-search-input")
# search.send_keys(userCity)
# search.send_keys(Keys.RETURN)
# OR ----
# put input city right into URL link
driver.get("https://www.espn.com/search/_/q/{}".format(userCity))


html = driver.page_source
soup = BeautifulSoup(html, "lxml")
#test soup


def returnSchedule(urlStr):
    schedule1 = ""
    driver.get(urlStr)
    try:
        schdeule = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "club-schedule"))
        )
        schedule1 = schdeule.text
        #print(schedule1)
        #print(schdeule.text)
    except:
        driver.quit()
    
    for character in schedule1:
        if character == "@":
            sam = schedule1.replace("@", "Away")
            print(sam)
        
        


try:
    # only finds the FIRST card element!!
    # this should be okay since the first card
    # element after a search is the search results
    cards = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, "Card"))
    )

    teams = cards.find_elements_by_tag_name("li")
    for team in teams:
        name = team.find_element_by_class_name("Truncate")
        league = team.find_element_by_class_name("LogoTile__Meta")

        linkElement = team.find_element_by_tag_name("a")
        link = linkElement.get_attribute("href")
        print(link)

        # only save team if data is not empty
        if name.text == "" and league.text == "":
            continue

        else:
            # create object and add to array
            newTeam = {
                'name': name.text,
                'league': league.text,
                'link': link
            }
            teamList.append(newTeam)
            

    print("")
    print(teamList)
    print("")

    # seperates team name from Card
    # teamNames = cards.find_elements_by_class_name("Truncate")
    # print("Teams: ")
    # for team in teamNames:
    #     print(team.text)


except:
    print("Driver failed. Quitting...")
    driver.quit()


returnSchedule(teamList[0]['link'])

    

# for team in teamList:
#     returnSchedule(team['link'])

time.sleep(2)

driver.quit()


# write python object to new json file
# WORKS

# teamObj = teamList
# jsonStr = json.dumps(teamObj)
# jsonFile = open("data.json", "w")
# jsonFile.write(jsonStr)
# jsonFile.close()
