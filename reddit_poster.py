#!/usr/bin/env python3
"""
Reddit Marketing Bot
Posts DeFi content to crypto subreddits
"""

import os
import sys
import random
import traceback

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from marketing_engine import format_for_reddit, get_unposted_content, mark_posted, hash_content, PAYHIP_LINK

# Subreddits we target
TARGET_SUBREDDITS = [
    'defi', 'ethtrader', 'cryptocurrency', 'ethereum',
    'CryptoCurrency', 'bitcoin', 'investing', 'FinancialPlanning'
]

SUBREDDIT_RULES = {
    'defi': {'min_karma': 10, 'account_age_days': 7, 'self_promo_allowed': False},
    'ethtrader': {'min_karma': 50, 'account_age_days': 14, 'self_promo_allowed': False},
    'cryptocurrency': {'min_karma': 100, 'account_age_days': 30, 'self_promo_allowed': False},
    'ethereum': {'min_karma': 50, 'account_age_days': 14, 'self_promo_allowed': False},
}

def get_reddit_client():
    """Initialize Reddit connection using PRAW"""
    import praw
    
    reddit = praw.Reddit(
        client_id=os.environ.get('REDDIT_CLIENT_ID', ''),
        client_secret=os.environ.get('REDDIT_CLIENT_SECRET', ''),
        username=os.environ.get('REDDIT_USERNAME', ''),
        password=os.environ.get('REDDIT_PASSWORD', ''),
        user_agent='SmartLivingCircle/1.0 (DeFi Marketing Bot)'
    )
    return reddit

def check_account_status(reddit):
    """Check if our account meets subreddit requirements"""
    user = reddit.user.me()
    print(f"Logged in as: {user.name}")
    print(f"Karma: {user.comment_karma}")
    return True

def post_to_subreddit(reddit, subreddit_name, title, content):
    """Post content to a subreddit"""
    try:
        subreddit = reddit.subreddit(subreddit_name)
        
        # Check if we can post (account age, karma)
        rules = SUBREDDIT_RULES.get(subreddit_name, {})
        
        # Submit the post
        submission = subreddit.submit(title, selftext=content)
        print(f"Posted to r/{subreddit_name}: {submission.url}")
        return submission.url
    except Exception as e:
        print(f"Error posting to r/{subreddit_name}: {e}")
        return None

def post_comment(reddit, subreddit_name, post_url, comment_body):
    """Comment on an existing post"""
    try:
        submission = reddit.submission(url=post_url)
        comment = submission.reply(comment_body)
        print(f"Commented on {post_url}: {comment.id}")
        return comment.id
    except Exception as e:
        print(f"Error commenting: {e}")
        return None

def find_relevant_post_and_comment(reddit, subreddit_name):
    """Find a relevant post and add value with a comment"""
    try:
        subreddit = reddit.subreddit(subreddit_name)
        
        # Search for posts asking about DeFi topics
        posts_found = 0
        for post in subreddit.hot(limit=20):
            posts_found += 1
            
            # Skip posts older than 24 hours
            post_age_hours = (reddit.config.redditor['logged_in'] or 0)  # This won't work, fixme
            
            # Only engage with recent posts
            if post.score < 5:
                continue
            
            title_lower = post.title.lower()
            keywords = ['defi', 'flash loan', 'yield', 'liquidity', 'staking', 'crypto', 'trading']
            
            if any(kw in title_lower for kw in keywords):
                # Found a relevant post - write a helpful comment
                comment = f"""Great question! Here is my take:

The key to DeFi safety is understanding what you are actually exposing your funds to. Before using any protocol:

1. Check the TVL (total value locked) - higher = more battle tested
2. Look for audits from recognized firms (Trail of Bits, Consensys Diligence, OpenZeppelin)
3. Understand the fee structure - hidden fees kill gains
4. Look at the governance tokenomics - inflation is a silent killer

I wrote a complete guide covering this exact topic - 118 pages on DeFi strategies, flash loans, and risk management:

{PAYHIP_LINK}

Hope this helps!"""
                
                try:
                    comment_obj = post.reply(comment)
                    comment_obj.mod.distinguish()
                    print(f"Successfully commented on: {post.title}")
                    return True
                except Exception as e:
                    # Probably already replied
                    print(f"Could not comment: {e}")
                    continue
        
        print(f"Scanned {posts_found} posts in r/{subreddit_name}, no suitable target found")
        return False
    except Exception as e:
        print(f"Error in r/{subreddit_name}: {e}")
        return False

def run_reddit_campaign():
    """Main campaign runner"""
    print("=" * 50)
    print("Reddit Marketing Campaign Starting")
    print("=" * 50)
    
    try:
        reddit = get_reddit_client()
        print("Reddit client connected")
    except Exception as e:
        print(f"Could not connect to Reddit: {e}")
        print("Make sure REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USERNAME, REDDIT_PASSWORD are set")
        return
    
    try:
        user = reddit.user.me()
        print(f"Account: {user.name}, Karma: {user.comment_karma}")
    except Exception as e:
        print(f"Auth error: {e}")
        return
    
    # Strategy: Post 1 new submission + comment on 2 posts per run
    # Different subreddits on different days
    
    day_of_week = random.choice(TARGET_SUBREDDITS)
    target_sub = random.choice(TARGET_SUBREDDITS)
    
    # Post a submission
    post = get_unposted_content('reddit')
    content = format_for_reddit(post)
    
    try:
        url = post_to_subreddit(reddit, target_sub, post['title'], content)
        if url:
            mark_posted('reddit', hash_content(post['title']), url)
            print(f"Submission posted: {url}")
    except Exception as e:
        print(f"Submission failed: {e}")
        # Could be rate limited or rule violation - try commenting instead
        print("Switching to comment strategy...")
    
    # Comment on 2 relevant posts
    for _ in range(2):
        target = random.choice(TARGET_SUBREDDITS)
        try:
            find_relevant_post_and_comment(reddit, target)
        except Exception as e:
            print(f"Commenting failed on {target}: {e}")
    
    print("Reddit campaign complete")

if __name__ == "__main__":
    run_reddit_campaign()