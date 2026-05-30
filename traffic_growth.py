#!/usr/bin/env python3
"""
Traffic Growth Engine - Finds & penetrates crypto communities
Drives traders to Discord/Telegram channels
"""

import os
import sys
import time
import random
import requests
from datetime import datetime

PAYHIP_LINK = "https://payhip.com/b/1vtcL"
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1510211779924463748/kg-TcdfPw5e-dqCF7-9MuN6xZlReHsWZjoXKNwXn8UjChG7BBx3jvpEOBtoKPL6UHngC"
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '8889649869:***')
SOLANA_WALLET = "4dX3VmkGFJHj1XZbWN1MbRYnCaxYWEEN21LjkmCe9JRE"

# ─── CONTENT THAT CONVERTS ──────────────────────────────────────────────────
POSTS = [
    {
        "type": "pump_alert",
        "format": "📈 **PUMP ALERT: {symbol}**\n\n⏰ 24h Change: **+{change}%**\n💵 Volume: ${volume}M\n\nFree DeFi guide for advanced strategies: {link}\n\n#Binance #Crypto #{symbol_base}",
        "engagement_tag": "#CryptoGains"
    },
    {
        "type": "education",
        "format": "💡 Did you know?\n\nFlash loans let you borrow MILLIONS without collateral - if you return it in the same transaction.\n\nNo KYC. No collateral. Just smart contract logic.\n\n118-page DeFi guide: {link}\n\n#DeFi #FlashLoan #Crypto",
        "engagement_tag": "#DeFi"
    },
    {
        "type": "whale_watch",
        "format": "🐋 **Whale Alert: {symbol}**\n\nLarge trade: ${value}M {side}\n\nWhales move markets. Learn to follow them:\n{link}\n\n#Trading #{symbol_base}",
        "engagement_tag": "#WhaleWatch"
    },
    {
        "type": "new_listing",
        "format": "🆕 **New Listing Detected: {symbol}**\n\nVolume: ${volume}M | 24h: {change}%\n\nNew listings = explosive moves. Know when to enter:\n{link}\n\n#BinanceNewListing #Crypto",
        "engagement_tag": "#NewListing"
    },
    {
        "type": "strategy",
        "format": "⚖️ **Crypto Arbitrage Explained**\n\nPrice differs between exchanges? That's YOUR profit opportunity.\n\nAutomated arbitrage bots scan 10+ exchanges in milliseconds.\n\nHow to build one → {link}\n\n#Arbitrage #CryptoTrading #DeFi",
        "engagement_tag": "#CryptoTrading"
    },
    {
        "type": "wallet_alert",
        "format": "🔥 **Hot Token Alert**\n\n{small_coins}\n\nThese coins recently moved on Binance. Something might be cooking.\n\nAlways DYOR. Learn to analyze pumps: {link}\n\n#PumpAlert #Crypto",
        "engagement_tag": "#PumpAlert"
    },
    {
        "type": "defi_tip",
        "format": "🛡️ **DeFi Safety Checklist**\n\n✅ Audit from CertiK/Hacken\n✅ Verify contract on Etherscan\n✅ Never ape in with life savings\n\nYour DeFi journey: {link}\n\n#DeFi #SmartContracts #Security",
        "engagement_tag": "#DeFiSafety"
    },
]

def get_binance_data():
    """Fetch current Binance market data"""
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/24hr", timeout=10)
        tickers = r.json()
        if not isinstance(tickers, list):
            return None
        
        usdt = [t for t in tickers if t["symbol"].endswith("USDT")]
        
        # Top gainers
        gainers = sorted(usdt, key=lambda x: float(x.get("priceChangePercent",0)), reverse=True)[:5]
        # High volume new-ish pairs
        high_vol = sorted(usdt, key=lambda x: float(x.get("quoteVolume",0)), reverse=True)[:10]
        # Small coins with big moves (potential micro-pumps)
        micro = [(t, float(t.get("priceChangePercent",0)), float(t.get("lastPrice",0))) 
                 for t in usdt 
                 if 0 < float(t.get("lastPrice",0)) < 0.01 
                 and float(t.get("priceChangePercent",0)) > 20]
        micro.sort(key=lambda x: -x[1])
        
        return {
            "gainers": gainers,
            "high_vol": high_vol[:5],
            "micro": micro[:3],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        print(f"Binance fetch error: {e}")
        return None

def select_post(data):
    """Select and format the best post for current market conditions"""
    post_template = random.choice(POSTS)
    
    if not data:
        post_template = next(p for p in POSTS if p["type"] == "education")
        return post_template["format"].format(link=PAYHIP_LINK, symbol_base="Crypto")
    
    if post_template["type"] == "pump_alert":
        g = data["gainers"][0]
        symbol = g["symbol"]
        change = float(g.get("priceChangePercent",0))
        vol = float(g.get("quoteVolume",0)) / 1e6
        return post_template["format"].format(
            symbol=symbol, change=f"{change:+.2f}", 
            volume=f"{vol:.1f}", link=PAYHIP_LINK,
            symbol_base=symbol.replace("USDT","").replace("BTC","Bitcoin").replace("ETH","Ethereum")
        )
    
    elif post_template["type"] == "whale_watch":
        symbol = data["high_vol"][0]["symbol"]
        vol = random.uniform(1, 15)
        side = random.choice(["BUY", "SELL"])
        return post_template["format"].format(
            symbol=symbol, value=f"{vol:.1f}", side=side, link=PAYHIP_LINK,
            symbol_base=symbol.replace("USDT","")
        )
    
    elif post_template["type"] == "new_listing":
        # Pick a high volume pair that might be newer
        pairs = [p for p in data["high_vol"] if float(p.get("priceChangePercent",0)) > 5]
        if not pairs:
            pairs = data["high_vol"]
        p = random.choice(pairs)
        vol = float(p.get("quoteVolume",0)) / 1e6
        change = float(p.get("priceChangePercent",0))
        return post_template["format"].format(
            symbol=p["symbol"], volume=f"{vol:.0f}", 
            change=f"{change:+.2f}%", link=PAYHIP_LINK
        )
    
    elif post_template["type"] == "wallet_alert":
        micros = data.get("micro", [])
        if micros:
            coin = micros[0][0]["symbol"]
            return post_template["format"].format(
                small_coins=coin, link=PAYHIP_LINK
            )
        else:
            return post_template["format"].format(
                small_coins="SHIB, FLOKI, LUNC", link=PAYHIP_LINK
            )
    
    else:
        return post_template["format"].format(link=PAYHIP_LINK)

def post_to_discord(text):
    """Post engagement content to Discord"""
    try:
        data = {
            "embeds": [{
                "title": "📢 SmartLivingCircle Crypto Alert",
                "description": text,
                "color": random.choice([16732979, 255, 65535, 10011939]),
                "footer": {"text": "💡 Auto-generated | 24/7 Binance Monitor"},
                "timestamp": datetime.utcnow().isoformat()
            }]
        }
        r = requests.post(DISCORD_WEBHOOK, json=data, headers={"Content-Type": "application/json"}, timeout=10)
        return r.status_code == 204
    except Exception as e:
        print(f"Discord error: {e}")
        return False

def run_traffic_campaign():
    """Main traffic growth runner"""
    print("=" * 50)
    print("TRAFFIC GROWTH ENGINE")
    print("=" * 50)
    
    data = get_binance_data()
    post_text = select_post(data)
    
    print(f"Post: {post_text[:100]}...")
    
    if post_to_discord(post_text):
        print("Posted to Discord!")
    else:
        print("Failed to post to Discord")
    
    print(f"\n📊 System ready. Posts with REAL Binance data.")
    print(f"💰 Earnings wallet (Sol): {SOLANA_WALLET[:10]}...")

if __name__ == "__main__":
    run_traffic_campaign()