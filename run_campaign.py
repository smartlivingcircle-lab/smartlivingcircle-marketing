#!/usr/bin/env python3
"""
SmartLivingCircle - Full Marketing Campaign Runner
Runs all platforms in sequence
"""

import os
import sys
import random
from datetime import datetime

# Ensure project root in path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def run_reddit():
    client_id = os.environ.get('REDDIT_CLIENT_ID', '')
    if not client_id:
        log("Reddit: No credentials (network blocked) - skipping")
        return
    log("Starting Reddit campaign...")
    try:
        from reddit_poster import run_reddit_campaign
        run_reddit_campaign()
        log("Reddit campaign done")
    except Exception as e:
        log(f"Reddit error: {e}")

def run_discord():
    log("Starting Discord campaign...")
    try:
        from discord_poster import run_discord_campaign
        run_discord_campaign()
        log("Discord campaign done")
    except Exception as e:
        log(f"Discord error: {e}")

def run_telegram():
    log("Starting Telegram campaign...")
    try:
        from telegram_poster import run_telegram_campaign_sync
        run_telegram_campaign_sync()
        log("Telegram campaign done")
    except Exception as e:
        log(f"Telegram error: {e}")

def run_all():
    log("=" * 60)
    log("SMARTLIVINGCIRCLE MARKETING ENGINE - FULL RUN")
    log("=" * 60)
    
    # Random order to avoid pattern detection
    platforms = ['reddit', 'discord', 'telegram']
    random.shuffle(platforms)
    
    for platform in platforms:
        if platform == 'reddit':
            run_reddit()
        elif platform == 'discord':
            run_discord()
        elif platform == 'telegram':
            run_telegram()
    
    log("=" * 60)
    log("ALL CAMPAIGNS COMPLETE")
    log("=" * 60)

def run_single(platform):
    if platform == 'reddit':
        run_reddit()
    elif platform == 'discord':
        run_discord()
    elif platform == 'telegram':
        run_telegram()
    else:
        log(f"Unknown platform: {platform}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_single(sys.argv[1])
    else:
        run_all()