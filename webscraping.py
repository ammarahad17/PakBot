import pandas as pd
import requests
from bs4 import BeautifulSoup
import string

# Read the list of topic names from the text file
text = pd.read_csv('pakistan_topics.txt', header=None, names=['topic'])

# Create a list to store all scraped data
all_data = []

# Iterate through each topic name
for topic in text['topic']:
    # Capitalize the words and join with underscores to create the modified topic
    modified_topic = '_'.join(string.capwords(topic).split())

    # URL of the web page you want to scrape
    url = 'https://en.wikipedia.org/wiki/' + modified_topic + '#bodyContent'

    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find all paragraphs (p) in the page
        paragraphs = soup.find_all('p')

        # Create a list to store the scraped data for this topic
        data = []

        # Iterate through the paragraphs and append them to the data list
        for paragraph in paragraphs:
            data.append(paragraph.get_text())
            # Append the data for this topic to the list of all data
        all_data.extend(data)
    else:
        print(f"Page for topic '{topic}' not found. Moving to the next topic.")

# Create a DataFrame from all the scraped data
df = pd.DataFrame({'Data': all_data})

# Save the DataFrame to a single CSV file
df.to_csv('WikiPakistan.csv', index=False)

print("All data saved to WikiPakistan.csv")
