# documentation

#### scraping

##### login
Instagram requires a user to be logged in to view an account profile. Therefore first, we have to input our login credentials and wait for the page to load. Rather than identify a specific element on the loaded page after login completion, we just wait a few seconds:
```python
time.sleep(5)
```
This time can be increased to accommodate slower connections.

##### modals
The followers and following lists are modals on the account profile. Once opened they will start to display accounts but if you scroll straight to the bottom, it will stop and give a link to suggestions. Instead, if you fiddle with the modal by scrolling up and down, you can force it to load additional followers for that account, 12 at a time. Therefore, we need to scroll in a loop until we reach the total number of follower/following accounts:
```python
follower_css = "ul div li:nth-child({}) a.notranslate"
  for group in itertools.count(start=1, step=12):
      for follower_index in range(group, group + 12):
          yield waiter.find_element(driver, follower_css.format(follower_index)).text
```

#### the cache
In order to track activity over time (i.e. who has unfollowed an account recently), we need to "cache" some data to compare against. The script achieves this by copying the retrieved list of followers to `followers_cache.txt` at the end of a run here:
```python
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
```

As shown above, during execution, the script prompts the user whether or not they would like to cache the followers from that run as follows:
```bash
would you like to cache this data? y/n:
```
Based on their input (y/n), it will either overwrite the contents of `followers_cache.txt` with the followers list from that run, or do nothing, respectively.

Note: to produce expected results, the contents of the cache have to belong to the ***same*** account as the account of interest in the current run.
