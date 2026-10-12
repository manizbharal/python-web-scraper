import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
from datetime import datetime
import json

# Setup automated logging
logging.basicConfig(
    filename='scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_advanced_pipeline(url, csv_out, json_out):
    logging.info(f"Starting automated data extraction pipeline for: {url}")
    print("Initializing pipeline...")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        logging.info("Successfully fetched website data with Status Code 200.")
    except Exception as e:
        logging.error(f"Failed to fetch URL. Error: {str(e)}")
        print(f"Extraction failed. Check scraper.log for details.")
        return

    # Parse HTML DOM
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes_data = []

    # Extract dynamic elements
    quote_elements = soup.find_all('div', class_='quote')
    logging.info(f"Extracted {len(quote_elements)} raw elements from HTML.")

    for item in quote_elements:
        text = item.find('span', class_='text').get_text(strip=True)
        author = item.find('small', class_='author').get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in item.find_all('a', class_='tag')]

        quotes_data.append({
            'quote': text,
            'author': author,
            'tags': ", ".join(tags),
            'extracted_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

    # Load into Pandas Dataframe
    df = pd.DataFrame(quotes_data)

    # Data Transformation & Cleaning
    df['author'] = df['author'].str.title()
    df.drop_duplicates(subset=['quote'], inplace=True)

    # Export multi-format outputs
    df.to_csv(csv_out, index=False)
    df.to_json(json_out, orient='records', indent=4)

    logging.info(f"Pipeline finished successfully. Output saved to {csv_out} and {json_out}.")
    print(f"Pipeline executed successfully! Saved {len(df)} records to CSV & JSON.")

if __name__ == '__main__':
    # Live demo scraping endpoint
    target_url = 'https://quotes.toscrape.com/'
    run_advanced_pipeline(target_url, 'extracted_quotes.csv', 'extracted_quotes.json')