import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from dotenv import load_dotenv
load_dotenv()


def extract_linkedin_details(search_input):
    try:
        login_url = "https://www.linkedin.com/login"

        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        chrome_options.add_argument("--disable-webrtc")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        chrome_options.add_argument('--disable-ipv6')
        chrome_options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(options=chrome_options)
        print("Logging into LinkedIn...")
        
        # Login process
        driver.get(login_url)
        email = os.environ.get("email")
        psd = os.environ.get("psd")
        if not email or not psd:
            raise ValueError("Email or password environment variables are not set.")
        
        driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(email)
        driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(psd, Keys.ENTER)
        time.sleep(2)
        print(f"Searching for {search_input}...")

        # Data storage
        data = {}

        # Page navigation
        for pages in range(1, 3):
            searching_url = f"https://www.linkedin.com/search/results/people/?keywords={search_input}&origin=SWITCH_SEARCH_VERTICAL&page={pages}&sid=!yR"
            driver.get(searching_url)
            time.sleep(5)

            elements = driver.find_elements(By.CLASS_NAME, "reusable-search__result-container")
            print(f"Finding {len(elements)} people on page {pages}...")

            for element in elements:
                    
                    profile_url = element.find_element(By.CLASS_NAME, 'entity-result__title-text').find_element(By.CLASS_NAME, 'app-aware-link ').get_attribute("href")
                    name = element.find_element(By.CLASS_NAME, 'entity-result__title-text').find_element(By.CLASS_NAME, 'app-aware-link ').text.split("\n")[0]
                    try:
                        title = element.find_element(By.CLASS_NAME, 'entity-result__primary-subtitle').text
                    except:
                        title ="Not Available"
                    try:
                        location = element.find_element(By.CLASS_NAME, 'entity-result__secondary-subtitle').text
                    except:
                        location = "Not Available"

                    # Print results
                    print("Name:", name)
                    # print("Profile URL:", profile_url)
                    # print("Title:", title)
                    # print("Location:", location)
                    print("........................")

                    # Add to data dictionary
                    if not data:
                        data = {
                            "Name": [name],
                            "Profile URL": [profile_url],
                            "Profile Title": [title],
                            "Location": [location]
                        }
                    else:
                        data["Name"].append(name)
                        data["Profile URL"].append(profile_url)
                        data["Profile Title"].append(title)
                        data["Location"].append(location)

                    # Save to CSV after each page
                    df = pd.DataFrame(data)
                    df.to_csv(f'data/{search_input}_on_linkedin.csv', index=False)


        driver.quit()
        print("Data extraction completed successfully.")

    except WebDriverException as e:
        print(f"WebDriver error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")




if __name__ == "__main__":
    
    search_term = "hr"  
    extract_linkedin_details(search_term)

