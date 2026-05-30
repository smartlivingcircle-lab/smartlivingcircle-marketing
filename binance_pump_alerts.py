#!/usr/bin/env python3
"""
Binance Crypto Pump Alert Scanner v2
Monitors Binance for sudden pumps → posts to Discord + Telegram
Drives traffic to Payhip funnel

RUN: py -3 binance_pump_alerts.py
"""

import os, sys, time, requests
from datetime import datetime

WORKDIR = "C:/Users/INSPIRON/smartlivingcircle-marketing"
sys.path.insert(0, WORKDIR)

PAYPIP_LINK = "https://payhip.com/b/1vtcL"
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1510211779924463748/kg-TcdfPw5e-dqCF7-9MuN6xZlReHsWZjoXKNwXn8UjChG7BBx3jvpEOBtoKPL6UHngC"
TELEGRAM_BOT_TOKEN = "8889649869:***"
TELEGRAM_USER_ID = "6180735205"

# Known meme coins to watch (high volatility = pump potential)
MEME_COINS = [
    "FLOKI", "SHIB", "LUNC", "1000SATS", "PEPE", "WIF", "BOME", 
    "FLOKIUSDT", "SHIBUSDT", "LUNCUSDT", "1000SATSUSDT", "PEPEUSDT",
    "WIFUSDT", "BOMEUSDT", "BONKUSDT", "SMOLETH", "RATSUSDT"
]

MIN_VOLUME_USD = 500_000   # Min 24h volume to care about
MIN_PUMP_PCT = 5           # Min % gain to trigger alert
SCAN_INTERVAL = 60         # Seconds between scans

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def binance_ticker(symbol):
    r = requests.get(f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}", timeout=10)
    if r.status_code == 200:
        d = r.json()
        return {
            'symbol': symbol,
            'price': float(d['lastPrice']),
            'change_pct': float(d['priceChangePercent']),
            'volume': float(d['quoteVolume']),
            'high': float(d['highPrice']),
            'low': float(d['lowPrice']),
            'count': int(d['count'])  # number of trades
        }
    return None

def post_discord_pump(ticker_data):
    d = ticker_data
    color = 0x00FF00 if d['change_pct'] < 15 else 0xFF4500
    
    # Build coin name without USDT
    coin = d['symbol'].replace('USDT','').replace('SHIB','SHIBA').replace('1000SATS','1000SATS')
    
    content = f"""
🚨 **PUMP DETECTED: ${coin}**

📈 **+{d['change_pct']:.1f}%** in 24h
💰 Price: ${d['price']:.8f}
📊 Volume: ${d['volume']/1e6:.2f}M
🔼 High: ${d['high']:.8f} | 🔽 Low: ${d['low']:.8f}

Trades: {d['count']:,}

_Track more pumps in real-time_ 👆
"""
    
    data = {
        "content": content.strip(),
        "embeds": [{
            "title": f"🚨 PUMP ALERT: ${coin} +{d['change_pct']:.1f}%",
            "description": f"Price: ${d['price']:.8f}\nVolume: ${d['volume']/1e6:.1f}M\nTrades: {d['count']:,}",
            "color": color,
            "url": PAYPIP_LINK,
            "footer": {"text": "SmartLivingCircle • Free Alpha"},
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }]
    }
    
    r = requests.post(DISCORD_WEBHOOK, json=data, headers={"Content-Type": "application/json"}, timeout=10)
    return r.status_code == 204

def send_telegram_pump(ticker_data):
    d = ticker_data
    coin = d['symbol'].replace('USDT','')
    
    msg = f"""🚨 PUMP ALERT: ${coin}

📈 +{d['change_pct']:.1f}% (24h)
💰 ${d['price']:.8f}
📊 Vol: ${d['volume']/1e6:.1f}M
🔼 ${d['high']:.8f} | 🔽 ${d['low']:.8f}

More alpha 👆"""
    
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            json={"chat_id": TELEGRAM_USER_ID, "text": msg, "parse_mode": "HTML"},
            timeout=10
        )
        return r.json().get('ok', False)
    except:
        return False

def get_top_gainers():
    """Get all Binance tickers, return top movers"""
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/24hr", timeout=15)
        if r.status_code != 200:
            return []
        
        tickers = r.json()
        gainers = []
        
        for t in tickers:
            try:
                # Only USDT pairs with enough volume
                if not t['symbol'].endswith('USDT'):
                    continue
                if t['symbol'] in ['USDCUSDT', 'BUSDUSDT', 'DAIUSDT', 'FDUSDUSDT']:
                    continue
                    
                price = float(t['lastPrice'])
                change = float(t['priceChangePercent'])
                volume = float(t['quoteVolume'])
                
                if change >= MIN_PUMP_PCT and volume >= MIN_VOLUME_USD and price > 0.00000001:
                    gainers.append({
                        'symbol': t['symbol'],
                        'price': price,
                        'change_pct': change,
                        'volume': volume,
                        'high': float(t['highPrice']),
                        'low': float(t['lowPrice']),
                        'count': int(t['count'])
                    })
            except:
                pass
        
        gainers.sort(key=lambda x: x['change_pct'], reverse=True)
        return gainers[:15]
        
    except Exception as e:
        log(f"Error fetching tickers: {e}")
        return []

def run_pump_scanner():
    """Main scan loop"""
    log("=== BINANCE PUMP SCANNER STARTED ===")
    log(f"Scanning {len(MEME_COINS)} coins every {SCAN_INTERVAL}s")
    log(f"Alerts trigger at >{MIN_PUMP_PCT}% gain + ${MIN_VOLUME_USD/1e6:.0f}M volume")
    log("Ctrl+C to stop\n")
    
    alerted = set()  # Don't spam the same pump twice
    last_report = time.time()
    
    while True:
        try:
            # Scan specific coins
            pump_candidates = []
            for symbol in MEME_COINS:
                if not symbol.endswith('USDT'):
                    s = symbol + 'USDT'
                else:
                    s = symbol
                t = binance_ticker(s)
                if t and t['change_pct'] >= MIN_PUMP_PCT and t['volume'] >= MIN_VOLUME_USD:
                    pump_candidates.append(t)
            
            # Also get top gainers across all Binance
            top_gainers = get_top_gainers()
            
            # Find new pumps (not alerted yet in last 30 min)
            new_pumps = []
            
            for t in pump_candidates:
                if t['symbol'] not in alerted:
                    new_pumps.append(t)
                    alerted.add(t['symbol'])
            
            for t in top_gainers[:5]:
                if t['symbol'] not in alerted:
                    new_pumps.append(t)
                    alerted.add(t['symbol'])
            
            # Post new pump alerts
            if new_pumps:
                log(f"🚨 {len(new_pumps)} NEW PUMP(S) DETECTED!")
                for pump in new_pumps:
                    coin = pump['symbol'].replace('USDT','')
                    log(f"  → ${coin}: +{pump['change_pct']:.1f}% | Vol ${pump['volume']/1e6:.1f}M")
                    
                    # Post to both channels
                    dc = post_discord_pump(pump)
                    tg = send_telegram_pump(pump)
                    log(f"    Discord: {'OK' if dc else 'FAIL'} | Telegram: {'OK' if tg else 'FAIL'}")
            
            # Periodic top gainers report
            if time.time() - last_report >= 300:  # Every 5 min
                top5 = get_top_gainers()[:5]
                if top5:
                    report = "📊 **TOP GAINERS (5 min update)**\n\n"
                    for t in top5:
                        coin = t['symbol'].replace('USDT','')
                        report += f"${coin}: +{t['change_pct']:.1f}%\n"
                    report += f"\n{PAYPIP_LINK}"
                    
                    requests.post(DISCORD_WEBHOOK, json={"content": report}, 
                                   headers={"Content-Type": "application/json"}, timeout=10)
                    log("Sent 5-min gainers report to Discord")
                last_report = time.time()
            
            # Cleanup old alerts after 30 min
            if len(alerted) > 100:
                alerted = set(list(alerted)[-50:])
            
            time.sleep(SCAN_INTERVAL)
            
        except KeyboardInterrupt:
            log("\nScanner stopped.")
            break
        except Exception as e:
            log(f"Error: {e}")
            time.sleep(30)

if __name__ == "__main__":
    run_pump_scanner()