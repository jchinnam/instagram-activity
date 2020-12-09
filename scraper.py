import itertools

from explicit import waiter, XPATH
from selenium import webdriver
import time
import os

# pull user vars from keys.json
def read_keys():
    with open('keys.json') as file:
      keys = json.load(file)

    username = keys["username"]
    password = keys["password"]
    driver_path = keys["driver_path"]

    return username, password, driver_path

def login(driver, username, password):
    # load page
    driver.get("https://www.instagram.com/accounts/login/")

    # login
    waiter.find_write(driver, "//div/label/input[@name='username']", username, by=XPATH)
    waiter.find_write(driver, "//div/label/input[@name='password']", password, by=XPATH)
    waiter.find_element(driver, "//div/button[@type='submit']", by=XPATH).click()

    # wait for the page to load
    time.sleep(5)
    print("login complete")

def scrape_followers(driver, account):
    # load account page
    driver.get("https://www.instagram.com/{0}/".format(account))

    # click followers link
    waiter.find_element(driver, "//a[@href='/{}/followers/']".format(account), by=XPATH).click()

    # wait for followers modal to load
    waiter.find_element(driver, "//div[@role='dialog']", by=XPATH)

    # keep scrolling in a loop until you've hit the desired number of followers
    follower_css = "ul div li:nth-child({}) a.notranslate"  # Taking advange of CSS's nth-child functionality
    for group in itertools.count(start=1, step=12):
        for follower_index in range(group, group + 12):
            yield waiter.find_element(driver, follower_css.format(follower_index)).text

        # instagram loads followers 12 at a time. find the last follower element
        # and scroll it into view, forcing instagram to load another 12. second check
        # here in case element has gone stale
        last_follower = waiter.find_element(driver, follower_css.format(follower_index))
        driver.execute_script("arguments[0].scrollIntoView();", last_follower)

def scrape_following(driver, account):
    # load account page
    driver.get("https://www.instagram.com/{0}/".format(account))

    # click following link
    waiter.find_element(driver, "//a[@href='/{}/following/']".format(account), by=XPATH).click()

    # wait for the following modal to load
    waiter.find_element(driver, "//div[@role='dialog']", by=XPATH)

    # keep scrolling in a loop until you've hit the desired number of following
    follower_css = "ul div li:nth-child({}) a.notranslate"  # Taking advange of CSS's nth-child functionality
    for group in itertools.count(start=1, step=12):
        for follower_index in range(group, group + 12):
            yield waiter.find_element(driver, follower_css.format(follower_index)).text

        # instagram loads following 12 at a time. find the last following element
        # and scroll it into view, forcing instagram to load another 12. second check
        # here in case element has gone stale
        last_follower = waiter.find_element(driver, follower_css.format(follower_index))
        driver.execute_script("arguments[0].scrollIntoView();", last_follower)


if __name__ == "__main__":
    # read in user variables
    username, password, driver_path = read_keys()

    # details on account of interest
    account = '' # <account of interest here>
    num_followers = 1; # <account number followers here>
    num_following = 1; # <account number following here>

    # create web driver
    driver = webdriver.Chrome(executable_path=driver_path)

    try:
        login(driver, username, password)
        print("account: ", account)

        # get followers for the account
        print("followers:")
        for count, follower in enumerate(scrape_followers(driver, account=account), 1):
            print("\t{:>3}: {}".format(count, follower))
            if count >= num_followers:
                break

        # get following for the account
        print("following:")
        for count, following in enumerate(scrape_following(driver, account=account), 1):
            print("\t{:>3}: {}".format(count, following))
            if count >= num_following:
                break

    finally:
        driver.quit()
