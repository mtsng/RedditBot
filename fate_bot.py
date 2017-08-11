#This bot is based on the tutorial by shantnu
#Check out his tutorial at: pythonforengineers.com/build-a-reddit-bot-part-1


import praw
import pdb
import os
import re
import datetime
import time

def calTimeDiff(post_date):
	time_now = datetime.datetime.utcnow()
	tdelta = time_now - post_date

	return tdelta.total_seconds()

def timestampToUTC(timestamp):
	
	return datetime.datetime.utcfromtimestamp(timestamp)


def checkFlairReply(flair_check_timer, timestamp):
	post_date = timestampToUTC(timestamp)
	time_diff = calTimeDiff(post_date)

	if time_diff >= flair_check_timer:
		
def checkForFlair(submission):		



#Main Function
def main():
	bot = 'bot1'
	subredname = "grandorder"
	post_limit = 5
	time_limit = 900 #15 min
	message = "Please Flair"
	flair_check_timer = 1800 #30 min

	reddit = praw.Reddit(bot)

	if not os.path.isfile("posts_replied_to.txt"):
		posts_replied_to = []

	else:
		with open("posts_replied_to.txt", "r") as f:
			posts_replied_to = f.read()
			posts_replied_to = posts_replied_to.split("\n")
			posts_replied_to = list(filter(None, posts_replied_to))

	subreddit = reddit.subreddit(subredname)
	
	for submission in subreddit.new(limit=post_limit):
		post_date = timestampToUTC(submission.created_utc)
		time_diff = calTimeDiff(post_date)

		if submission.id not in posts_replied_to:
			if (time_diff >= time_limit and submission.link_flair_text is None):
				submission.reply(message)

				posts_replied_to.append(submission.id)
	
	with open("posts_replied_to.txt", "w") as f:
		for post_id in posts_replied_to:
			f.write(post_id + "\n")

main()	
