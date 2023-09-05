import requests
from bs4 import BeautifulSoup
import schedule
import time
import pickle
from datetime import datetime

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"{timestamp} - Running CoinalyzeScrapper...")

def scrape_coinalyze(): #The function that scrapes coinylize website and return the position of every coin in that moment...
    url = 'https://coinalyze.net/?order_by=volume_24hour&order_dir=desc'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the <tbody> element
    tbody = soup.find('tbody')

    # Find all <tr> elements within the <tbody> element
    rows = tbody.find_all('tr')

    coin_data = [] 
    
    # Loop through each <tr> element and extract the desired data
    for i, row in enumerate(rows, start=1):
        coin_name = row['data-coin']
        coin_entry = {"Position": i, "CoinName": coin_name, "Timestamp": timestamp}
        coin_data.append(coin_entry)

    return coin_data

def job():
    print(f"{timestamp} - Scraping Coinalyze...")
    coin_data = scrape_coinalyze()

    # Load the existing data from the pickle file
    try:
        with open('coin_data_list.pkl', 'rb') as file:
            coin_data_list = pickle.load(file)
    except FileNotFoundError:
        coin_data_list = []

    # Append the new coin data to the existing list
    coin_data_list.append(coin_data)

    # Save the updated coin_data_list to the pickle file
    with open('coin_data_list.pkl', 'wb') as file:
        pickle.dump(coin_data_list, file)

# Schedule the job to run every 5 minutes
schedule.every(30).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)