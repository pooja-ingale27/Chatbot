#!/usr/bin/env python
# coding: utf-8

# In[11]:


# Importing required libraries
import requests
from bs4 import BeautifulSoup
import pickle  
import re
import logging  
import nltk  
from nltk.corpus import stopwords

# Download stopwords the first time
# nltk.download('stopwords')
# stop_words = set(stopwords.words('english'))

# setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ### 1. Clean Webpage Content Function

# In[12]:


def clean_webpage_content(webpage_content):
    # Remove JavaScript code
    webpage_content = re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', '', webpage_content, flags=re.DOTALL)

    # Remove HTML tags
    webpage_content = re.sub(r'<[^>]+>', '', webpage_content)

    # Remove unwanted phrases using regex
    unwanted_phrases = [
        r'.*?Claim close',
        r'Integrations arrow_right_alt.*?Key Features arrow_right_alt',
        r'ComparisonsBotPenguin Vs.*?LandbotProduct What do\?Who use it\?Where run\?',
        r'Pricing Chatbot Pricing \(except WA\) arrow_right_alt.*?Website, Telegram, Facebook Live Chat bots',
        r'Partners Partners Home arrow_right_alt.*?Earn clients happierImplementation Partners arrow_right_alt',
        r'expand_more Integrations arrow_right_alt.*?expand_more DO MORE Chat Automation!',
        re.escape('arrow_right_alt'),
        re.escape('Enter Name*Enter Email*+ expand_more Enter Phone NumberEnter Facebook Page Link*10k 100k100k 1Mn1Mn 3Mn3Mn 10Mn10Mn+ Select number followers*Less 100k100k 500k500k+ Select number FB messages get*Enter informationCancelClaimBy submitting form agree terms. View privacy policy learn use information.')
    ]
    for phrase in unwanted_phrases:
        webpage_content = re.sub(phrase, '', webpage_content, flags=re.DOTALL)

    # Remove stopwords using nltk
    webpage_content = ' '.join(
        word for word in webpage_content.split()
        if word.lower() not in stop_words
    )

    # Remove extra whitespaces
    webpage_content = ' '.join(webpage_content.split())

    return webpage_content


# ### 2. Extract Links Function with Relative & Absolute Handling

# In[13]:


def links(website_html: str) -> dict:
    soup = BeautifulSoup(website_html, 'html.parser')
    base_url = 'https://botpenguin.com'
    links_dict = {}
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        if not href or href.startswith('javascript'):
            continue
        if href.startswith('http'):
            full_url = href
        else:
            full_url = base_url + href
        key = href.strip('/').replace('/', '_') or 'root'
        links_dict[key] = full_url
    return links_dict


# ### 3. Scrape Function with Request & Parsing Error Handling

# In[14]:


def scrape_and_store(url, label):
    logger.info(f"Scraping {label} ({url})")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error making request to {url}: {e}")
        return None, None

    if response.status_code != 200:
        logger.error(f"Non-200 status code from {url}: {response.status_code}")
        return None, None

    try:
        soup = BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        logger.error(f"Error parsing HTML from {url}: {e}")
        return None, None

    website_html = soup.prettify()
    links_list = links(website_html)
    logger.info(f"Links found on {label}: {len(links_list)}")
    website_content = soup.get_text()

    return website_content, links_list


# ### 4. Main Execution Block with Pickle Saving

# In[16]:


if __name__ == '__main__':
    website_urls = {"Home page": "https://botpenguin.com/"}

    try:
        with open('scraped_data.pkl', 'rb') as file:
            all_data = pickle.load(file)
    except FileNotFoundError:
        all_data = []

    for label, url in website_urls.items():
        website_content, links_list = scrape_and_store(url, label)

        if website_content is None:
            continue

        cleaned_content = clean_webpage_content(website_content)

        if cleaned_content:
            data = {'label': label, 'context': cleaned_content, 'links': links_list}
            all_data.append(data)
            logger.info(f"{label} data extracted and cleaned.")

    # Save all data to pickle
    with open('scraped_data.pkl', 'wb') as file:
        pickle.dump(all_data, file)
    logger.info("All data saved to scraped_data.pkl.")


# In[ ]:




