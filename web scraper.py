import requests
from bs4 import BeautifulSoup
import pandas as pd  # For saving data to Excel

# Base URL for Data Science jobs on Reed
BASE_URL = "https://www.reed.co.uk/jobs/data-science-jobs"

# User-Agent header to mimic a browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

# List to store all job data
jobs = []

# Start with page 1
page_number = 1

while True:
    print(f"Scraping page {page_number}...")

    # Construct the page-specific URL
    url = f"{BASE_URL}?pageno={page_number}"
    
    # Make the HTTP request
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html5lib')

    # Locate job listings
    job_cards = soup.find_all('div', class_='col-sm-12 col-md-7 col-lg-8 col-xl-9')

    # Stop if no job cards found (we’ve reached the last page)
    if not job_cards:
        print("No more jobs found. Scraping complete.")
        break

    # Parse each job card
    for card in job_cards:
        try:
            title_tag = card.find('a', class_='job-card_jobTitle__HORxw')
            if not title_tag:
                continue  # Skip this if job title not found

            title = title_tag.get_text(strip=True)
            job_url = "https://www.reed.co.uk" + title_tag['href']

            company_tag = card.find('a', class_='job-card_profileUrl__fRi56')
            company = company_tag.get_text(strip=True) if company_tag else 'N/A'

            metadata = card.find_all('li', class_='job-card_jobMetadata__item___QNud')
            salary = metadata[0].get_text(strip=True) if len(metadata) > 0 else 'N/A'
            location = metadata[1].get_text(strip=True) if len(metadata) > 1 else 'N/A'
            job_type = metadata[2].get_text(strip=True) if len(metadata) > 2 else 'N/A'
            remote = metadata[3].get_text(strip=True) if len(metadata) > 3 else 'N/A'

            jobs.append({
                'Title': title,
                'URL': job_url,
                'Company': company,
                'Salary': salary,
                'Location': location,
                'Job Type': job_type,
                'Remote': remote
            })

        except Exception as e:
            print(f"Error parsing job card: {e}")

    # Go to the next page
    page_number += 1

# Convert the list of job dicts to a DataFrame
df = pd.DataFrame(jobs)

# Save to Excel file
df.to_excel("reed_jobs.xlsx", index=False, engine='openpyxl')
print("\nData saved to reed_jobs.xlsx")
