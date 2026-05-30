#!/usr/bin/env python3
"""
Post educational content to Discord - runs every hour
Keeps the channel active and engaging
"""
import os, sys, requests, random
from datetime import datetime

WORKDIR = "C:/Users/INSPIRON/smartlivingcircle-marketing"
sys.path.insert(0, WORKDIR)

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1510211779924463748/kg-TcdfPw5e-dqCF7-9MuN6xZlReHsWZjoXKNwXn8UjChG7BBx3jvpEOBtoKPL6UHngC"
DISCORD_INVITE = "https://discord.gg/YSc6tUuSaD"
PAYPIP_LINK = "https://payhip.com/b/1vtcL"

POSTS = [
    {
        "title": "💡 DeFi Tip of the Day",
        "content": "Did you know? Flash loans let you borrow MILLIONS without collateral—as long as you return it in the same transaction.\n\nThis is how whales exploit price differences across exchanges instantly.\n\nI broke down 7 proven flash loan strategies in my guide. Link in bio.",
        "color": 0x00AAFF
    },
    {
        "title": "📊 Market Pattern Alert",
        "content": "When BTC pumps, here's the typical flow:\n1. BTC rises\n2. ETH follows\n3. Altcoins explode\n4. Then... correction\n\nThe smart play: Buy established alts DURING the BTC pump, not after.\n\nJoin our Discord for real-time alpha.",
        "color": 0xFFAA00
    },
    {
        "title": "🔐 Security Reminder",
        "content": "STOP: Before you click any crypto link\n\n✅ Check the URL 3x\n✅ Google the project first\n✅ NEVER share your seed phrase\n✅ Use 2FA everywhere\n\nOne mistake = total loss. Stay safe out there.",
        "color": 0xFF4444
    },
    {
        "title": "📚 Crypto Education",
        "content": "What is 'impermanent loss'?\n\nWhen you provide liquidity to a DEX pool (e.g., ETH + USDC), and one asset moves significantly in price, you can end up with LESS value than just holding.\n\nThis is why understanding DeFi mechanics is CRITICAL before depositing funds.\n\nMy guide covers this and more. Link in bio.",
        "color": 0x00FF88
    },
    {
        "title": "🚀 Swing Trade Watch",
        "content": "The best swing trade setups happen when:\n- A coin pumps 20%+ on high volume\n- It has a real use case\n- The team is doxxed\n\nNot all pumps are scams—but most are. Can you tell the difference?\n\nLearn to spot the difference in my guide.",
        "color": 0xAA00FF
    },
    {
        "title": "💰 Risk Management 101",
        "content": "Rule #1: Never risk more than 2% of your portfolio on a single trade.\n\nIf you have $1,000 → max $20 per trade.\n\nThis way, even 10 losses in a row won't destroy you.\n\nMost traders break this rule. Don't be most traders.",
        "color": 0xFF6600
    },
    {
        "title": "📡 Alpha Signal",
        "content": "Following crypto influencers won't make you money.\n\nKnowing HOW they think will.\n\nThe difference between retail and smart money:\n- Retail trades on tips\n- Smart money researches first\n- Smart money manages risk\n- Smart money takes profits\n\nWhich one are you?",
        "color": 0x00AACC
    },
    {
        "title": "⚡ Flash Loan Explained",
        "content": "Flash loans = free loans if you're fast enough.\n\nBorrow → Trade → Return → Keep profit\n\nAll in one transaction. No risk to you if the trade fails (you just don't profit).\n\nThis is DeFi at its most powerful. Learn it:\nhttps://payhip.com/b/1vtcL",
        "color": 0x00FF00
    },
]

def post_content():
    post = random.choice(POSTS)
    
    msg = f"{post['content']}\n\n👉 Join us: {DISCORD_INVITE}\n📚 Free guide: {PAYPIP_LINK}"
    
    data = {
        "embeds": [{
            "title": post['title'],
            "description": msg,
            "color": post['color'],
            "footer": {"text": f"SmartLivingCircle • {datetime.now().strftime('%H:%M UTC')}"}
        }]
    }
    
    r = requests.post(DISCORD_WEBHOOK, json=data, headers={"Content-Type": "application/json"}, timeout=10)
    if r.status_code == 204:
        print(f"[{datetime.now().strftime('%H:%M')}] Posted: {post['title'][:30]}")
    else:
        print(f"[{datetime.now().strftime('%H:%M')}] Failed: {r.status_code}")

if __name__ == "__main__":
    post_content()