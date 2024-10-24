from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.chrome.options import Options


url = "https://www.google.com/maps/"

options = Options()
# options.add_argument("--headless")
driver = webdriver.Chrome( options=options)
driver.get(url)

xpath = '//*[@id="searchboxinput"]'
chrome_input = driver.find_element(By.XPATH, xpath)

req_loc = "xeven solutions"
chrome_input.send_keys(req_loc)

chrome_input.send_keys(Keys.ENTER)

sleep(6)

#reviews button
driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div/div/button[2]/div[2]/div[2]').click()
sleep(6)

scroll_elem = driver.find_element(By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]')

for i in range(10):
    driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scroll_elem)
    print(f"Scroll {i+1}")
    sleep(3)

reviews = driver.find_elements(By.CLASS_NAME, 'jftiEf')

sleep(5)

print(len(reviews))

name_list = []
text_list = []
when_list = []
stars_list = []
no_rws_list = []
for review in reviews:
        try:
            name = review.find_element(By.CLASS_NAME, 'd4r55').text
            when = review.find_element(By.CLASS_NAME, 'rsqaWe').text
            stars = review.find_element(By.CLASS_NAME, 'kvMYJc').get_attribute("aria-label")

            try:
                no_reviews = review.find_element(By.CLASS_NAME, 'RfnDt ').text
            except:
                 no_reviews = "0 reviews"
            
            try:
                text = review.find_element(By.CLASS_NAME, 'wiI7pd').text
            except:
                 text="no review found"

        except Exception as e:
            print(f"Error: {e}")

        # sleep(2)

        # print(review.index)
        # print(no_reviews)
        # print(when)
        # print(stars)
        
        name_list.append(name)
        text_list.append(text)
        when_list.append(when)
        stars_list.append(stars)
        no_rws_list.append(no_reviews)

# creating csv
import pandas as pd

data = {
    'Name': name_list,
    'Review Text': text_list,
    'Date': when_list,
    'Rating': stars_list,
    'Number of Reviews': no_rws_list
}

df= pd.DataFrame(data)

df.to_csv(f'Gmap_Reviews_Data/{req_loc}_reviews.csv', index=False, encoding='utf-8')





