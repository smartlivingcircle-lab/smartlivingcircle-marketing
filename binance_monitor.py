#!/usr/bin/env python3
"""
Binance Crypto Monitor
Monitors Binance for new listings, pump signals, whale alerts
Sends alerts to Discord + Telegram
Drives organic traffic by providing VALUE to crypto traders
"""

import os
import sys
import time
import json
import hmac
import hashlib
import requests
from datetime import datetime
from urllib.parse import urlencode

# ─── CONFIG ──────────────────────────────────────────────────────────────────
BINANCE_API_KEY = os.environ.get('BINANCE_API_KEY', 'rOK72URbgdJkZ8h8RyQE6PvvHowFITRymUsWAgqFZPZhz3NijmXGtgAmYiUNBqJ9')
BINANCE_SECRET  = os.environ.get('BINANCE_SECRET', '3FapeEQsLMJVaR1xF7YHKyDQatmcgXcOfvIo6DDy5HaeQ1NqeyIFg4S6tsx90qnw')
DISCORD_WEBHOOK = os.environ.get('DISCORD_WEBHOOK', 'https://discord.com/api/webhooks/1510211779924463748/kg-TcdfPw5e-dqCF7-9MuN6xZlReHsWZjoXKNwXn8UjChG7BBx3jvpEOBtoKPL6UHngC')
TELEGRAM_TOKEN   = os.environ.get('TELEGRAM_BOT_TOKEN', '8889649869:AAFD9DiTckmtHn3lBqzAPmyjP7__aLYyR9o')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '')
PAYHIP_LINK      = os.environ.get('PAYHIP_LINK', 'https://payhip.com/b/1vtcL')

HEADERS = {"X-MBX-APIKEY": BINANCE_API_KEY}
STATE_FILE = "monitor_state.json"

# ─── BINANCE API ──────────────────────────────────────────────────────────────
def binance_request(endpoint, params=None):
    params = params or {}
    params["timestamp"] = int(time.time() * 1000)
    params["signature"] = hmac.new(
        BINANCE_SECRET.encode(),
        urlencode(params).encode(),
        hashlib.sha256
    ).hexdigest()
    r = requests.get(f"https://api.binance.com{endpoint}", params=params, headers=HEADERS, timeout=10)
    try:
        return r.json()
    except:
        return {}

def binance_public(endpoint, params=None):
    r = requests.get(f"https://api.binance.com{endpoint}", params=params or {}, timeout=10)
    try:
        return r.json()
    except:
        return {}

# ─── STATE PERSISTENCE ────────────────────────────────────────────────────────
def load_state():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except:
        return {"watched_symbols": set(), "posted_alerts": [], "last_check": None}

def save_state(state):
    state["posted_alerts"] = state["posted_alerts"][-50:]  # keep last 50
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, default=str)

# ─── ALERTS ──────────────────────────────────────────────────────────────────
def post_discord(title, description, color=16732979, fields=None, url=None):
    try:
        data = {
            "embeds": [{
                "title": title,
                "description": description,
                "color": color,
                "footer": {"text": f"SmartLivingCircle | {datetime.now().strftime('%H:%M UTC')}"},
                "fields": fields or []
            }]
        }
        if url:
            data["embeds"][0]["url"] = url
        requests.post(DISCORD_WEBHOOK, json=data, headers={"Content-Type": "application/json"}, timeout=10)
    except Exception as e:
        print(f"  Discord error: {e}")

def post_telegram(text):
    if not TELEGRAM_CHAT_ID:
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=10)
    except Exception as e:
        print(f"  Telegram error: {e}")

# ─── MONITORS ────────────────────────────────────────────────────────────────
def check_new_listings(state):
    """Find brand new trading pairs on Binance Spot"""
    try:
        tickers = binance_public("/api/v3/ticker/24hr")
        if not isinstance(tickers, list):
            return
        
        new_symbols = []
        for t in tickers:
            symbol = t.get("symbol", "")
            # Check if it's a relatively new listing (very high 24h volume for a new pair)
            if symbol.endswith(("USDT", "BUSD", "BNB")):
                volume = float(t.get("quoteVolume", 0))
                if volume > 1_000_000:  # $1M+ volume
                    if symbol not in state["watched_symbols"]:
                        state["watched_symbols"].add(symbol)
                        new_symbols.append((symbol, volume, t))
        
        if new_symbols:
            for symbol, volume, t in sorted(new_symbols, key=lambda x: -x[1])[:3]:
                price = float(t.get("lastPrice", 0))
                change = float(t.get("priceChangePercent", 0))
                state["posted_alerts"].append(f"NEW_PAIR:{symbol}")
                print(f"  🆕 NEW: {symbol} | Vol: ${volume:,.0f} | Price: ${price} | 24h: {change:+.2f}%")
                
                fields = [
                    {"name": "Symbol", "value": f"`{symbol}`", "inline": True},
                    {"name": "24h Volume", "value": f"${volume:,.0f}", "inline": True},
                    {"name": "Price", "value": f"${price:.6f}", "inline": True},
                ]
                post_discord(
                    f"🆕 New Binance Pair",
                    f"**{symbol}** just appeared with ${volume/1e6:.1f}M 24h volume!\n\n💰 Price: `${price}` | 24h: **{change:+.2f}%**\n\n📖 Learn DeFi trading strategies: {PAYHIP_LINK}",
                    color=0x00ff00,
                    fields=fields,
                    url="https://www.binance.com/en/support/announcement"
                )
    except Exception as e:
        print(f"  Listings error: {e}")

def check_top_gainers():
    """Top gainers in last 24h - useful for pump detection"""
    try:
        tickers = binance_public("/api/v3/ticker/24hr")
        if not isinstance(tickers, list):
            return
        
        gainers = []
        for t in tickers:
            symbol = t.get("symbol", "")
            if symbol.endswith("USDT"):
                change = float(t.get("priceChangePercent", 0))
                volume = float(t.get("quoteVolume", 0))
                if change > 15 and volume > 5_000_000:  # 15%+ gain + $5M vol
                    gainers.append((symbol, change, volume))
        
        if gainers:
            gainers.sort(key=lambda x: -x[1])
            top = gainers[0]
            print(f"  📈 TOP GAINER: {top[0]} | {top[1]:+.2f}% | Vol: ${top[2]:,.0f}")
            
            post_discord(
                f"📈 Pump Alert: {top[0]}",
                f"**{top[0]}** is up **{top[1]:+.2f}%** in 24h!\n\nVolume: ${top[2]/1e6:.1f}M\n\n⚠️ DYOR! Don't chase pumps.\n\n📚 Flash Loan guide for advanced strategies: {PAYHIP_LINK}",
                color=0xff6600
            )
    except Exception as e:
        print(f"  Gainers error: {e}")

def check_binance_announcements():
    """Check latest Binance announcements"""
    try:
        r = requests.get("https://api.binance.com/api/v3/exchangeInfo", timeout=10)
        # Check for new symbols traded today
        tickers = binance_public("/api/v3/ticker/24hr")
        if not isinstance(tickers, list):
            return
        
        today = datetime.utcnow().strftime("%Y-%m-%d")
        new_today = []
        for t in tickers:
            symbol = t.get("symbol", "")
            if symbol.endswith("USDT"):
                # Rough filter: symbols with very low price that just started moving
                price = float(t.get("lastPrice", 0))
                change = float(t.get("priceChangePercent", 0))
                if 0 < price < 0.01 and change > 50:  # sub-penny coins with huge moves
                    new_today.append((symbol, price, change))
        
        if new_today:
            new_today.sort(key=lambda x: -x[2])
            top = new_today[0]
            print(f"  💎 MICRO PUMP: {top[0]} | Price: ${top[1]:.8f} | {top[2]:+.1f}%")
            
            post_discord(
                f"💎 Micro Coin Alert: {top[0]}",
                f"Sub-penny token **{top[0]}** surging {top[2]:+.1f}%!\n\nPrice: `${top[1]:.8f}`\n\n⚠️ High risk - these are speculative. Read our DeFi guide first: {PAYHIP_LINK}",
                color=0xff00ff
            )
    except Exception as e:
        print(f"  Announcements error: {e}")

def check_whale_trades():
    """Monitor for large USDT trades (> $500k)"""
    try:
        # Get recent trades on major pairs
        for symbol in ["BTCUSDT", "ETHUSDT", "BNBUSDT"]:
            r = requests.get(
                f"https://api.binance.com/api/v3/trades",
                params={"symbol": symbol, "limit": 5},
                timeout=10
            )
            if isinstance(r.json(), list) and r.json():
                last_trade = r.json()[-1]
                qty = float(last_trade.get("qty", 0))
                price = float(last_trade.get("price", 0))
                value = qty * price
                if value > 500_000:
                    side = "🟢 BUY" if last_trade.get("isBuyerMaker") == False else "🔴 SELL"
                    print(f"  🐋 WHALE: {symbol} | {side} ${value/1e6:.2f}M")
    except Exception as e:
        print(f"  Whale error: {e}")

# ─── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    print("=" * 55)
    print("BINANCE MONITOR - SmartLivingCircle Traffic Engine")
    print("=" * 55)
    
    state = load_state()
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Running checks...")
    
    check_new_listings(state)
    check_top_gainers()
    check_binance_announcements()
    check_whale_trades()
    
    state["last_check"] = datetime.now().isoformat()
    save_state(state)
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Done")

if __name__ == "__main__":
    main()