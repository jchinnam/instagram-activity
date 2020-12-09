#!/usr/bin/python
# analyze instagram follower/following lists
# must copy/paste follower/following module content into respective text files

def diff(first, second):
    return [item for item in first if item not in second]

# read in text files
with open("followers.txt") as f:
    followers = f.readlines()

with open("following.txt") as f:
    following = f.readlines()

with open("followers_cache.txt") as f:
    older = f.readlines()

# extract "profile pictures" lines and substring for usernames
sub = "profile picture"
followers = [s[:-19] for s in followers if sub in s]
following = [s[:-19] for s in following if sub in s]
older = [s[:-19] for s in older if sub in s]

print("analyzing followers...\n")

print("1. followers:", len(followers), "\n")
print("2. following:", len(following), "\n")

# check for people who don't follow me back
rude = diff(set(following), set(followers))
print("3. not following back:", len(rude))
for r in rude: print(r)

# check for people unfollowed me
unfollowers = diff(set(older), set(followers))
print("\n4. recently unfollowed:", len(unfollowers))
for u in unfollowers: print(u)
