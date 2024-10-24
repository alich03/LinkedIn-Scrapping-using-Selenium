import requests
 
url = "https://api.prospeo.io/linkedin-email-finder"

api_key = "f89fbdb9d026ff4aa2fc55a494a726e8"
 
required_headers = {
    'Content-Type': 'application/json',
    'X-KEY': api_key
}

data = {
    'url': 'https://www.linkedin.com/in/ali-hasnain-ai'
}
 
response = requests.post(url, json=data, headers=required_headers)

print(response.json())