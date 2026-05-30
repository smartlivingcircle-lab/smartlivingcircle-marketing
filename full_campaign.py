#!/usr/bin/env python3
"""
Full Traffic Campaign - Posts to ALL platforms
Bluesky + Discord + Telegram simultaneously
"""

import os, sys, time, random
import requests as r

PAYPIP_LINK = "https://payhip.com/b/1vtcL"
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1510211779924463748/kg-TcdfPw5e-dqCF7-9MuN6xZlReHsWZjoXKNwXn8UjChG7BBx3jvpEOBtoKPL6UHngC"
TELEGRAM_TOKEN="8889649869:AAEQ3uZ2mI-2hZ3jK5kL8mN1pQ9rS6tU2vW0-xy"
TELEGRAM_USER_ID="6180735205"

EDUCATION_POSTS = [
    "⚡ FLASH LOANS: The secret weapon of DeFi whales\n\nMost traders don't know they exist.\nA flash loan lets you borrow ANY amount without collateral—as long as you return it in the SAME transaction.\n\nHow whales use them:\n→ Arbitrage between DEXs\n→ Collateral swaps\n→ Liquidate underwater positions\n\nMy new guide covers 7 proven flash loan strategies:\nhttps://payhip.com/b/1vtcL\n\n#DeFi #FlashLoans #Crypto #Ethereum #Web3",

    "💰 Why most crypto traders LOSE money\n\nNot because they're stupid.\nBecause they trade on emotion, not data.\n\nThe 3 rules of profitable trading:\n1️⃣ Cut losses fast, let winners run\n2️⃣ Never risk more than 2% per trade\n3️⃣ Use leverage ONLY when odds are in your favor\n\nI made $2,400 last month following these rules.\nLearn the exact strategies:\nhttps://payhip.com/b/1vtcL\n\n#Crypto #Trading #Bitcoin #Ethereum",

    "🧵 What I've learned from 5 years in crypto:\n\n→ 90% of 'opportunities' are scams\n→ The best time to buy is when news is bad\n→ Dollar-cost averaging beats timing the market\n→ Flash loans can generate risk-free profits\n→ Most people will never understand DeFi\n\nMy 118-page guide covers everything I wish I knew sooner:\nhttps://payhip.com/b/1vtcL\n\nSave this. Come back to it in 2 years. #Crypto #DeFi #Web3",

    "🔍 How to spot a rug pull BEFORE it happens:\n\n1️⃣ Check team doxx (real names? LinkedIn?)\n2️⃣ LP locked? (Uniswap shows this)\n3️⃣ Taxing bot? (40%+ fee = red flag)\n4️⃣ Social accounts created recently?\n5️⃣ Unusual whale activity (someone dumping)\n\nThe guide I've linked covers 12 more warning signs:\nhttps://payhip.com/b/1vtcL\n\nStay safe out there 🛡️ #Crypto #DeFi #BSC #Ethereum",

    "📊 THE BIGGEST CRYPTO OPPORTUNITY nobody talks about:\n\nFlash loans.\n\nYou borrow millions WITHOUT collateral.\nYou execute a trade.\nYou return the loan.\nAll in one transaction.\n\nRisk-free profit IF you know what you're doing.\n\nI wrote a complete 118-page guide on this:\nhttps://payhip.com/b/1vtcL\n\nFree to read. #Crypto #FlashLoans #Arbitrage #DeFi"
]

BLUESKY_POSTS = [
    """⚡ FLASH LOANS explained simply:

You borrow millions WITHOUT collateral.
You make a trade.
You return the loan.
All in ONE transaction.

Whales use this for arbitrage every day.

I wrote a 118-page guide showing 7 proven strategies:
https://payhip.com/b/1vtcL

#DeFi #Crypto #Web3 #Ethereum""",

    """5 years in crypto taught me:

→ 90% of 'opportunities' are scams
→ Best time to buy = bad news
→ DCA beats timing the market
→ Flash loans = risk-free profit IF you know how

My complete guide:
https://payhip.com/b/1vtcL

Save this. Come back in 2 years. #Crypto #DeFi""",

    """How to spot a rug pull BEFORE you invest:

1️⃣ Team doxxed?
2️⃣ LP locked?
3️⃣ Taxing bot 40%+?
4️⃣ New socials?
5️⃣ Whale dumping?

12 more warning signs in my guide:
https://payhip.com/b/1vtcL

🛡️ Stay safe #Crypto #DeFi"""
]

def post_discord(content):
    data = {"embeds": [{"description": content, "color": 0x0099FF, "url": PAYPIP_LINK}]}
    return r.post(DISCORD_WEBHOOK, json=data, headers={"Content-Type": "application/json"}, timeout=10).status_code == 204

def post_bluesky(text):
    try:
        from atproto import Client
        from datetime import datetime, timezone
        client = Client()
        client.login("smartlivingcircle.bsky.social", "p2r7-cb7g-ffj2-6i3s")
        p = client.send_post(text)
        return True, str(p.uri)
    except Exception as e:
        return False, str(e)

def send_telegram(text):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        resp = r.post(url, json={"chat_id": TELEGRAM_USER_ID, "text": text, "parse_mode": "HTML"}, timeout=10)
        return resp.json().get('ok', False)
    except:
        return False

def get_binance_gainers():
    try:
        tickers = r.get("https://api.binance.com/api/v3/ticker/24hr", timeout=10).json()
        gainers = []
        for t in tickers:
            try:
                price = float(t.get('lastPrice', 0))
                change = float(t.get('priceChangePercent', 0))
                volume = float(t.get('quoteVolume', 0))
                if change > 5 and volume > 5_000_000 and price > 0.00001:
                    gainers.append((t['symbol'], change, volume))
            except:
                pass
        gainers.sort(key=lambda x: x[1], reverse=True)
        return gainers[:5]
    except:
        return []

def run_campaign():
    print("=== FULL TRAFFIC CAMPAIGN ===")
    ts = time.strftime("%H:%M")
    print(f"[{ts}] Starting multi-platform post...")
    
    # 1. Binance gainers alert
    gainers = get_binance_gainers()
    if gainers:
        msg = "🚨 <b>TOP GAINERS</b>\n\n"
        for sym, chg, _ in gainers:
            msg += f"${sym}: +{chg:.1f}%\n"
        msg += f"\n<a href='{PAYPIP_LINK}'>Get my DeFi guide</a>"
        send_telegram(msg)
        # Also Discord
        dmsg = "🚨 **TOP GAINERS**\n\n" + "\n".join(f"${s}: +{c:.1f}%" for s,c,_ in gainers)
        dmsg += f"\n\nhttps://payhip.com/b/1vtcL"
        post_discord(dmsg)
        print(f"[{ts}] Pump alert: {len(gainers)} gainers")
    
    # 2. Random education post
    content = random.choice(EDUCATION_POSTS)
    ok = post_discord(content)
    print(f"[{ts}] Discord: {'OK' if ok else 'FAIL'}")
    
    # 3. Bluesky post (3-post rotation)
    bsky_content = random.choice(BLUESKY_POSTS)
    ok, result = post_bluesky(bsky_content)
    print(f"[{ts}] Bluesky: {'OK → ' + result[-30:] if ok else 'FAIL: ' + result[:50]}")
    
    print("=== CAMPAIGN DONE ===")

if __name__ == "__main__":
    run_campaign()