# main.py
import os
import pandas as pd
import json
from Utilis.utils import clean_linkedin_url
from scrapper_linkedin.scraper import scrape_company_data, scrape_about_page_data, scrape_jobs_data
from json_merge.company_details import get_full_company_details
from Configuration.config import create_driver
from selenium.webdriver.support.ui import WebDriverWait
import time
from clean_empty_fields.data_clean import clean_data

def main():
    driver = create_driver()

    # Create a directory to save the scraped files
    directory = "Scraping_Companies"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Read CSV with company names and LinkedIn URLs
    df = pd.read_csv('companies_list_space.csv')  # Assuming columns: 'Company Name', 'LinkedIn URL'

    # Iterate through each row in the CSV
    for index, row in df.iterrows():
        company_name = row['Company Name']
        linkedin_url = row['Linkedin URL']

        # Ensure linkedin_url is a string and check if URL is empty or not
        if pd.isna(linkedin_url) or not linkedin_url.strip():
            print(f"Skipping {company_name} due to missing or empty URL.")
            continue

        filename = f"{company_name.replace(' ', '_').lower()}.json"
        filepath = os.path.join(directory, filename)

        # Check if the file already exists
        if os.path.exists(filepath):
            print(f"File already exists for {company_name}, skipping...")
            continue

        print(f"Scraping data for {company_name} at {linkedin_url}")

        # Clean URL
        cleaned_url = clean_linkedin_url(linkedin_url)

        # Call scrapper function to get data
        company_data = scrape_company_data(driver, cleaned_url)
        about_data = scrape_about_page_data(driver, cleaned_url)
        jobs_data=scrape_jobs_data(driver,cleaned_url)
       
        

        if company_data is None or about_data is None or jobs_data is None:
            print(f"Failed to scrape data for {company_name}.")
            continue

        # Consolidate data
        full_data = get_full_company_details(company_data, about_data,jobs_data)
        
        full_data_clean = clean_data(full_data)

        # Save each company's data into a separate JSON file inside the directory
        with open(filepath, 'w') as f:
            json.dump(full_data_clean, f, indent=4)

        print(f"Data saved for {company_name} in {filepath}")

    # Close the driver
    driver.quit()

if __name__ == "__main__":
    main()
