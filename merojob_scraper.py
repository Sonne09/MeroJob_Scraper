import csv
from selenium import webdriver
from bs4 import BeautifulSoup


def get_url(search_text):
    """Generate a url from search text"""
    template = ' https://merojob.com/search/?q={}'
    search_term = search_text.replace(' ', '+')
    
    # add term query to url
    url = template.format(search_term)
    
    # add page query placeholder
    url += '&page={}'
        
    return url


def extract_record(job):
    """Extract and return data from a single record"""

    try:
        # Job title and the location
        job_title = job.h1.a.text.strip()  
        company = job.h3.a.text.strip()
    
    # Key skill and jobpost url
        key_skills = job.find('span', 'badge').text

    except AttributeError:
        job_title = 'NA'
        company = 'NA'
        key_skills = 'NA'
    
    job_url = 'https://www.merojob.com' + job.h1.a.get('href')

    result = (job_title, company, key_skills, job_url)

    return result


def main(search_term):
    """Run main program"""

    # startup the webdriver
    driver = webdriver.Chrome('./chromedriver')

    records = []
    url = get_url(search_term)

    # looping through multiple pages.
    for page in range(1,30):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'lxml')
        cards = soup.find_all('div','card mt-3 hover-shadow')
        for job in cards:
            record = extract_record(job)
            if record:
                records.append(record)
    
    driver.close()

    # Savimg extracted data to a csv file
    with open('results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Job Title', 'Company', 'Key Skill', 'Job Url'])
        writer.writerows(records)

# Run the main program
main('IT')