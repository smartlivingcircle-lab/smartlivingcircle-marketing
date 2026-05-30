#!/usr/bin/env python3
"""
Telegram Marketing Bot
Posts DeFi content to Telegram groups/channels
"""

import os
import sys
import json
import random
import traceback
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from marketing_engine import format_for_telegram, get_unposted_content, mark_posted, hash_content, PAYHIP_LINK, CONTENT_POOL

# Telegram bot token - get from @BotFather
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')

# Target chat IDs (group or channel)
# Can be @username (for public groups) or numeric ID (for private)
TELEGRAM_TARGETS = [
    # Example: '@defi_community' or -1001234567890 for private groups
]

def send_telegram_message(bot_token, chat_id, text, disable_web_page_preview=False):
    """Send a message via Telegram Bot API using python-telegram-bot"""
    try:
        import telegram
        bot = telegram.Bot(token=bot_token)
        message = bot.send_message(
            chat_id=chat_id,
            text=text,
            disable_web_page_preview=disable_web_page_preview,
            parse_mode='HTML'
        )
        print(f"Sent to {chat_id}: {message.message_id}")
        return message.message_id
    except Exception as e:
        print(f"Telegram error: {e}")
        return None

def send_to_all_targets(text):
    """Send message to all configured Telegram targets"""
    if not TELEGRAM_BOT_TOKEN:
        print("No Telegram bot token configured")
        return []
    
    results = []
    for target in TELEGRAM_TARGETS:
        msg_id = send_telegram_message(TELEGRAM_BOT_TOKEN, target, text)
        results.append(msg_id)
    return results

def search_and_post_to_groups():
    """Search for DeFi Telegram groups and post"""
    # Note: Telegram Bot API can search for messages but not discover groups automatically
    # This would require manual group discovery or using a group database
    
    # For now, post to pre-configured targets
    pass

def create_group_post():
    """Create a group post for Telegram (shorter, punchier)"""
    # Pick a post
    post = get_unposted_content('telegram')
    
    # Format for Telegram (shorter, more punchy)
    text = format_for_telegram(post)
    
    # Add some emoji and formatting
    telegram_text = f"🔵 **{post['title']}**\n\n{post['body'][:400]}\n\n👉 {PAYHIP_LINK}"
    
    return telegram_text, post

def run_telegram_campaign():
    """Main Telegram campaign runner"""
    print("=" * 50)
    print("Telegram Marketing Campaign Starting")
    print("=" * 50)
    
    if not TELEGRAM_BOT_TOKEN:
        print("TELEGRAM_BOT_TOKEN not set. Skipping Telegram.")
        print("To set up:")
        print("1. Message @BotFather on Telegram")
        print("2. Create bot with /newbot")
        print("3. Copy the token and add to config")
        return
    
    if not TELEGRAM_TARGETS:
        print("No TELEGRAM_TARGETS configured. Skipping Telegram.")
        print("Add group/channel usernames or IDs to the TELEGRAM_TARGETS list.")
        return
    
    # Create and send post
    text, post = create_group_post()
    
    try:
        results = send_to_all_targets(text)
        if any(r for r in results):
            mark_posted('telegram', hash_content(post['title']))
            print(f"Telegram campaign complete. Sent to {len([r for r in results if r])} targets.")
        else:
            print("Telegram campaign completed but no messages sent (check targets).")
    except Exception as e:
        print(f"Telegram campaign error: {e}")

if __name__ == "__main__":
    run_telegram_campaign()