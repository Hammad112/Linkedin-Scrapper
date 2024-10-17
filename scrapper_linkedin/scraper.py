# scraper.py
import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from urllib.parse import urljoin


def scrape_company_data(driver, url):
    driver.get(url)
    time.sleep(2)  # Allow the page to load completely
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find the main div with the company info
    main_div = soup.find('div', class_='block mt2')
    if not main_div:
        print(f"Could not find the main div on page {url}")
        return None

    company_name = main_div.find('h1', class_='org-top-card-summary__title').get_text(strip=True) if main_div.find('h1') else 'N/A'
    tagline_element = main_div.find('p', class_='org-top-card-summary__tagline')
    tagline = tagline_element.get_text(strip=True) if tagline_element else 'N/A'

    # Followers, industry, location
    info = main_div.find_all('div', class_='org-top-card-summary-info-list__info-item')
    industry = info[0].get_text(strip=True) if len(info) > 0 else 'N/A'
    location = info[1].get_text(strip=True) if len(info) > 1 else 'N/A'
    followers= info[2].get_text(strip=True) if len(info)> 2 else 'N/A'
   
    employees = main_div.find('span', class_='t-normal')
    employees_count = employees.get_text(strip=True) if employees else 'N/A'

 
    crunch_base = soup.find('div', class_='org-about-module-wrapper org-about-module__card-spacing')
    if not crunch_base:
        print(f"Could not find the main div on page {url}")
        return None

    
    grants = crunch_base.find('p', class_='t-14 t-black t-normal hoverable-link-text').get_text(strip=True)if crunch_base.find('p') else 'N/A'
    # Attempt to find the paragraph element with the specified class
    funds_element = crunch_base.find('p', class_='t-14 t-bold')

    # Check if the element was found and then call get_text
    funds = funds_element.get_text(strip=True) if funds_element else 'N/A'
    
    # Store scraped data in a dictionary
    company_details = {
        'Company Name': company_name,
        'Tagline': tagline,
        'Followers': followers,
        'Employee Count': employees_count,
        'Industry': industry,
        'Location': location,
        'Funding':funds,
        'Funds_status':grants,
    }

    return company_details


def scrape_about_page_data(driver, url):
    driver.get(url + '/about/')
    time.sleep(2)
    about_soup = BeautifulSoup(driver.page_source, 'html.parser')

    company_details = {
        'Overview': 'N/A',
        'Website': 'N/A',
        'Phone': 'N/A',
        'Verified Page': 'N/A',
        'Company size': 'N/A',
        'Associated Members': 'N/A',
        'Headquarters': 'N/A',
        'Founded': 'N/A',
        'Specialties': 'N/A',
    }

    # Scrape the overview paragraph
    overview_paragraph = about_soup.find('p', class_='break-words white-space-pre-wrap t-black--light text-body-medium')
    if overview_paragraph:
        company_details['Overview'] = overview_paragraph.get_text(strip=True)


    ## Contact Information
    for title in about_soup.find_all('dt', class_='mb1'):
        title_text = title.get_text(strip=True)
        data_element = title.find_next_sibling('dd')

        if not data_element:
            continue

        if 'Website' in title_text:
            company_details['Website'] = data_element.find('a')['href'] if data_element.find('a') else 'N/A'
        elif 'Phone' in title_text:
            company_details['Phone'] = data_element.get_text(strip=True)
        elif 'Verified Page' in title_text:
            company_details['Verified Page'] = data_element.get_text(strip=True)
        elif 'Company size' in title_text:
            company_details['Company size'] = data_element.get_text(strip=True)
            company_details['Associated Members'] = data_element.find_next_sibling('dd').get_text(strip=True) if data_element.find_next_sibling('dd') else 'N/A'
        elif 'Headquarters' in title_text:
            company_details['Headquarters'] = data_element.get_text(strip=True)
        elif 'Founded' in title_text:
            company_details['Founded'] = data_element.get_text(strip=True)
        elif 'Specialties' in title_text:
            company_details['Specialties'] = data_element.get_text(strip=True)

    return company_details




def scrape_jobs_data(driver, url):
    # Navigate to the jobs section of the company
    driver.get(url + '/jobs/')
    time.sleep(2)  # Allow time for the page to load

    jobs_data = {}

    # Attempt to find the "show all jobs" button
    try:
        show_all_button = driver.find_element(By.CSS_SELECTOR, '.org-jobs-recently-posted-jobs-module__show-all-jobs-btn-link')

        # Get the href attribute from the <a> tag
        relative_url = show_all_button.get_attribute('href')

        # Concatenate the relative URL with the base URL to get the full URL
        full_url = urljoin(url, relative_url)


        # Navigate to the full URL (clicking the button alternative)
        driver.get(full_url)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find all job cards (li elements with class 'jobs-search-results__list-item')
        job_cards = soup.find_all('li', class_='jobs-search-results__list-item')

        # Check if any job cards are found
        if not job_cards:
            print("No job cards found.")
            return {"message": "No data found for jobs."}  # Return specific message if no jobs found

        # Loop through each job card and extract relevant details
        for job_card in job_cards:
            job_data = {}

            # Job Title
            job_title_tag = job_card.find('a', class_='job-card-list__title')
            if job_title_tag:
                job_title = job_title_tag.text.strip()
                job_data['title'] = job_title

                # Check if 'title' was successfully added (to skip empty job cards)
                if not job_title:
                    continue  # Skip this iteration if no title is found

                # Company Name
                company_tag = job_card.find('span', class_='job-card-container__primary-description')
                if company_tag:
                    job_data['company'] = company_tag.text.strip()
                
                # Location
                location_tag = job_card.find('li', class_='job-card-container__metadata-item')
                if location_tag:
                    job_data['location'] = location_tag.text.strip()
                
                # Number of Applicants
                applicants_tag = job_card.find('span', class_='tvm__text tvm__text--positive')
                if applicants_tag:
                    job_data['applicants'] = applicants_tag.text.strip()
                else:
                    job_data['applicants'] = '0 applicants'  # Default to '0 applicants' if not found
                
                # Status (e.g., Viewed, Applied)
                status_tag = job_card.find('li', class_='job-card-container__footer-job-state')
                if status_tag:
                    job_data['status'] = status_tag.text.strip()
                else:
                    job_data['status'] = 'Unknown status'  # Default status if not found
                
                # Add job data to the jobs_data dictionary with the job title as the key
                jobs_data[job_title] = job_data

        # Check if any job data was collected
        if not jobs_data:
            print("No job data collected.")
            return {"message": "No data found for jobs."}  # Return specific message if no jobs data found

        return jobs_data

    except Exception as e:    
        return {"jobs_status": "No jobs found for this company."}  # Return specific message on error
