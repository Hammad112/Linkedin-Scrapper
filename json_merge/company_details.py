# company_details.py
def get_full_company_details(scraped_data, about_data, jobs_data):
    # Ensure all inputs are dictionaries
    if isinstance(scraped_data, list):
        # Handle conversion from list to dict (example)
        scraped_data = scraped_data[0] if scraped_data else {}
        
    if isinstance(about_data, list):
        about_data = about_data[0] if about_data else {}
        
    if isinstance(jobs_data, list):
        jobs_data = {job['title']: job for job in jobs_data}  # Example of creating a dict from jobs list

    # Merge all dictionaries
    full_data = {**scraped_data, **about_data, **jobs_data}
    return full_data

