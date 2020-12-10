# instagram-activity
Web scraping & scripting to analyze instagram follower/following activity. See [here](docs.md) for implementation docs.

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
account name: # enter account username
account num followers: # enter account number of followers
account num following: # enter account number of following
```

##### Wiping the cache
This script can "cache" a list of followers, to track activity over time. To wipe the cache, delete the contents of `followers_cache.txt`. For more on the cache, see [here](docs.md#the-cache).

### Analytics
- followers that account of interest doesn't follow back
- accounts that don't follow account of interest back
- unfollower since last cache

### Dependencies
Running with
- ChromeDriver 87.0.4280.88 for Mac
- explicit 0.1.3

Note: scraping designed as of Dec 2020. May not work on later versions of instagram.com
