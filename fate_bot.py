#This bot is based on the tutorial by shantnu
#Check out his tutorial at: pythonforengineers.com/build-a-reddit-bot-part-1


import praw
import pdb
import os
import re
import datetime
import time

#finds the number of seconds that have past since posting
def calTimeDiff(post_time):
	time_now = datetime.datetime.utcnow()
	tdelta = time_now - post_time

	return tdelta.total_seconds()

#the utc time at the moment of function call
def timeNow():
	
	return datetime.datetime.utcnow()

#converted utc timestamp of post to utc datetime object
def timestampToUTC(timestamp):
	
	return datetime.datetime.utcfromtimestamp(timestamp)

#checks for flair comments from post author
def checkFlairReply(submission, posts_flaired, flair_check_timer):
	#time of the create of the post
	post_time = timestampToUTC(submission.created_utc)
	#the seconds since the creation of the post
	time_diff = calTimeDiff(post_time)

	#if user manually flairs post, add it the the posts_flaired list
	if submission.link_flair_text != None and submission.id not in posts_flaired:
		posts_flair.append(submission.id)

	#checks for proper post "age", a missing flair, and absence in the posts_flaired list	
	if (time_diff >= flair_check_timer and submission.link_flair_text is None and submission.id not in posts_flaired):
		#loops through the top level comments of the post
		for comment in submission.comments.list():
			#checks the comment to see if it has the same author as the post and if they have a potential flair
			if comment.author == submission.author and re.search("^\[.*\]$", comment.body):
				flair = comment.body
				print(flair[1:flair.len() - 1])
				posts_flaired.append(submission.id)
				#submission.mod.flair(text=flair, css_class='bot')
					

#checks to see if post is flaired and the age of the post; if the post is "old" enough and unflaired, the bot comments;		
def checkForFlair(submission, posts_replied_to, message, time_limit):		
	#time of the creation of the post
	post_time = timestampToUTC(submission.created_utc)
	#the number of seconds since the creation of the post
	time_diff = calTimeDiff(post_time)
	
	#if the post has not been visited and time and flair conditions are true, the bot comments and adds it to the visited list
	if submission.id not in posts_replied_to:
		if(time_diff >= time_limit and submission.link_flair_text is None):
			submission.reply(message)

			posts_replied_to.append(submission.id)


#Main Function
def main():
	bot = 'bot1'
	subredditname = "pythonforengineers"
	post_limit = 5 #number of posts to be checked at a time
	time_limit = 120 #time limit for unflaired post before bot comment
	message = "Please Flair" #Bot message
	flair_check_timer = 300 #the amount of time given for user to flair post after bot comment
#	interval_start = timeNow()

	#Do not change below here unless you know your stuff
	reddit = praw.Reddit(bot)
	subreddit = reddit.subreddit(subredditname)

	#creates/opens a text file that stores visited posts, so the bot does not span the post
	if not os.path.isfile("posts_replied_to.txt"):
		#if file does not exist, create a new list
		posts_replied_to = []

	else:
		#opens exisitng file and creates a list of content
		with open("posts_replied_to.txt", "r") as f:
			posts_replied_to = f.read()
			posts_replied_to = posts_replied_to.split("\n")
			posts_replied_to = list(filter(None, posts_replied_to))

	#creates/opens a text file that tracks flaired posts after bot comment; prevents excess work from bot
	if not os.path.isfile("posts_flaired.txt"):
		#if file does not exist, create a new list
		posts_flaired = []
	else:
		#opens existing file and creates a list of content
		with open("posts_flaired.txt", "r") as f:
			posts_flaired = f.read()
			posts_flaired = posts_flaired.split("\n")
			posts_flaired = list(filter(None, posts_flaired))
	
	#loops through the post_limit number of new posts
	for submission in subreddit.new(limit=post_limit):
		checkForFlair(submission, posts_replied_to, message, time_limit)

	#loops through the visited, unflair posts for flair comments
	for post_id in posts_replied_to:
		missing_flair_post = reddit.submission(post_id)
		checkFlairReply(missing_flair_post, posts_flaired, flair_check_timer)

#	if calTimeDiff(interval_start) >= flair_check_timer:
#		interval_start = timeNow()

#		for post_id in posts_replied_to:
#			missing_flair_post = reddit.submission(post_id)
#			checkFlairReply(missing_flair_post, posts_flaired, flair_check_timer)

	#writes the list back to the file	
	with open("posts_replied_to.txt", "w") as f:
		for post_id in posts_replied_to:
			f.write(post_id + "\n")
	#writes the list beck to the file
	with open("posts_flaired.txt", "w") as f:
		for post_id in posts_replied_to:
			f.write(post_id + "\n")

main()	
