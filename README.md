# instagram-activity
Web scraping & scripting to analyze instagram follower/following activity. See [here](docs.md) for implementation docs.

Updated as of Nov 2021. May not work on later versions of instagram.com. May not work on accounts with very large followings, due to Instagram limitations on rendering the lists.

### Setup
```bash
$ git clone <repo>
$ cd instagram-activity/
$ pip install explicit # install explicit
```

##### Setting user vars
Login credentials are necessary for scraping Instagram. `username` & `password` below should be to an account that does not require two-factor authentication. In `/keys.json`, set
- `username` to ***your*** username for login
- `password` to ***your*** password for login
- `driver_path` to path to your chromedriver

### Usage
```bash
$ python activity.py
target account name: # enter account username
mode? choose one: manual / scrape: # enter "manual" or "scrape"
account num followers: # enter account number of followers
account num following: # enter account number of following
```

##### Wiping the cache
This script can "cache" a list of followers, to track activity over time. To "wipe the cache", delete the contents of `followers_cache.txt`. For more on the cache, see [here](docs.md#the-cache).

### Analytics
- followers that account of interest doesn't follow back
- accounts that don't follow account of interest back
- unfollower since last cache

### Dependencies
Running with
- ChromeDriver 95.0.4638.69 for Mac, downloads [here](https://chromedriver.chromium.org/downloads)
- explicit 0.1.3
