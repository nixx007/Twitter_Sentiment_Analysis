from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import time
import pandas as pd

options = webdriver.ChromeOptions()
options.headless= True
options.add_argument("--no-sandbox")
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)
url="https://twitter.com/login"
driver.get(url)
time.sleep(5)
print(driver.current_url)

username = driver.find_element(By.XPATH,"//input[@name='text']")
username.send_keys("chauhannishaant@gmail.com")

next_button = driver.find_element(By.XPATH,"//span[contains(text(),'Next')]")
next_button.click()

time.sleep(5)

username = driver.find_element(By.XPATH,"//input[@name='text']")
username.send_keys('9877688635')

next_button = driver.find_element(By.XPATH,"//span[contains(text(),'Next')]")
next_button.click()

password = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//input[@name='password']"))
)
password.send_keys('Test@12345')

log_in = driver.find_element(By.XPATH,"//span[contains(text(),'Log in')]")
log_in.click()

time.sleep(5)

driver.get("https://twitter.com/explore")
keywords = ["Imbruvica", "Ibrutinib", "Abbvie", "Imbruvica pricing", "Imbruvica drug"]
query = f"({' OR '.join(keywords)})"
time.sleep(5)

search_box = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Search query']"))
)
search_box.send_keys(query)
search_box.send_keys(Keys.ENTER)

time.sleep(5)

UserTags=[]
UserProfessions = []
TimeStamps=[]
Tweets=[]
Replys=[]
reTweets=[]
Likes=[]

last_height = driver.execute_script("return document.body.scrollHeight")
current_scroll_position = 0
articles = driver.find_elements(By.XPATH,"//article[@data-testid='tweet']")
print(articles, len(articles))

while True:
    for article in articles:

        UserTag = driver.find_element(By.XPATH,".//div[@data-testid='User-Name']")
        UserTags.append(UserTag.text)
        # UserTag.click()
        # time.sleep(3)
        # UserProfession = driver.find_element(By.XPATH,".//span[@data-testid='UserProfessionalCategory']").text
        # UserProfessions.append(UserProfession)
        # back = driver.find_element(By.XPATH,".//div[@data-testid='app-bar-back']")
        # time.sleep(2)
        # back.click()
        # time.sleep(3)

        TimeStamp = WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH,".//time")))
        TimeStamps.append(TimeStamp.get_attribute('datetime'))

        Tweet = WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH,".//div[@data-testid='tweetText']"))).text
        Tweets.append(Tweet)

        Reply = WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH,".//div[@data-testid='reply']"))).text
        Replys.append(Reply)

        reTweet = WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH,".//div[@data-testid='retweet']"))).text
        reTweets.append(reTweet)

        Like = WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH,".//div[@data-testid='like']"))).text
        Likes.append(Like)
    
    current_scroll_position += 3000

    driver.execute_script('window.scrollTo(0, {});'.format(current_scroll_position))
    time.sleep(10)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")

    # break condition
    if new_height == last_height:
        break
    last_height = new_height

    # find all tweet articles again to check if there are more tweets to scrape
    articles = driver.find_elements(By.XPATH,"//article[@data-testid='tweet']")
    Tweets2 = list(set(Tweets))
    if len(Tweets2) > 100:
        break

driver.quit()
    
print(len(UserTags), len(UserProfessions), len(TimeStamps), len(Tweets), len(Replys), len(reTweets), len(Likes))

data = pd.DataFrame({
    'UserTags': UserTags,
    # 'UserProfessions' : UserProfessions, 
    'TimeStamps': TimeStamps,
    'Tweets': Tweets,
    'Replys': Replys,
    'reTweets': reTweets,
    'Likes':Likes
})

data.to_csv("twitter_data_05.csv")



