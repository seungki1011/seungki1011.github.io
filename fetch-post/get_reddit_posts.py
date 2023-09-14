import praw
import os

# Reddit API authentication debugging - 1
print(os.environ['REDDIT_CLIENT_ID'])
print(os.environ['REDDIT_CLIENT_SECRET'])
print(os.environ['REDDIT_USER_AGENT'])

# Reddit API authentication debugging - 2
reddit = praw.Reddit(
    client_id=os.environ['REDDIT_CLIENT_ID'],
    client_secret=os.environ['REDDIT_CLIENT_SECRET'],
    user_agent=os.environ['REDDIT_USER_AGENT']
)

# Initialize the Reddit API client
# reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
#                      client_secret=REDDIT_CLIENT_SECRET,
#                      user_agent=REDDIT_USER_AGENT)


# Attempt to fetch top posts from the past 24 hours in the MachineLearning subreddit
subreddit = reddit.subreddit('MachineLearning')
try:
    # Use the time_filter parameter to get top posts from the past 24 hours
    top_posts = subreddit.top(time_filter='day', limit=5)
    
    for post in top_posts:
        print(f'Title: {post.title}')
        print(f'URL: {post.url}')
        print('-----')
except praw.exceptions.PRAWException as e:
    print(f"Error: {e}")