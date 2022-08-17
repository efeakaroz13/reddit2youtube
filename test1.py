#Copyright (c) 2022 Efe Akaröz
#Test file for downloading reddit videos
from secret import Secret
import requests
import praw
import pprint
import json 


mysecret = Secret()
clientid = mysecret.clientid
secretkey = mysecret.secret


reddit = praw.Reddit(client_id =clientid,
                     client_secret =secretkey,
                     user_agent ='Linux Android')


subreddit = reddit.subreddit('sekulermilliyetciturk')
out = []
for r in subreddit.hot(limit=50):
	if r.is_video == True:
		#print(r.title)
		out.append(r)

#	print(json.dumps(json.loads(str(vars(r))),indent=4))
#	break

print(len(out))
for o in out:
	print(o.title)
