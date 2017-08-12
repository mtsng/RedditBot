#This bot is based on the tutorial by shantnu
#Check out his tutorial at: pythonforengineers.com/build-a-reddit-bot-part-1
#Check out John Huttlinger too for his flair bot: github.com/JBHUTT09
#Check out bboe for his handling of the ratelimit: github.com/bboe 

import praw
import pdb
import os
import re
import datetime
import time
import sys

flairs = {'JP News': 's', 'JP Discussion': 's', 'JP PSA': 's', 'JP Spoliers': 's', 'NA News': 't', 'NA PSA': 't',
	'NA Spoliers': 't', 'News': 'd', 'Tips & Tricks': 'i', 'Fluff': 'b', 'Comic': 'b', 'Guide': 'i', 'PSA': 'k',
	'Rumor': 'c', 'WEEKLY RANT': 'j', 'Translated': 'f', 'Story Translation': 'i', 'Discussion': 'i',
	'Poll': 'i', 'Moderator': 'a', 'Maintenance': 'c', 'Stream': 'b', 'OC': 'b', 'New Post': 'b'}


#handle ratelimit issues by bboe
def handle_ratelimit(func, *args, **kwargs):
	while True:
		try:
			func(*args, **kwargs)
			break
		except praw.errors.RateLimitExceeded as error:
			print("\tSleeping for %d seconds" + error.sleep_time)
			tim.sleep(error.sleep_time)

#finds the number of seconds that have past since posting
def cal_time_diff(post_time):
	time_now = datetime.datetime.utcnow()
	tdelta = time_now - post_time

	return tdelta.total_seconds()

#returns the utc time at the moment of function call
def time_now():
	
	return datetime.datetime.utcnow()

#converted utc timestamp of post to utc datetime object
def timestamp_to_UTC(timestamp):
	
	return datetime.datetime.utcfromtimestamp(timestamp)

#checks for flair comments from post author
def check_flair_comments(submission, posts_flaired):

	#if user manually flairs post, add it the the posts_flaired list
	if submission.link_flair_text != None and submission.id not in posts_flaired:
		posts_flair.append(submission.id)

	print(submission.link_flair_text is None)
	print(submission.id not in posts_flaired)
	#checks for proper post "age", a missing flair, and absence in the posts_flaired list	
	if (submission.link_flair_text is None and submission.id not in posts_flaired):
		#loops through the top level comments of the post
		for top_level_comment in submission.comments.list():
			#checks the comment to see if it has the same author as the post and if they have a potential flair
			if top_level_comment.author == submission.author and re.search("^\[.*\]$", top_level_comment.body):
				flair_comment = top_level_comment.body
				flair = flair_comment[1:len(flair_comment) - 1]
				print(flair)
				
				#if the flair is valid, the post is flaired, otherwise inform the poster of an incorrect flair
				if(check_valid_flair(flair)):
					print("work")
					top_level_comment.reply("Post has been flaired: " + flair)
					posts_flaired.append(submission.id)
					submission.mod.flair(text=flair, css_class=flairs[flair])
				else:
					print("fail")
					top_level_comment.reply("Incorrect flair. Please flair manually.")

#return true if the flair is valid, otherwise false					
def check_valid_flair(flair):
	
	if flair in flairs:
		return True
	
	return False

#checks if the user already commented a flair and flairs the post for them
def check_preemptive_flair_comment(submission, posts_flaired):
	
	for top_level_comment in submission.comments.list():
		if top_level_comment.author == submission.author and re.search("^\[.*\]$", top_level_comment.body):
			flair_comment = top_level_comment.body
			flair = flair_comment[1:len(flair_comment) - 1]
			
			if(check_valid_flair(flair)):
				top_level_comment.reply("Post has been flaired: " + flair)
				posts_flaired.append(submission.id)
				submission.mod.flair(text=flair, css_class=flairs[flair])
				return True
			else:
				top_level_comment.reply("Incorrect flair. Please flair manually.")
	return False

#checks to see if post is flaired and the age of the post; if the post is "old" enough and unflaired, the bot comments;		
def check_for_flair(submission, posts_replied_to, message, time_limit, posts_flaired):		
	#time of the creation of the post
	post_time = timestamp_to_UTC(submission.created_utc)
	#the number of seconds since the creation of the post
	time_diff = cal_time_diff(post_time)
	
	#if the post has not been visited and time and flair conditions are true, the bot comments and adds it to the visited list
	if submission.id not in posts_replied_to:
		if(time_diff >= time_limit and submission.link_flair_text is None):
			if check_preemptive_flair_comment(submission, posts_flaired) == False:
				submission.reply(message)
				posts_replied_to.append(submission.id)




#Main Function
def main():
	bot = 'bot1'
	subreddit_name = "fgobottest"
	text_limit = 100
	start_pt_modifier = .25
	post_limit = 2 #number of posts to be checked at a time
	time_limit = 300 #time limit (in seconds) for unflaired post before bot comment
	message = "Please Flair" #Bot message

	#Do not change below here unless you know your stuff
	reddit = praw.Reddit(bot)
	subreddit = reddit.subreddit(subreddit_name)

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

	#if statements ensure that text file length do not get too large
	if len(posts_flaired) > text_limit:
		flaired_length = len(posts_flaired)
		start = start_pt_modifier * flaired_length
		end = flaired_length
		temp_flaired = posts_flair[start:end]
		posts_flaired = temp_flaired

	if len(posts_replied_to) > text_limit:
		replied_length = len(posts_replied_to)
		start = start_pt_modifier * replied_length
		end = replied_length
		temp_replied_to = posts_replied_to[start:end]
		posts_replied_to = temp_replied_to 

	#try-catch for connection errors with reddit
	try:
		#loops through the post_limit number of new posts
		for submission in subreddit.new(limit=post_limit):
			handle_ratelimit(check_for_flair, submission, posts_replied_to, message, time_limit, posts_flaired)
		
		#loops through the visited, unflaired posts for flair comments
		for post_id in posts_replied_to:
			missing_flair_post = reddit.submission(post_id)
			handle_ratelimit(check_flair_comments, missing_flair_post, posts_flaired)

	except Exception:
		sys.exc_clear()
	
	#writes the list back to the file	
	with open("posts_replied_to.txt", "w") as f:
		for post_id in posts_replied_to:
			f.write(post_id + "\n")
	#writes the list beck to the file
	with open("posts_flaired.txt", "w") as f:
		for post_id in posts_flaired:
			f.write(post_id + "\n")

main()	
