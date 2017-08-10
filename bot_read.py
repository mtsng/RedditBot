import praw

reddit = praw.Reddit('bot1')

subreddit = reddit.subreddit("grandorder")

for submission in subreddit.new(limit=5):
	print("Title: ", submission.title)
	print("Flair: ", submission.link_flair_text)
	print("Created: ", submission.created_utc)
