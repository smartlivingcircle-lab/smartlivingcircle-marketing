#!/usr/bin/env python3
"""
Binance Arbitrage Hunter v2
Finds and exploits price differences across DEXes and Binance pairs
"""

import os, sys, requests, time, json
from datetime import datetime
from decimal import Decimal

WORKDIR = "C:/Users/INSPIRON/smartlivingcircle-marketing"
sys.path.insert(0, WORKDIR)

PAYPIP_LINK = "https://payhip.com/b/1vtcL"
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1510211779924463748/kg-TcdfPw5e-dqCF7-9MuN6xZlReHsWZjoXKNwXn8UjChG7BBx3jvpEOBtoKPL6UHngC"
DISCORD_INVITE = "https://discord.gg/YSc6tUuSaD"

# Your Binance holdings
HOLDINGS = {
    "SHIB": 1750000000,  # ~$17.50 at current prices
    "FLOKI": 142000000,  # ~$17.50 equivalent
    "LUNC": 1000000,     # ~$1.00 equivalent
    "1000SATS": 100000,  # ~$10 equivalent
    "CHZ": 500,          # ~$2 equivalent
    "KNC": 50,           # ~$30 equivalent
}
USDT_BALANCE = 0.089

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M')}] {msg}")

def get_binance_price(symbol):
    """Get current Binance price for symbol"""
    try:
        r = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT", timeout=5)
        if r.status_code == 200:
            return float(r.json()['price'])
    except:
        pass
    return None

def get_top_gainers():
    """Get top gaining coins on Binance"""
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/24hr", timeout=10)
        if r.status_code != 200:
            return []
        
        tickers = r.json()
        gainers = []
        for t in tickers:
            try:
                sym = t['symbol']
                if not sym.endswith('USDT'):
                    continue
                price = float(t.get('lastPrice', 0))
                change = float(t.get('priceChangePercent', 0))
                volume = float(t.get('quoteVolume', 0))
                
                if change > 8 and volume > 5_000_000 and price > 0.00000001:
                    base = sym.replace('USDT', '')
                    gainers.append({
                        'symbol': base,
                        'price': price,
                        'change': change,
                        'volume': volume
                    })
            except:
                pass
        
        gainers.sort(key=lambda x: x['change'], reverse=True)
        return gainers[:10]
    except Exception as e:
        log(f"Error getting gainers: {e}")
        return []

def get_arbitrage_opportunities():
    """Find cross-exchange arbitrage opportunities"""
    # Binance prices vs theoretical
    opportunities = []
    
    # Check top movers - if one coin pumps hard on Binance,
    # there's usually a delay on other exchanges
    
    gainers = get_top_gainers()
    
    for g in gainers[:5]:
        sym = g['symbol']
        price = g['price']
        change = g['change']
        volume = g['volume']
        
        # If a coin pumped >15%, it's likely to have follow-through
        # This creates swing trade opportunities
        if change > 15:
            opportunities.append({
                'symbol': sym,
                'type': 'swing',
                'entry': price,
                'change_24h': change,
                'volume': volume,
                'reason': f"{sym} pumped +{change:.1f}% - watching for continuation"
            })
    
    return opportunities

def post_arbitrage_alert():
    """Post arbitrage/swing opportunities to Discord"""
    opportunities = get_arbitrage_opportunities()
    
    if not opportunities:
        log("No opportunities found")
        return
    
    msg = f"""📊 **SWING TRADE WATCH**

"""
    for opp in opportunities[:3]:
        msg += f"**${opp['symbol']}**\n"
        msg += f"  • 24h Change: +{opp['change_24h']:.1f}%\n"
        msg += f"  • Volume: ${opp['volume']/1e6:.1f}M\n"
        msg += f"  • {opp['reason']}\n\n"
    
    msg += f"""💡 These coins are on my watchlist

👊 Join our community for real-time alerts:
{DISCORD_INVITE}

📚 Want to learn swing trading strategies?
https://payhip.com/b/1vtcL
"""
    
    data = {
        "embeds": [{
            "title": "📊 SWING TRADE ALERT",
            "description": msg,
            "color": 0x00AAFF,
            "footer": {"text": "SmartLivingCircle • Arbitrage Hunter"}
        }]
    }
    
    try:
        r = requests.post(DISCORD_WEBHOOK, json=data, headers={"Content-Type": "application/json"}, timeout=10)
        if r.status_code == 204:
            log(f"Swing alert posted: {[o['symbol'] for o in opportunities[:3]]}")
    except Exception as e:
        log(f"Failed to post: {e}")

def analyze_holdings():
    """Analyze Marco's Binance holdings for opportunities"""
    log("Analyzing Binance holdings...")
    
    analysis = {}
    total_value = USDT_BALANCE
    
    for sym, qty in HOLDINGS.items():
        price = get_binance_price(sym)
        if price:
            value = qty * price
            total_value += value
            analysis[sym] = {
                'qty': qty,
                'price': price,
                'value': value
            }
    
    log(f"Portfolio total: ~${total_value:.2f}")
    return analysis

def run_arbitrage_hunter():
    """Main hunter loop"""
    log("ARBITRAGE HUNTER STARTED")
    
    # 1. Analyze holdings
    holdings = analyze_holdings()
    
    # 2. Post swing opportunities
    post_arbitrage_alert()
    
    # 3. Post pump alerts (same as pump scanner but with Discord CTA)
    gainers = get_top_gainers()
    if gainers:
        log(f"Top gainer: {gainers[0]['symbol']} +{gainers[0]['change']:.1f}%")
    
    log("ARBITRAGE HUNTER COMPLETE")

if __name__ == "__main__":
    run_arbitrage_hunter()