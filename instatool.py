from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import math

class InstagramTools:

    # Class Initializer
    def __init__(self, username, password):
        self.username = username # the username of your instagram account
        self.password = password # the password of your instagram account
        self.driver = webdriver.Firefox(executable_path=r'C:\Program Files\geckodriver.exe') #specifies the driver which you want to use)

    # method to login into your account
    def login(self): 
        driver = self.driver
        driver.get("https://www.instagram.com/")
        time.sleep(2)
        username_box = driver.find_element_by_xpath("//input[@name='username']")
        username_box.clear()
        username_box.send_keys(self.username)
        time.sleep(2)
        password_box = driver.find_element_by_xpath("//input[@name='password']")
        password_box.clear()
        password_box.send_keys(self.password)
        time.sleep(2)
        password_box.send_keys(Keys.RETURN)
        time.sleep(3)

    # method to get followers of a given account
    def get_followers(self, username): 
        self.driver.get("https://www.instagram.com/%s/"%(username))
        time.sleep(2)
        buttons = self.driver.find_elements_by_xpath("//a[@class='-nal3 ']")
        followers_number = self.driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/*/span").text
        self.followers_number = strToNum(followers_number)
        self.followers_accounts = []
        
        if (0 < self.followers_number):      # Only scan if atleast 1 follower
            self.followers_button = [button for button in buttons if 'followers' in button.get_attribute('href')]
            self.followers_button[0].click()
            time.sleep(2)
            self.followers_window = self.driver.find_element_by_xpath("//div[@class='isgrP']")
            counter = 0
            while counter < (self.followers_number/2.5):  
                self.followers_window.send_keys(Keys.PAGE_DOWN)
                counter = counter + 1
                time.sleep(0.2)
            self.followers_accounts = self.driver.find_elements_by_xpath("//a[@class='FPmhX notranslate  _0imsa ']")
            self.followers_accounts = [account.get_attribute('title') for account in self.followers_accounts]

            # condition to make sure all followers are scanned
            if (len(self.followers_accounts) < self.followers_number - 2): 
                return self.get_followers(username)
        return self.followers_accounts
        
    # method to get followings of given account
    def get_followings(self, username): 
        self.driver.get("https://www.instagram.com/%s/"%(username))
        time.sleep(2)
        buttons = self.driver.find_elements_by_xpath("//a[@class='-nal3 ']")
        following_number = self.driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[3]/*/span").text
        self.following_number = strToNum(following_number)
        self.following_accounts = []
        
        if (0 < self.following_number <= 1000):
            self.following_button = [button for button in buttons if 'following' in button.get_attribute('href')]
            self.following_button[0].click()
            time.sleep(2)
            self.following_window = self.driver.find_element_by_xpath("//div[@class='isgrP']")
            counter = 0
            while counter < (self.following_number/2.5):  
                self.following_window.send_keys(Keys.PAGE_DOWN)
                counter = counter + 1
                time.sleep(0.2)
            self.following_accounts = self.driver.find_elements_by_xpath("//a[@class='FPmhX notranslate  _0imsa ']")
            self.following_accounts = [account.get_attribute('title') for account in self.following_accounts]

            # condition to make sure all followers are scanned
            if (len(self.following_accounts) < self.following_number - 2):
                return self.get_followings(username)
        return self.following_accounts

    # method to get all available details of a given user
    def get_user_details(self, username):
        self.driver.get('https://www.instagram.com/'+username+'/?hl=en')
        user_name = self.driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/div[2]/h1").text
        user_bio =  self.driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/div[2]/span").text
        user_url = self.driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/div[2]/a").text
        user_postsNo = strToNum(self.driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[1]/*/span").text)
        return [user_name, user_bio, user_url, user_postsNo, self.get_followers(username), self.get_followings(username)]
    
    # method to find mutual followers between a given set of users
    def find_mutual_followers(self, usernames):
        usernamesDict = dict()

        # scan list of all followers for each user
        all_followers = []
        for username in usernames:
            usernamesDict[usernames.index(username)] = username
            followers = set(self.get_followers(username))
            all_followers.append(followers)

        # make powerset of users to get all subset of users
        powset = powerset(all_followers)
        mutual_followers = dict()
        n = 0

        # find common following through set intersection for every subset of users
        for subset in powset:
            users = []
            for sets in subset:
                users.append(usernamesDict[all_followers.index(sets)])
            intersected = setsIntersection(subset)
            mutual_followers[n] = [users,intersected]
            n += 1
        return mutual_followers

    # method to find mutual followings between a given set of users
    def find_mutual_followings(self, usernames):
        usernamesDict = dict()

        # scan list of all followers for each user
        all_followings = []
        for username in usernames:
            usernamesDict[usernames.index(username)] = username
            followings = set(self.get_followings(username))
            all_followings.append(followings)
        
        # make powerset of users to get all subset of users
        powset = powerset(all_followings)
        mutual_followings = dict()
        n = 0

        # find common following through set intersection for every subset of users
        for subset in powset:
            users = []
            for sets in subset:
                users.append(usernamesDict[all_followings.index(sets)])
            intersected = setsIntersection(subset)
            mutual_followings[n] = [users,intersected]
            n += 1
        return mutual_followings
    
    # method to get all available details for a post
    def get_post_details(self, posturl):
        self.driver.get(posturl)
        time.sleep(2)
        username = self.driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div/article/header/div[2]/div/div/span/a").text
        post_date = self.driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div/article/div[3]/div[2]/a/time").get_attribute("title")
        
        # get the post's user's followers number to scrape liked properly
        self.driver.get('https://www.instagram.com/'+username)
        followers_number = strToNum(self.driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/*/span").text)
        time.sleep(2)

        # Scrape post likes
        self.driver.get(posturl)
        time.sleep(2)
        if (0 < followers_number):
            others_button = self.driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div/article/div[3]/section[2]/div/div/button")
            others_button.click()
            time.sleep(2)
            like_window = self.driver.find_element_by_xpath("//div[@class='pbNvD  fPMEg    ']/div/div[3]/div")
            counter = 0
            liked_accountsTemp = []
            while counter < (followers_number/3):  
                like_accounts = self.driver.find_elements_by_xpath("//a[@class='FPmhX notranslate MBL3Z']")
                for account in like_accounts:
                    liked_accountsTemp.append(account.get_attribute('title'))
                like_window.send_keys(Keys.PAGE_DOWN)
                counter = counter + 1
                time.sleep(0.2)

            # remove duplicates    
            liked_accounts = []
            for liked_account in liked_accountsTemp:
                if liked_account not in liked_accounts:
                    liked_accounts.append(liked_account)
        post_details = [username, post_date, liked_accounts, followers_number]
        return (post_details)

    # method to get urls of all posts of a given user
    def get_posts_url(self, username):
        self.driver.get('https://www.instagram.com/'+username)

        # scroll until end of page to get all post urls in the DOM
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        posts_urlsTemp = []
        while True:
            post_urls = self.driver.find_elements_by_xpath("//div[@class='v1Nh3 kIKUG  _bz0w']/a")
            for element in post_urls:
                posts_urlsTemp.append(element.get_attribute("href"))
            self. driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        # remove duplicates
        posts_urls = []
        for post_url in posts_urlsTemp:
            if post_url not in posts_urls:
                posts_urls.append(post_url)
        return (posts_urls)
    
    # method to check if a given set of users like a a givem number of post of a user or not
    def check_if_liked_by(self, usernames, username, no_of_posts):

        # get posts urls of all posts of the user
        main_posts_url = self.get_posts_url(username)
        posts = dict()
        username_likes = dict()

        # loop until given numbero of posts
        for url in main_posts_url[:no_of_posts]:

            # get post details
            post_detail = self.get_post_details(url)
            posts[url] = post_detail
            username_likes[url] = dict()

            # check if given set of users have liked the post
            for username in usernames:
                if username in post_detail[2]:
                    username_likes[url][username] = True
                else:
                    username_likes[url][username] = False 
        return username_likes
        
def strToNum(strNum):
    num = ""
    for char in strNum:
        if char in ["0","1","2","3","4","5","6","7","8","9"]:
            num += char
    num = int(num)
    if "." in strNum:
        num /= 10
    if "m" in strNum:
        num += 1
        num *= 1000000
    if "k" in strNum:
        num += 1
        num *= 1000
    return num


def setsIntersection(sets):
    intersected = sets[0]
    for i in range(1, len(sets)):
        intersected = intersected.intersection(sets[i])
    return intersected

def powerset(s):
    x = len(s)
    powset = []
    for i in range(1,1 << x):
        subset = ([s[j] for j in range(x) if (i & (1 << j))])
        if len(subset) > 1:
            powset.append(subset)
    return powset


def main():
    username = input("username: ")
    password = input("password: ")
    tool = InstagramTools(username,password)
    tool.login() #logins your account
    time.sleep(3)
if __name__ == "__main__":
    main()