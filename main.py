# Import libraries
# import requests
from bs4 import BeautifulSoup
import csv
from selenium import webdriver
import time as t
import json
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# Define a function to scrape the web page
def scrape(url, print_result=False):
    try:
        # Den Pfad zum Webdriver anpassen (z.B. Chrome oder Firefox)
        driver = webdriver.Chrome()

        driver.get(url)

        # # Warten, bis die Tabelle geladen wurde (dies ist ein Beispiel, die tatsächliche Website kann unterschiedlich sein)
        # WebDriverWait(driver, 10)
        # results_table = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "grid__GridItem-sc-10p77ff-1 cuHsGh")))

        # wait till all elements are loaded
        t.sleep(5)

        # HTML-Inhalt der Seite erhalten
        page_source = driver.page_source

        # Mit BeautifulSoup den HTML-Inhalt parsen
        soup = BeautifulSoup(page_source, 'html.parser')

        # find race title
        race_title = soup.find('div', class_='headline-main').text.strip()
        formatted_race_title = race_title.replace(' ', '_')

        # find all races and qualifyings
        result_races_filter = soup.find('div', class_='grid__GridItem-sc-10p77ff-1 cuHsGh title')

        # find all results to all races
        results_races = result_races_filter.find('div', class_='select__Select-sc-1jtg7kw-0 jZzHgV')

        # Rennergebnisse in der Tabelle mit dem angegebenen Klassenname finden
        results_table = soup.find('div', class_='grid__GridItem-sc-10p77ff-1 cuHsGh session-table-wrapper')

        if results_races and results_table:
            #get all races
            races = results_races.find_all('option')

            #get all results for all races
            races_results = results_table.find_all('table', class_='table__Table-sc-1js841w-0 eieqVK')

            race_results_data = []

            #reverse list as the races are listed reverserly to result tables
            for (row_races, race_result) in zip(reversed(races), races_results):
                race = row_races.text.strip()
                race_data = {
                    "race": race,
                    "results": []
                }

                print(race)

                #loop through race results
                rows = race_result.find_all('tr')
                for row in rows[1:]: # skip header-row
                    columns = row.find_all('td')

                    rank = columns[0].text.strip()
                    driver_number = columns[1].text.strip()
                    driver = [i.text.strip() for i in columns[2].find_all('a')]
                    team = [i.text.strip() for i in columns[3].find_all('a')]
                    time = columns[4].text.strip()

                    print(f"Position: {rank}, Fahrernummer: {driver_number}, Fahrer: {driver}, Team: {team}, Zeit: {time}")

                    result_entry = {
                        "Position": rank,
                        "Fahrernummer": driver_number,
                        "Fahrer": driver,
                        "Team": team,
                        "Zeit": time
                    }

                    #append race results
                    race_data["results"].append(result_entry)

                #append race-names to specific race results
                race_results_data.append(race_data)

                if print_result == True:
                    #save results to json file
                    current_timestr = t.strftime("%Y%m%d-%H%M%S")
                    with open(f'/home/vagrant/RaceMates/WebScraper_RaceMates/results/{formatted_race_title}_rennergebnisse_{current_timestr}.json', 'w') as json_file:
                        json.dump(race_results_data, json_file, indent=4, ensure_ascii=False)

                    #print(json.dumps(race_results_data, indent=4, ensure_ascii=False))

        else:
            print("Rennen oder Rennergebnisse nicht gefunden.")

    except Exception as e:
        # Print an error message
        print(e)

# Call the scrape function
if __name__ == "__main__":
    to_scrap_url = "https://www.adac-motorsport.de/adac-gt-masters/race-calendar/2023/race-details/2023-6-9-festival-of-dreams,-hockenheimring-baden-wurttemberg/"
    scrape(url = to_scrap_url, print_result=True)