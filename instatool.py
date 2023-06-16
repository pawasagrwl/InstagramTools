from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
from itertools import chain, combinations

class InstagramTools:

    # Class Initializer
    def __init__(self, username, password, headless=False):
        self.username = username 
        self.password = password 
        options = Options()
        if headless:
            options.add_argument("-headless")
        print (set)
        self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

    # method to login into your account
    def login(self): 
        self.driver.get("https://www.instagram.com/")
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys(self.username)
        time.sleep(0.5)
        password_box = self.driver.find_element(By.NAME, 'password')
        password_box.send_keys(self.password)
        time.sleep(0.5)
        password_box.send_keys(Keys.RETURN)
        time.sleep(10)
        try:
            WebDriverWait(self.driver, 5).until(EC.url_contains('two_factor'))
            print("Two Factor Authentication Required!")
            code = input("Enter code: ")
            code_box = self.driver.find_element(By.NAME, 'verificationCode')
            code_box.send_keys(code)
            time.sleep(0.5)
            code_box.send_keys(Keys.RETURN)
            time.sleep(10)
        except Exception:
            print("Logged in without 2FA.")


    # method to get followers of a given account
    def get_followers(self, username): 
        self.driver.get(f"https://www.instagram.com/{username}")
        time.sleep(2)
        followers_number = self.driver.find_element(By.XPATH, "//*[@id='react-root']/section/main/div/header/section/ul/li[2]/*/span").text
        followers_number = self._convert_str_num(followers_number)
        followers_accounts = self._scroll_and_collect(followers_number, 'followers')
        return followers_accounts
        
    # method to get followings of given account
    def get_followings(self, username): 
        self.driver.get(f"https://www.instagram.com/{username}")
        time.sleep(2)
        following_number = self.driver.find_element(By.XPATH, "//*[@id='react-root']/section/main/div/header/section/ul/li[3]/*/span").text
        following_number = self._convert_str_num(following_number)
        following_accounts = self._scroll_and_collect(following_number, 'following')
        return following_accounts
    
    # method to get urls of all saved posts
    def get_saved_posts(self):
        self.driver.get(f"https://www.instagram.com/{self.username}/saved/all-posts/")
        time.sleep(2)
        saved_posts_urls = []

        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            a_elements = self.driver.find_elements(By.XPATH, "//div[contains(@class, '_aabd')]/a")
            for a in a_elements:
                url = a.get_attribute("href")
                if url not in saved_posts_urls:
                    saved_posts_urls.append(url)

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:  # reached end of page
                break
            last_height = new_height
        
        with open(f'{self.username}_saved_posts.txt', 'w') as f:
            for url in saved_posts_urls:
                f.write(url + '\n')
        
        return saved_posts_urls
    
    # method to save posts from list of urls
    def save_posts(self, urls_filename):
        with open(urls_filename, 'r') as f:
            urls = f.readlines()
        saved_urls = set(self.get_saved_posts())
        urls = [url for url in urls if url not in saved_urls]
        print ("Number of posts to save: ", len(urls))
        for url in urls:
            url = url.strip()  # remove any leading/trailing whitespace and newline characters
            self.driver.get(url)
            try:
                wait = WebDriverWait(self.driver, 2)
                wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[3]/div[1]/div[3]/div/div/button")))
                save_button = self.driver.find_elements(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[3]/div[1]/div[3]/div/div/button")
                try:
                    save_button[0].click()
                    time.sleep(3)
                except Exception as e:
                    print("Failed due to:", str(e))
            except Exception as e:
                print("Failed due to:", str(e))
            time.sleep(1)  # wait for 10 seconds
    
    # method to open posts from a list of urls to save
    def open_posts(self, urls_filename):
        with open(urls_filename, 'r') as f:
            urls = f.readlines()
        saved_urls = set(self.get_saved_posts())
        urls = [url for url in urls if url not in saved_urls]
        print ("Number of posts to save: ", len(urls))
        count = 0
        for url in urls:
            print (count)
            url = url.strip()  # remove any leading/trailing whitespace and newline characters
            self.driver.get(url)
            input("Enter any key to continue..")
            count += 1
    
    def _convert_str_num(self, str_num):
        num = ""
        for char in str_num:
            if char.isdigit():
                num += char
        num = int(num)
        if "." in str_num:
            num /= 10
        if "m" in str_num:
            num += 1
            num *= 1000000
        elif "k" in str_num:
            num += 1
            num *= 1000
        return num

    def _scroll_and_collect(self, count, type):
        accounts = []
        if count > 0:
            button = self.driver.find_element(By.XPATH, f"//a[contains(@href, '{type}')]")
            button.click()
            time.sleep(2)
            counter = 0
            while counter < (count/2.5):  
                self.driver.find_element(By.XPATH, "//div[@class='isgrP']").send_keys(Keys.PAGE_DOWN)
                counter += 1
                time.sleep(0.2)
            account_elements = self.driver.find_elements(By.XPATH, "//a[@class='FPmhX notranslate  _0imsa ']")
            accounts = [account.get_attribute('title') for account in account_elements]
        return accounts

def main():
    username = input("Enter username: ")
    password = input("Enter password: ")
    tool = InstagramTools(username, password)
    tool.login()
    tool.open_posts("saved_urls.txt")
    # rest of your code here...

if __name__ == "__main__":
    main()
