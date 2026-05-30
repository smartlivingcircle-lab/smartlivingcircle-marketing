#!/usr/bin/env python3
"""
Discord Marketing Bot
Posts DeFi content to Discord servers via webhooks
"""

import os
import sys
import json
import requests
import random
import traceback
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from marketing_engine import format_for_discord, get_unposted_content, mark_posted, hash_content, PAYHIP_LINK, CONTENT_POOL

# Discord webhook URLs (one per server)
# These are placeholder - replace with actual webhook URLs
DISCORD_WEBHOOKS = [
    # Add your Discord webhook URLs here
    # Example: "https://discord.com/api/webhooks/123456/abcdef"
]

DISCORD_EMBED_COLOR = 5814783  # A nice blue-green color

def post_to_discord_webhook(webhook_url, title, description):
    """Post an embed message to a Discord webhook"""
    if not webhook_url or "your-webhook" in webhook_url:
        return None
        
    data = {
        "embeds": [{
            "title": title,
            "description": description,
            "color": DISCORD_EMBED_COLOR,
            "url": PAYHIP_LINK,
            "footer": {
                "text": "SmartLivingCircle | DeFi Education"
            },
            "timestamp": datetime.utcnow().isoformat(),
            "fields": [
                {
                    "name": "Get the Full Guide",
                    "value": f"[118-page DeFi ebook - Click Here]({PAYHIP_LINK})",
                    "inline": True
                }
            ]
        }]
    }
    
    try:
        response = requests.post(
            webhook_url,
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 204:
            print(f"Posted to Discord webhook: {title[:50]}...")
            return True
        else:
            print(f"Discord API error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Error posting to Discord: {e}")
        return False

def post_to_all_webhooks(title, description):
    """Post the same message to all configured webhooks"""
    results = []
    for webhook in DISCORD_WEBHOOKS:
        if webhook and "your-webhook" not in webhook:
            result = post_to_discord_webhook(webhook, title, description)
            results.append(result)
    return results

def create_weekly_digest_content():
    """Create a digest post combining multiple content pieces"""
    # Pick 3 random posts
    selected = random.sample(CONTENT_POOL, min(3, len(CONTENT_POOL)))
    
    body = "Here are this week's DeFi insights:\n\n"
    
    for i, post in enumerate(selected, 1):
        body += f"**{i}. {post['title']}**\n"
        # Short summary only
        summary = post['body'][:150] + "..."
        body += f"{summary}\n\n"
    
    body += f"\n**Get ALL the details:** {PAYHIP_LINK}"
    return body

def run_discord_campaign():
    """Main Discord campaign runner"""
    print("=" * 50)
    print("Discord Marketing Campaign Starting")
    print("=" * 50)
    
    if not DISCORD_WEBHOOKS or all("your-webhook" in w for w in DISCORD_WEBHOOKS):
        print("No Discord webhooks configured. Skipping Discord.")
        print("To set up: Add webhook URLs to DISCORD_WEBHOOKS list")
        return
    
    # Pick random content
    post = get_unposted_content('discord')
    title = post['title']
    description = format_for_discord(post)
    
    # Post
    results = post_to_all_webhooks(title, description)
    if any(results):
        mark_posted('discord', hash_content(post['title']))
    
    # Also send weekly digest (less frequently)
    # Only if it's the first post of the day or random chance
    if random.random() < 0.2:  # 20% chance
        digest = create_weekly_digest_content()
        post_to_all_webhooks("Weekly DeFi Digest", digest)
    
    print("Discord campaign complete")

if __name__ == "__main__":
    run_discord_campaign()