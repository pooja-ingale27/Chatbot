# Chatbot

Project Goal:

To create a chatbot that can answer questions based on the content of a webpage by:

•	Scraping text from a URL.

•	Processing and cleaning the content.

•	Using a question-answering (Q&A) model from Hugging Face to generate answers.


Method:

1.	Setup required libraries
   
•	Imported Python libraries such as requests, BeautifulSoup, re, pickle, nltk, etc.

•	Enabled logging to track the process.

•	downloaded NLTK stopwords for filtering unnecessary words from the text. (Download just the first time)


2.	Created Web Scraper script (Web_Scraper.py)
   
2.1.	Cleaning Webpage Content

Wrote a function to:

•	Remove JavaScript and HTML tags from the webpage.

•	Remove unwanted phrases using regular expressions.

•	Remove common English stopwords to keep the text relevant and clean.



2.2.	Extracting All Links

•	Created a function to find and store all clickable links from the webpage.

•	Handled both relative and absolute URLs properly.


2.3.	Scraping and Parsing Webpage

Created a function to:

•	Send an HTTP request to the webpage.

•	Check for response errors.

•	Extract text and links using BeautifulSoup.


2.4.	Running the Scraper and Saving Data

•	Scraped data from https://botpenguin.com/.

•	Cleaned the scraped content.

•	Saved the cleaned content, label, and links into a .pkl file using pickle.


3.	Built the Chatbot Script (API.py)
   
3.1.	Connect to Hugging Face and QA Model.

•	Used the model: deepset/roberta-base-squad2.

•	Required an API key (fetched from .env or user input).


3.2.	Define Chatbot Function

•	Created a function to send the user's question and context (webpage text) to the model.


3.3.	Load Scraped Data for Chatbot Context

•	Loaded the cleaned webpage content from the .pkl file created earlier.

•	Used this content as the chatbot's context for answering questions.


3.4.	Extract Answer from Model

•	Extracted the "answer" field from the model’s response and handled errors or unexpected formats.

3.5.	Interactive Chat Loop

•	Added a loop so users can keep asking questions until they type exit.







