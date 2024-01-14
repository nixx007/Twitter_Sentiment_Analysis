from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import pandas as pd

class TwitterScraper:
    def __init__(self, username, phone, password, keywords):
        """
        Initialize TwitterScraper instance with provided username, password, and keywords.

        Parameters:
        - username (str): Twitter account username
        - phone    (str): User's Phone number 
        - password (str): Twitter account password
        - keywords (list): List of keywords to search for in tweets
        """
        self.username = username
        self.phone = phone
        self.password = password
        self.keywords = keywords
        self.driver = self.setup_driver()

    def setup_driver(self):
        """
        Set up the Chrome WebDriver with options.

        Returns:
        - webdriver.Chrome: Configured Chrome WebDriver
        """
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument("--no-sandbox")
        options.add_experimental_option("detach", True)
        return webdriver.Chrome(options=options)

    def login(self):
        """
        Perform Twitter login using the provided username and password.
        """
        self.driver.get("https://twitter.com/login")
        time.sleep(5)
        username = self.driver.find_element(By.XPATH,"//input[@name='text']")
        username.send_keys(self.username)

        next_button = self.driver.find_element(By.XPATH,"//span[contains(text(),'Next')]")
        next_button.click()

        time.sleep(5)

        username = self.driver.find_element(By.XPATH,"//input[@name='text']")
        username.send_keys(self.phone)

        next_button = self.driver.find_element(By.XPATH,"//span[contains(text(),'Next')]")
        next_button.click()

        password = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='password']"))
        )
        password.send_keys(self.password)

        log_in = self.driver.find_element(By.XPATH,"//span[contains(text(),'Log in')]")
        log_in.click()
        time.sleep(5)

    def search_tweets(self):
        """
        Search for tweets using the specified keywords.
        """
        self.driver.get("https://twitter.com/explore")
        query = f"({' OR '.join(self.keywords)})"
        time.sleep(5)

        search_box = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Search query']"))
        )
        search_box.send_keys(query)
        search_box.send_keys(Keys.ENTER)

        time.sleep(5)

    def scrape_tweets(self):
        """
        Scrape tweets based on the search results.
        """
        self.UserTags=[]
        self.TimeStamps=[]
        self.Tweets=[]
        self.Replys=[]
        self.reTweets=[]
        self.Likes=[]

        last_height = self.driver.execute_script("return document.body.scrollHeight")
        current_scroll_position = 0
        articles = self.driver.find_elements(By.XPATH,"//article[@data-testid='tweet']")

        while True:

            for article in articles:
            
                UserTag = self.driver.find_element(By.XPATH,".//div[@data-testid='User-Name']")
                self.UserTags.append(UserTag.text)

                TimeStamp = WebDriverWait(self.driver,3).until(EC.presence_of_element_located((By.XPATH,".//time")))
                self.TimeStamps.append(TimeStamp.get_attribute('datetime'))

                Tweet = WebDriverWait(self.driver,3).until(EC.presence_of_element_located((By.XPATH,".//div[@data-testid='tweetText']"))).text
                self.Tweets.append(Tweet)

                Reply = WebDriverWait(self.driver,3).until(EC.presence_of_element_located((By.XPATH,".//div[@data-testid='reply']"))).text
                self.Replys.append(Reply)

                reTweet = WebDriverWait(self.driver,3).until(EC.presence_of_element_located((By.XPATH,".//div[@data-testid='retweet']"))).text
                self.reTweets.append(reTweet)

                Like = WebDriverWait(self.driver,3).until(EC.presence_of_element_located((By.XPATH,".//div[@data-testid='like']"))).text
                self.Likes.append(Like)

            current_scroll_position += 2000

            self.driver.execute_script('window.scrollTo(0, {});'.format(current_scroll_position))
            time.sleep(10)

            new_height = self.driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break
            last_height = new_height

            # find all tweet articles again to check if there are more tweets to scrape
            articles = self.driver.find_elements(By.XPATH,"//article[@data-testid='tweet']")
            Tweets_unique = list(set(self.Tweets))
            if len(Tweets_unique) > 100:
                break

    def save_to_csv(self, filename="twitter_data.csv"):
        """
        Save scraped data to a CSV file.

        Parameters:
        - filename (str): Name of the CSV file (default is "twitter_data.csv")
        """
        data = pd.DataFrame({
            'UserTags': self.UserTags,
            'TimeStamps': self.TimeStamps,
            'Tweets': self.Tweets,
            'Replys': self.Replys,
            'reTweets': self.reTweets,
            'Likes': self.Likes
        })
        data.to_csv(filename)

    def close_driver(self):
        """
        Close the Chrome WebDriver.
        """
        self.driver.quit()

# Usage
if __name__ == "__main__":
    username = "your_id"
    phone = "your_phone"
    password = "your_password"
    keywords = ["Imbruvica", "Ibrutinib", "Abbvie", "Imbruvica pricing", "Imbruvica drug"]

    scraper = TwitterScraper(username, phone, password, keywords)
    scraper.login()
    scraper.search_tweets()
    scraper.scrape_tweets()
    scraper.save_to_csv()
    scraper.close_driver()
