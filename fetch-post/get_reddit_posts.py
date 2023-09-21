import praw
import os
import datetime

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
    # news_posts_count = 0  # Initialize a counter for news posts

    for post in top_posts:
        # Check if the post has a "News" flair
        if post.link_flair_text == "News":
            news_posts.append(post)
            # news_posts_count += 1

            # Break if we have found the top 5 news posts or if we reach the end of the top posts
            if len(news_posts) >= 5 or len(news_posts) >= 20:
                break
    
    # Get the current date in the format 'YYYY-MM-DD'
    current_date = datetime.date.today().strftime("%Y-%m-%d")
    
    # Define the file path with the current date and the 'reddit-posts' folder
    file_path = os.path.join("/Users/seungkikim/Desktop/seungki1011.github.io/_news", f"{current_date}-reddit_news_posts.md")

    # Ensure the 'reddit-posts' folder exists; create it if not
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Front matter containing metadata
    front_matter = f"""---
    layout: post
    title: "Reddit News {current_date}"
    author: seungki
    categories: [Reddit]
    image: post_images/redditlogo.png
    toc: True
    ---
    """
    
    # Write the titles and content of the news posts to the text file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(front_matter)
        
        for i, post in enumerate(news_posts, start=1):
            file.write("---")
            file.write("\n")
            file.write(f"## [{i}] \"{post.title}\"\n")
            file.write(f"{post.selftext}\n\n")
            file.write(f"[URL of Post]({post.url})\n\n")
            
            print(f'Title: {post.title}')
            print(f"Content: {post.selftext}")
            print(f'URL: {post.url}')
            print('-----')
            
    print(f"News posts saved as '{current_date}-reddit_news_posts.md'")    
                
except praw.exceptions.PRAWException as e:
    print(f"Error: {e}")






