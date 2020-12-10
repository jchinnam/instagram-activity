# instagram-activity
Web scraping & scripting to analyze instagram follower activity

### Setup
```bash
$ git clone <repo>
$ cd instagram-activity/
$ pip install explicit # install explicit
```

In `/keys.json`, set
- `username` to ***your*** username for login
- `password` to ***your*** password for login
- `driver_path` to your path to chromedriver

Note: login credentials are necessary for scraping Instagram. `username` & `password` above should be to an account that does not require two-factor authentication.

### Usage
```bash
$ python activity.py
account name: # enter account username
account num followers: # enter account number of followers
account num following: # enter account number of following
```

##### Wiping the cache
To wipe the cache, delete the contents of `followers_cache.txt`.

### Dependencies
Runs with
- ChromeDriver 87.0.4280.88 for Mac
- explicit 0.1.3

Note: scraping designed as of Dec 2020. May not work on later versions of instagram.com
