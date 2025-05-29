#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests
import os
import _pickle
import time


# In[3]:


# Define the API URL and headers
API_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"

# Try to get API key from environment variable; if not found, prompt user to input it
if 'API_KEY' in os.environ:
    api_key = os.getenv('API_KEY')
else:
    api_key = str(input('Enter HF API KEY:'))

# Raise an error if API key is still not provided
if not api_key:
    raise ValueError("API_KEY environment variable is not set")
headers = {"Authorization": f"Bearer {api_key}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


# In[4]:


def chatbot(question, context):
    for _ in range(3):  # Retry up to 3 times
        try:
            output = query({
                "inputs": {
                    "question": question,
                    "context": context,
                },
            })
            if 'error' in output and 'loading' in output['error'].lower():
                wait_time = output.get("estimated_time", 5)
                print(f"Model loading. Retrying in {wait_time} sec...")
                time.sleep(wait_time)
                continue
            return output
        except Exception as e:
            print("An error occurred:", e)
            return None
    return {"error": "Model did not respond in time."}


# In[5]:


def extract_answer(output):
    if isinstance(output, dict):
        if "answer" in output:
            return output["answer"]
        elif "error" in output:
            return f"Error from model: {output['error']}"
        else:
            return f"Unexpected response format: {output}"
    elif isinstance(output, list) and len(output) > 0 and isinstance(output[0], dict):
        return output[0].get("answer", "Answer key not found in list response.")
    else:
        return "Invalid or unrecognized response format."


# In[6]:


# Load scraped webpage content from pickle file to use as context
with open("scraped_data.pkl", "rb") as f:
    loaded_data = _pickle.load(f)
context = loaded_data[0].get('context', None)

# Interactive loop to ask questions until user types 'exit'
while True:
    question = input("Ask a question or exit: ")
    if question.lower() == 'exit':
        break
    output = chatbot(question, context)
    answer = extract_answer(output)
    print(f"Generating answer: {answer}\n\n", end='')


# In[ ]:




