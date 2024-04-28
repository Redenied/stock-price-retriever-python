from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

import csv, time

# Input file name in current directory
input_file = "stocks.csv"

def read_file(input_file):
    """Receives a file name and returns a list of dictionaries with stock name, amount, value(empty) and total(empty)."""

    stocks = []

    # Read input file
    with open(input_file, 'r') as file:     # Open input file in read mode
        file_reader = csv.DictReader(file)  # Create dict reader object
        for row in file_reader:             # Iterate over each dictionary (row)
            # Add dictionaries to the list, default values of 0 to Value and Total columns
            stocks.append({"Ticker": row['Ticker'], "Amount of shares": int(row['Amount of shares']), "Value": 0, "Total": 0})

    return stocks

def get_stock_values(stocks):
    """Fetches data from Yahoo Finance for each stock received from the stocks list of dictionaries."""

    # Create ChromeOptions instance to configure Chrome
    chrome_options = webdriver.ChromeOptions()
    # Exclude certain log messages
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # Create a web driver instance to control Chrome
    # - 'service=Service()' sets up the ChromeDriver service
    # - 'options=chrome_options' applies the configured options to the browser
    driver = webdriver.Chrome(service=Service(), options=chrome_options)

    for stock in stocks:
        url = "https://finance.yahoo.com/quote/" + stock["Ticker"]
        xpath = "//*[@id='nimbus-app']/section/section/section/article/section[1]/div[2]/div[1]/section/div/section/div[1]/fin-streamer[1]/span"
        driver.get(url)

        time.sleep(3)

        stock_value = driver.find_element(By.XPATH, xpath)
        print(stock_value.text)

        # Assign value from Yahoo Finance to Value and calculate Total
        stock["Value"] = float(stock_value.text.replace(",", ""))
        stock["Total"] = stock["Amount of shares"]*stock["Value"]

    return stocks

def output_values(stocks):
    """Creates a csv file with the stocks information obtained from the list of dictionaries."""

    # Column names
    keys = ["Ticker", "Amount of shares", "Value", "Total"]

    # Create file in current directory in write mode
    with open('stock_values.csv', 'w', newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(stocks)
    return

stocks = (read_file(input_file))
output_values(get_stock_values(stocks))
