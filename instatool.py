from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
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
        self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

    # method to login into your account
    def login(self): 
        self.driver.get("https://www.instagram.com/")
        time.sleep(2)
        self.driver.find_element(By.NAME, 'username').send_keys(self.username)
        time.sleep(2)
        password_box = self.driver.find_element(By.NAME, 'password')
        password_box.send_keys(self.password)
        time.sleep(2)
        password_box.send_keys(Keys.RETURN)
        time.sleep(3)

    # method to get followers of a given account
    def get_followers(self, username): 
        self.driver.get(f"https://www.instagram.com/{username}")
        time.sleep(2)
        followers_number = self.driver.find_element(By.XPATH, "//*[@id='react-root']/section/main/div/header/section/ul/li[2]/*/span").text
        followers_number = self._convert_str_num(followers_number)
        followers_accounts = self._scroll_and_collect(followers_number, 'followers', username)
        return followers_accounts
        
    # method to get followings of given account
    def get_followings(self, username): 
        self.driver.get(f"https://www.instagram.com/{username}")
        time.sleep(2)
        following_number = self.driver.find_element(By.XPATH, "//*[@id='react-root']/section/main/div/header/section/ul/li[3]/*/span").text
        following_number = self._convert_str_num(following_number)
        following_accounts = self._scroll_and_collect(following_number, 'following', username)
        return following_accounts

    # rest of the class methods here...

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

    def _scroll_and_collect(self, count, type, username):
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
    # rest of your code here...

if __name__ == "__main__":
    main()
