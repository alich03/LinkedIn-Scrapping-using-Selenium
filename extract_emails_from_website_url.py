import requests
from bs4 import BeautifulSoup
import re
import numpy as np

# URL of the website you want to scrape
# Define headers to mimic a browser request
#start function

def extract_email_from_web(url):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
    # Send a request to the website
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the page content
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract and concatenate text while preserving spaces between tags
        extracted_text = []
        for element in soup.descendants:
            if isinstance(element, str):
                extracted_text.append(element.strip())
            elif element.name not in ['style', 'script', 'head', 'title', 'meta', '[document]']:
                if element.string and element.string.strip():
                    extracted_text.append(element.string.strip())
                extracted_text.append(' ')  # Add a space after each tag ends
        # Join all pieces into a single string and clean up excessive spaces
        page_text = ' '.join(extracted_text).strip()
        # Define the regular expression pattern for emails
        email_pattern = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'
        # Find all occurrences of the pattern
        emails = re.findall(email_pattern, page_text)
        # Print the extracted emails
        all_mails = ""
        if emails:
            # print("Emails found:")
            for email in set(emails):  # Use set to avoid duplicates
                # Removing the extra characters after the domain
                d_len = len(email.split(".")[-1])
                if d_len > 3:
                    domain = d_len - 3
                    email = email[:-domain]
                # print(email)
                all_mails = all_mails+email+","
            return all_mails
        else:
            # print("No emails found.")
            return np.nan
    else:
        # print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return np.nan



url ="https://www.digimarkdevelopers.com/"

output = extract_email_from_web(url)

print(output)