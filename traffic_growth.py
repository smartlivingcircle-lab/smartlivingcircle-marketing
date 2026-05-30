#!/usr/bin/env python3
"""
Traffic Growth Engine v2
Multi-platform content distribution + community discovery
Finds crypto audiences across platforms and drives them to funnel
"""

import os
import sys
import time
import random
import requests
from datetime import datetime

WORKDIR = "C:/Users/INSPIRON/smartlivingcircle-marketing"
sys.path.insert(0, WORKDIR)

PAYPIP_LINK = "https://payhip.com/b/1vtcL"
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1510211779924463748/kg-TcdfPw5e-dqCF7-9MuN6xZlReHsWZjoXKNwXn8UjChG7BBx3jvpEOBtoKPL6UHngC"
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '8889649869:***')
TELEGRAM_USER_ID = "6180735205"  # Marco's personal DM

from content_generator import get_random_education, get_content_for_platform, generate_thread_prompt

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M')}] {msg}")

# ============================================================
# DISCORD - Post pump alerts and content
# ============================================================
def post_to_discord(content, alert_type="update"):
    """Post to Discord channel"""
    colors = {"pump": 0xFF0000, "update": 0x00FF00, "education": 0x0099FF}
    
    data = {
        "embeds": [{
            "title": f"📊 SmartLivingCircle {alert_type.upper()}",
            "description": content,
            "color": colors.get(alert_type, 0x00FF00),
            "footer": {"text": f"Auto-generated • {datetime.now().strftime('%H:%M UTC')}"},
            "url": PAYPIP_LINK
        }]
    }
    
    r = requests.post(DISCORD_WEBHOOK, json=data, headers={"Content-Type": "application/json"}, timeout=10)
    return r.status_code == 204

# ============================================================
# TELEGRAM - Send to Marco's DM + any channel
# ============================================================
def send_telegram_message(chat_id, text, parse_mode="HTML"):
    """Send via Telegram Bot API"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    r = requests.post(url, json={"chat_id": chat_id, "text": text, "parse_mode": parse_mode}, timeout=10)
    return r.json()

def telegram_dm(content):
    """Send DM to Marco"""
    try:
        result = send_telegram_message(TELEGRAM_USER_ID, content)
        if result.get('ok'):
            log(f"Telegram DM: Sent OK")
        else:
            err = result.get('description', 'Unknown error')
            log(f"Telegram DM: Failed - {err}")
    except Exception as e:
        log(f"Telegram DM: Error - {e}")

# ============================================================
# CONTENT DISTRIBUTION - All platforms at once
# ============================================================
def run_content_campaign():
    """Post crypto content to ALL connected platforms"""
    log("=== TRAFFIC CAMPAIGN STARTING ===")
    
    # Generate fresh content
    content = get_random_education()
    short_content = get_content_for_platform("telegram")
    
    # 1. Discord
    discord_ok = post_to_discord(content, "education")
    log(f"Discord: {'OK' if discord_ok else 'FAIL'}")
    
    # 2. Telegram DM
    telegram_dm(short_content)
    
    # 3. Binance pump alerts - check and post if something moved
    try:
        import hashlib, hmac, base64
        from urllib.parse import urlencode
        from decimal import Decimal
        
        BINANCE_KEY = os.environ.get('BINANCE_API_KEY', '')
        BINANCE_SECRET = os.environ.get('BINANCE_SECRET_KEY', '')
        
        if BINANCE_KEY and BINANCE_SECRET:
            # Get top gainers
            ts = int(time.time() * 1000)
            params = f"timestamp={ts}"
            sig = hmac.new(BINANCE_SECRET.encode(), params.encode(), hashlib.sha256).hexdigest()
            url = f"https://api.binance.com/api/v3/ticker/24hr?timestamp={ts}&signature={sig}"
            
            r = requests.get("https://api.binance.com/api/v3/ticker/24hr", timeout=10)
            if r.status_code == 200:
                tickers = r.json()
                # Find top gainers (filter for decent volume)
                gainers = []
                for t in tickers:
                    try:
                        price = float(t.get('lastPrice', 0))
                        change = float(t.get('priceChangePercent', 0))
                        volume = float(t.get('quoteVolume', 0))
                        if change > 5 and volume > 1_000_000 and price > 0.0001:
                            gainers.append((t['symbol'], change, volume))
                    except:
                        pass
                
                gainers.sort(key=lambda x: x[1], reverse=True)
                top5 = gainers[:5]
                
                if top5:
                    pump_msg = "🚨 **TOP GAINERS RIGHT NOW**\n\n"
                    for sym, chg, vol in top5:
                        pump_msg += f"${sym}: +{chg:.1f}%\n"
                    pump_msg += f"\n{PAYPIP_LINK}"
                    
                    post_to_discord(pump_msg, "pump")
                    telegram_dm(pump_msg)
                    log(f"Binance pump alerts: Posted {len(top5)} gainers")
    except Exception as e:
        log(f"Binance monitor: {e}")
    
    # 4. Fresh content to Discord
    fresh = get_random_education()
    post_to_discord(fresh, "education")
    
    log("=== CAMPAIGN COMPLETE ===")

# ============================================================
# COMMUNITY GROWTH - Find new audiences
# ============================================================
def discover_crypto_communities():
    """Find new Discord servers and Telegram groups to grow audience"""
    log("Looking for crypto communities...")
    
    # Known crypto Discord server invite codes (public servers)
    # These are public servers that allow member invites
    public_servers = [
        "cryptotrader", "bitcoin", "ethereum", "defi", 
        "cryptomoon", "cryptocurrency", "binance"
    ]
    
    return public_servers

def post_to_quora():
    """Post SEO content to Quora (via browser - needs human verification)"""
    log("Quora: Needs manual browser access - skipping in automated mode")
    return False

if __name__ == "__main__":
    run_content_campaign()