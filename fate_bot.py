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

def timeNow():
	
	return datetime.datetime.utcnow()

def timestampToUTC(timestamp):
	
	return datetime.datetime.utcfromtimestamp(timestamp)


def checkFlairReply(submission, posts_flaired, flair_check_timer):
	post_time = timestampToUTC(submission.created_utc)
	time_diff = calTimeDiff(post_time)

	if (time_diff >= flair_check_timer and submssion.link_flair_text is None):
		for comment in submission.comments.list():
			if comment.author == submission.author and re.search("[^", comment.body):
				flair = comment.body
				print(flair[1:])
				#submission.mod.flair(text=flair, css_class='bot')
					
		
def checkForFlair(submission, posts_replied_to, message, time_limit):		
	post_time = timestampToUTC(submission.created_utc)
	time_diff = calTimeDiff(post_time)
	
	if submission.id not in posts_replied_to:
		if(time_diff >= time_limit and submission.link_flair_text is None):
			submission.reply(message)

			posts_replied_to.append(submission.id)


#Main Function
def main():
	bot = 'bot1'
	subredditname = "grandorder"
	post_limit = 5
	time_limit = 120
	message = "Please Flair"
	flair_check_timer = 300
	interval_start = timeNow()

	reddit = praw.Reddit(bot)

	if not os.path.isfile("posts_replied_to.txt"):
		posts_replied_to = []

	else:
		with open("posts_replied_to.txt", "r") as f:
			posts_replied_to = f.read()
			posts_replied_to = posts_replied_to.split("\n")
			posts_replied_to = list(filter(None, posts_replied_to))

	if not os.path.isfile("posts_flaired.txt"):
		posts_flaired = []
	else:
		with open("posts_flaired.txt", "r") as f:
			posts_flaired = f.read()
			posts_flaired = posts_flaired.split("\n")
			posts_flaired = list(filter(None, posts_flaired))


	subreddit = reddit.subreddit(subredditname)
	
	for submission in subreddit.new(limit=post_limit):
		checkForFlair(submssion, posts_replied_to, message, time_limit)

	if calTimeDiff(interval_start) >= flair_check_timer:
		interval_start = timeNow()

		for post_id in posts_replied_to:
			missing_flair_post = reddit.submission(post_id)
			checkFlairReply(missing_flair_post, flair_check_timer)
	
	with open("posts_replied_to.txt", "w") as f:
		for post_id in posts_replied_to:
			f.write(post_id + "\n")

	with open("posts_flaired.txt", "w") as f:
		for post_id in posts_replied_to:
			f.write(post_id + "\n")

main()	
