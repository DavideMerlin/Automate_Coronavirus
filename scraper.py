#pip install selenium
from selenium import webdriver
#pip install pandas
import pandas as pd
from time import sleep
#pip install twilio
from twilio.rest import Client

#start up the webdriver and create a dataframe
class VirusBot():
    def __init__(self):
        self.driver = webdriver.Chrome()
        #define csv file columns
        columns = ['total_cases', 'new_cases', 'total_deaths', 'new_deaths','active_cases', 'total_recovered', 'serious_critical']
        self.df = pd.DataFrame(columns=columns)

    #tracker function to locate elements
    def tracker(self):
        #telling the driver what web page to open
        website = self.driver.get('https://worldometers.info/coronavirus/')
        #storing the table element in a variable
        table = self.driver.find_element_by_xpath('//*[@id="main_table_countries_today"]')
        #specifying what country you want to analyze
        country = table.find_element_by_xpath("//td[contains(., 'USA')]")
        #specifying the country row
        row = country.find_element_by_xpath("./..")
        #formatting the columns
        cell = row.text.split(" ")

        sleep(1)

        #scraping each row cell for "USA"
        total_cases = cell[2]
        new_cases = cell[3]
        total_deaths = cell[4]
        new_deaths = cell[5]
        active_cases = cell[6]
        total_recovered = cell[7]
        serious_critical = cell[8]

        #append results to columns in dataframe
        self.df = self.df.append(
            {'total_cases': total_cases,
            'new_cases': new_cases,
            'total_deaths': total_deaths,
            'new_deaths': new_deaths,
            'active_cases': active_cases,
            'total_recovered': total_recovered,
            'serious_critical': serious_critical}, ignore_index=True)

    #export function to create the CSV file
    def scrape_to_csv(self):
        self.df.to_csv('scraped_data.csv')

        #send_sms(country, total_cases, new_cases, total_deaths, new_deaths, active_cases, total_recovered, serious_critical)

        #close the web driver when results are reported
        self.driver.close()

#optional sms function
#fill out with your credentials
""" def send_sms(country, total_cases, new_cases, total_deaths, new_deaths, active_cases, total_recovered, serious_critical):
        account_sid = 'your sid here'
        auth_token = 'your token here'
        client = Client(account_sid, auth_token)

        message = client.messages \
                        .create(
                            body="The toal coronavirus cases in country were..'\
                                \nTotal cases: ' + total_cases +'\
                                \nNew cases: ' + new_cases + '\
                                \nTotal deaths: ' + total_deaths + '\
                                \nNew deaths: ' + new_deaths + '\
                                ...",
                                from_='your twilio number',
                                to='your personal phone number'
                            )

    self.driver.quit()
 """
#calling functions
bot = VirusBot()
bot.tracker()
bot.scrape_to_csv()
