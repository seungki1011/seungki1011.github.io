import praw
import os

# Reddit API authentication debugging - 1
# print(os.environ['REDDIT_CLIENT_ID'])
# print(os.environ['REDDIT_CLIENT_SECRET'])
# print(os.environ['REDDIT_USER_AGENT'])

reddit = praw.Reddit(
    client_id=os.environ['REDDIT_CLIENT_ID'],
    client_secret=os.environ['REDDIT_CLIENT_SECRET'],
    user_agent=os.environ['REDDIT_USER_AGENT']
)

# Initialize the Reddit API client
# reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
#                      client_secret=REDDIT_CLIENT_SECRET,
#                      user_agent=REDDIT_USER_AGENT)


# Attempt to fetch top posts from the past 24 hours in the ArtificialInteligence subreddit
subreddit = reddit.subreddit('ArtificialInteligence')
       
try:
    # Use the time_filter parameter to get top posts from the past week
    top_posts = subreddit.top(time_filter='week', limit=20)  # Fetch top 20 posts from the past week

    news_posts = []  # Initialize a list to store news posts
    news_posts_count = 0  # Initialize a counter for news posts

    for post in top_posts:
        # Check if the post has a "News" flair
        if post.link_flair_text == "News":
            news_posts.append(post)
            news_posts_count += 1

            # Break if we have found the top 5 news posts or if we reach the end of the top posts
            if news_posts_count >= 5 or len(news_posts) >= 20:
                break

    for post in news_posts:
        print(f'Title: {post.title}')
        print(f"Content: {post.selftext}")
        print(f'URL: {post.url}')
        print('-----')
        
except praw.exceptions.PRAWException as e:
    print(f"Error: {e}")






