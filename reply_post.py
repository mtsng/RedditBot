import praw
import pdb
import re
import os
import datetime, time

def convertthing(date):
	now = datetime.datetime.utcnow()
#	print(now)
#	print(date)
#	print((now - date).total_seconds())
	return (now - date).total_seconds()

#Create the Reddit instance
reddit = praw.Reddit('bot1')

if not os.path.isfile("posts_replied_to.txt"):
	posts_replied_to = []

else:
	#with opens the file, closes it, and handled errors
	with open("posts_replied_to.txt", "r") as f:
		posts_replied_to = f.read()
		posts_replied_to = posts_replied_to.split("\n")
		#filter empty values
		posts_replied_to = list(filter(None, posts_replied_to))


subreddit = reddit.subreddit("pythonforengineers")
for submission in subreddit.new(limit=1):
	
	d = datetime.datetime.utcfromtimestamp(submission.created_utc)
	t = convertthing(d)
	if submission.id not in posts_replied_to:
		if re.search("time test", submission.title, re.IGNORECASE) and t >= 600:
			submission.reply("10 Minutes or More have passed")

			print("Bot replying to: ", submission.title)
			print("Time:\n ")
			print(datetime.datetime.utcnow())
			print(datetime.datetime.utcfromtimestamp(int(submission.created_utc)))
			print(t)
			posts_replied_to.append(submission.id)
#	d = datetime.datetime.fromtimestamp(int(submission.created_utc))
#	print("Title: ", submission.title)
#	convertthing(d)

with open("posts_replied_to.txt", "w") as f:
	for post_id in posts_replied_to:
		f.write(post_id + "\n")
