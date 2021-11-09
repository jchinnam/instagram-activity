from explicit import waiter, XPATH
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import itertools
import time
import json
import sys
import cmd

# resources:
# https://www.geeksforgeeks.org/how-to-scroll-down-followers-popup-in-instagram/
# https://stackoverflow.com/questions/37233803/how-to-web-scrape-followers-from-instagram-web-browser

def diff(first, second):
    return [item for item in first if item not in second]


def read_keys():
    '''
    Reads user vars from keys.json.
    '''
    with open('keys.json') as file:
      keys = json.load(file)

    username = keys["username"]
    password = keys["password"]
    driver_path = keys["driver_path"]

    return username, password, driver_path


def login(driver, username, password):
    '''
    Logs into instagram.
    '''
    # load page
    driver.get("https://www.instagram.com/accounts/login/")

    # login
    waiter.find_write(driver, "//div/label/input[@name='username']", username, by=XPATH)
    waiter.find_write(driver, "//div/label/input[@name='password']", password, by=XPATH)
    waiter.find_element(driver, "//div/button[@type='submit']", by=XPATH).click()

    # wait for the page to load. increase from 5 if internet is slow
    time.sleep(5)
    print("login complete.\n")


def scrape(driver, account, type, max):
    '''
    Scrapes an instagram page follower or following modal.
    Parameters:
        driver: web driver
        account: instagram account of interest
        type: modal type (i.e. "follower" or "following")
        max: max count of followers/followed to scrape
    Returns:
        generator of users (either followers or followed)
    '''

    # load account page
    driver.get("https://www.instagram.com/{0}/".format(account))

    # grab modal
    driver.find_element_by_partial_link_text(type).click()
    followers_modal = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='isgrP']")))

    # scroll through list
    follower_index = 1
    follower_css = "ul div li:nth-child({}) a.notranslate"  # Taking advange of CSS's nth-child functionality
    while follower_index < num_followers:
        driver.execute_script(
            'arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',
          followers_modal)

        yield waiter.find_element(driver, follower_css.format(follower_index)).text
        follower_index += 1


def manual():
    '''
    Reads follower and following lists manually from text files.
    '''
    print("reading in followers.txt...\n")
    with open("followers.txt") as f:
        followers = f.readlines()

    print("reading in following.txt...\n")
    with open("following.txt") as f:
        following = f.readlines()

    # extract "profile pictures" lines and substring for usernames
    sub = "profile picture"
    followers = [s[:-19] for s in followers if sub in s]
    following = [s[:-19] for s in following if sub in s]

    return followers, following


if __name__ == "__main__":
    # read in account of interest details
    account = str(input("target account name: "))
    mode = str(input("mode? choose one: manual / scrape: "))

    # MODE: MANUAL
    if mode == "manual":
        followers_list, following_list = manual()

    # MODE: SCRAPE
    else:
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
            for count, follower in enumerate(scrape(driver, account, "follower", num_followers), 1):
                followers_list.append(follower)
                print(count)
                if count >= num_followers:
                    break

            # get following for the account
            following_list = []
            print("scraping following...\n")
            for count, following in enumerate(scrape(driver, account, "following", num_following), 1):
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
        for u in unfollowers: print(u) # comment/uncomment to print list

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
