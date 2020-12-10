from explicit import waiter, XPATH
from selenium import webdriver

import itertools
import time
import json
import sys
import cmd

def diff(first, second):
    return [item for item in first if item not in second]

# pull user vars from keys.json
def read_keys():
    with open('keys.json') as file:
      keys = json.load(file)

    username = keys["username"]
    password = keys["password"]
    driver_path = keys["driver_path"]

    return username, password, driver_path

# log in to instagram
def login(driver, username, password):
    # load page
    driver.get("https://www.instagram.com/accounts/login/")

    # login
    waiter.find_write(driver, "//div/label/input[@name='username']", username, by=XPATH)
    waiter.find_write(driver, "//div/label/input[@name='password']", password, by=XPATH)
    waiter.find_element(driver, "//div/button[@type='submit']", by=XPATH).click()

    # wait for the page to load. increase from 5 if internet is slow
    time.sleep(5)
    print("login complete.\n")

# scrape followers modal
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

# scrape following modal
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
    # read in account of interest details
    account = str(input("account name: "))
    num_followers = int(input("account num followers: "))
    num_following = int(input("account num following: "))

    # read in user variables
    username, password, driver_path = read_keys()

    # create web driver
    driver = webdriver.Chrome(executable_path=driver_path)

    # scraping
    try:
        login(driver, username, password)
        print("account: ", account, "\n")

        # get followers for the account
        followers_list = []
        print("scraping followers...\n")
        for count, follower in enumerate(scrape_followers(driver, account=account), 1):
            followers_list.append(follower)
            if count >= num_followers:
                break

        # get following for the account
        following_list = []
        print("scraping following...\n")
        for count, following in enumerate(scrape_following(driver, account=account), 1):
            following_list.append(following)
            if count >= num_following:
                break
    finally:
        driver.quit()

    ## ANALYTICS
    print("analyzing activity for {}...\n".format(account))

    print("1. followers:", len(followers_list), "\n")
    print("2. following:", len(following_list), "\n")

    # check for people account doesn't follow back
    nope = diff(set(followers_list), set(following_list))
    print("3. {} not following back:".format(account), len(nope))
    # for n in nope: print(n) # comment/uncomment to print list

    # check for people who don't follow back
    rude = diff(set(following_list), set(followers_list))
    print("\n4. not following {} back:".format(account), len(rude))
    for r in rude: print(r) # comment/uncomment to print list

    # check for people who unfollowed recently (since last cache)
    with open("followers_cache.txt") as f:
        cache = f.read().splitlines()

    if len(cache) == 0: # first time running? cache is empty
        print("\n5. you have no cache. can't provide recent unfollowers.\n")
    else:
        unfollowers = diff(set(cache), set(followers_list))
        print("\n5. unfollowers since last cache:", len(unfollowers))
        # for u in unfollowers: print(u) # comment/uncomment to print list

    # copy followers_list into followers_cache.txt?
    answer = str(input("would you like to cache this data? y/n: "))

    if answer == "y": # copy into cache
        print("copying into cache...")
        with open('followers_cache.txt', 'w') as f:
            for item in followers_list:
                f.write("%s\n" % item)
        print("data copied to cache. see you later!")
    else:
        print("you said no, see you later!")
