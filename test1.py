#Copyright (c) 2022 Efe Akaröz
#Test file for downloading reddit videos
from secret import Secret
import requests
import praw
import re
import pprint
import json 
from RedDownloader import RedDownloader
import random
import time
import os
from colorama import Style,Fore




mystringchecker = ["a","Q","T","t","I","P","K"]
mysecret = Secret()
clientid = mysecret.clientid
secretkey = mysecret.secret

subredditname = input("Enter A Subreddit:")


reddit = praw.Reddit(client_id =clientid,
                     client_secret =secretkey,
                     user_agent ='Linux Android')


subreddit = reddit.subreddit(subredditname)
howmanyposts = int(input("Select how many posts you want to scrape:"))
out = []
for r in subreddit.hot(limit=howmanyposts):
	#print(r)
	if r.is_video == True:
		#print(r.title)
		out.append(r)

#	print(json.dumps(json.loads(str(vars(r))),indent=4))
#	break
try:
	outjson = json.loads(open("databackup.json","r").read())
except:

	outjson = {"data":[]}
print(len(out))
for o in out:
	try:
		duration = int(str(vars(o)).split("'duration':")[1].split(",")[0].strip())
		print("INFO | VIDEO DURATION IS {} SECONDS".format(duration))
		if duration < 300:
			gonnascrape = 1
			for d in outjson:
				try:
					redditurl = outjson[d]["reddit"]
					if redditurl == o.url:
						gonnascrape = 0
						break
					else:
						pass

				except:
					pass
			if gonnascrape == 1:
				print("INFO | FETCHING {}".format(o.title))
				filename =f"{random.choice(out)}{random.randint(1,100000)}"

				fileout = RedDownloader.Download(url = "https://www.reddit.com"+o.permalink, output=filename, quality = 720)
				videotitlefinal = str(re.sub(r"[^a-zA-Z0-9 ]", "",str(o.title))).replace("ş","s").replace("Ş","S").replace("ğ","g").replace("Ğ","G").replace("ö","o").replace("Ö","o").replace("arap","Ar*p").replace("Arap","Ar*p").replace("Ü","U").replace("ü","u").replace("Ç","C").replace("ç","c")[:30]
				os.system(f"python3 ytuploadtests.py --file '{filename}.mp4' --title '{videotitlefinal} | Kentel Automation' --privacyStatus 'public' --keywords 'allah,din,peygamber,god,jesus,explore,keşfet,akp,chp,popular,reddit'")
				outjson["data"].append({"filename":filename,"title":o.title,"downloaded":time.ctime(time.time()),"uploaded":time.time(),"reddit":o.url})
				print("https://www.reddit.com"+o.permalink)
				print("DONE | FETCH COMPLETE")
			else:
				print(Fore.YELLOW,"WARNING",Fore.RESET,f"| '{o.title}' Video already exists. Passing")
	except Exception as e:
		print(e)

with open("databackup.json","w") as myfile:
	myfile.write(json.dumps(outjson,indent=4))

