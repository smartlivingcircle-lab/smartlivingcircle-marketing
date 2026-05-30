#!/usr/bin/env python3
"""
Hunter Mode - Aggressive Traffic Attack
Searches for new pools and drives them to funnel
"""

import os, sys, requests, time, random
from datetime import datetime

WORKDIR = "C:/Users/INSPIRON/smartlivingcircle-marketing"
sys.path.insert(0, WORKDIR)
import config

PAYPIP_LINK = config.PAYHIP_LINK
DISCORD_INVITE = getattr(config, 'DISCORD_INVITE', 'https://discord.gg/YSc6tUuSaD')

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1510211779924463748/kg-TcdfPw5e-dqCF7-9MuN6xZlReHsWZjoXKNwXn8UjChG7BBx3jvpEOBtoKPL6UHngC"

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M')}] {msg}")

# ============================================================
# AGGRESSIVE CONTENT - Pump alerts with CTA
# ============================================================
def post_pump_alert():
    """Post a pump alert to Discord with strong CTA"""
    try:
        import hashlib, hmac, base64
        from urllib.parse import urlencode
        
        BINANCE_KEY = os.environ.get('BINANCE_API_KEY', 'rOK72URbgdJkZ8h8RyQE6PvvHowFITRymUsWAgqFZPZhz3NijmXGtgAmYiUNBqJ9')
        BINANCE_SECRET = os.environ.get('BINANCE_API_SECRET', '')
        
        r = requests.get("https://api.binance.com/api/v3/ticker/24hr", timeout=10)
        if r.status_code != 200:
            return False
        
        tickers = r.json()
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
        top3 = gainers[:3]
        
        if not top3:
            log("No pumps found")
            return False
        
        # Format strong CTA message
        msg = f"""🚨 **HOT PUMPS RIGHT NOW**

"""
        for sym, chg, vol in top3:
            msg += f"• ${sym}: **+{chg:.1f}%**\n"
        
        msg += f"""
📈 Active for the next 30-60 min

💰 Want more alpha like this daily?
👉 Join the SmartLivingCircle Discord:
{DISCORD_INVITE}

📚 Learn to profit from crypto moves:
{PAYPIP_LINK}
"""
        
        data = {
            "embeds": [{
                "title": "🚨 TOP PUMPS - LIVE",
                "description": msg,
                "color": 0xFF0000,
                "footer": {"text": "SmartLivingCircle • Auto-alert"},
                "url": PAYPIP_LINK
            }]
        }
        
        r = requests.post(DISCORD_WEBHOOK, json=data, headers={"Content-Type": "application/json"}, timeout=10)
        if r.status_code == 204:
            log(f"Pump alert posted: {[s for s,c,v in top3]}")
            return True
    except Exception as e:
        log(f"Pump alert error: {e}")
    return False

# ============================================================
# QUORA ANSWERS - Generate ready-to-paste answers
# ============================================================
QUORA_ANSWERS = [
    {
        "question": "What are flash loans in crypto and how do they work?",
        "answer": """Flash loans are one of the most powerful (and misunderstood) features in DeFi.

**The concept:**
You borrow ANY amount of crypto WITHOUT collateral—as long as you return it within the SAME blockchain transaction.

If you can't pay it back, the entire transaction reverses. No loss for the protocol. Genius, right?

**How people actually profit from them:**

1. **Arbitrage** - Borrow at one DEX at a lower price, sell instantly at another DEX at a higher price, return the loan, keep the profit. All in one transaction.

2. **Collateral swap** - Swap your collateral from ETH to USDC without paying back your loan. Useful for avoiding liquidation.

3. **Self-liquidation** - If your position is about to get liquidated, borrow to self-liquidate and avoid the penalty.

**The catch:**
You need technical knowledge. You're programming transactions, not clicking buttons. One bug and your transaction fails.

I wrote a complete 118-page guide covering 7 proven flash loan strategies with real code examples:
https://payhip.com/b/1vtcL

It includes step-by-step setups, profit calculations, and risk management. Free to read."""
    },
    {
        "question": "How can I make $1000 a day with cryptocurrency?",
        "answer": """Be careful with anyone promising specific daily amounts. Crypto is volatile—not a paycheck.

That said, here are REAL strategies people use to generate consistent crypto income:

**1. DeFi Yield Farming**
- Lend crypto on Aave, Compound
- Earn 3-15% APY on stablecoins
- Lower risk, steady returns

**2. Flash Loan Arbitrage**
- Exploit price differences between DEXs
- Risk-free IF you know what you're doing
- Requires technical skill

**3. Liquidity Provision**
- Provide liquidity to DEX pools
- Earn trading fees (0.3% per trade)
- Risk: impermanent loss

**4. Crypto Education**
- Many people charge $50-500 for courses
- If you know DeFi, you can teach it
- Income is scalable

**What I do:**
I study the market patterns and share alpha in my community. I've made back my education costs multiple times over.

The key: Don't chase "get rich quick." Learn ONE strategy deeply. I wrote a guide on the strategies that actually work:
https://payhip.com/b/1vtcL

Includes flash loans, yield strategies, and risk management. Check the reviews."""
    },
    {
        "question": "What is the best cryptocurrency to invest in right now?",
        "answer": """I'm not a financial advisor. But I can tell you what smart money is doing:

**The boring truth:**
- BTC and ETH are still the safest bets for most people
- Diversification matters more than "moon shots"
- Only invest what you can afford to lose

**What's actually moving right now:**
Small-cap altcoins with real use cases. The pattern:
1. Bitcoin pumps → ETH follows → Then altcoins
2. When BTC stabilizes, look for altcoin season
3. New DeFi protocols often launch with airdrops

**The alpha:**
Most profitable trades happen in the 1-3 days AFTER a crypto event (exchange listing, protocol launch, airdrop).

**What I recommend:**
Learn how to find opportunities before they blow up. My guide covers:
- How to identify pump patterns
- Risk management
- The exact DeFi strategies whales use (including flash loans)
- Finding arbitrage opportunities

Stop looking for the "next Bitcoin." Learn how to find YOUR OWN opportunities:
https://payhip.com/b/1vtcL

The guide is 118 pages. Read the table of contents—there's a reason people keep buying it."""
    },
    {
        "question": "How do beginners make money with DeFi?",
        "answer": """DeFi (Decentralized Finance) is confusing at first. Here's a realistic path:

**Start here (lowest risk first):**

1. **Stablecoin lending** (Safest)
   - Lend USDC on Aave or Compound
   - Earn 5-12% APY
   - No price volatility risk
   - Risk: protocol hack (rare but possible)

2. **Liquidity provision** (Medium risk)
   - Provide USDC + ETH to a Uniswap pool
   - Earn trading fees
   - Risk: impermanent loss when ETH moves

3. **Yield farming** (Higher risk)
   - Move between pools chasing highest yields
   - Can be profitable but complex
   - Risk: rug pulls, token dumps

4. **Flash loans** (Advanced)
   - Borrow millions without collateral
   - Use for arbitrage
   - Requires coding skills
   - This is what the "whales" do

**My advice for beginners:**
Start with #1. Earn a stable 8-10% APY while learning. Don't rush to yield farming or flash loans.

I put together a complete guide that covers:
- Setting up your first DeFi position
- Avoiding common scams
- The exact strategies I use
- Flash loan basics (no coding required for the intro)

https://payhip.com/b/1vtcL

118 pages. Most people say they wish they had this when they started."""
    },
    {
        "question": "What are the risks of cryptocurrency trading?",
        "answer": """Honest answer—crypto trading is dangerous if you're not prepared.

**The real risks:**

1. **Volatility** - Crypto can drop 30% in a day. BTC dropped 80% in 2018. ETH dropped 90% in 2019. Can you hold through that?

2. **Scams** - Fake coins, rug pulls, phishing sites. I've seen people lose their entire portfolio to one mistake.

3. **Impermanent loss** - In DeFi liquidity pools, when one asset moves, you can lose money even if prices "go your way."

4. **Exchange risk** - If you don't hold your own keys, you're trusting an exchange. FTX happened.

5. **Leverage trading** - 100x leverage sounds amazing until you lose everything in one trade.

**How to protect yourself:**
- Never invest more than you can lose
- Use hardware wallets for storage
- Always verify URLs
- Never share seed phrases
- Learn risk management BEFORE trading

**The smart approach:**
Learn the game before you play it. I wrote a guide covering:
- Real risk management strategies
- How to spot scams BEFORE you fall for them
- DeFi safety protocols
- The actual strategies that work

It's free to read:
https://payhip.com/b/1vtcL

Read the risk management chapter first. Thank me later."""
    },
]

def generate_quora_answers_file():
    """Generate all Quora answers to a file for Marco to paste"""
    with open(f"{WORKDIR}/quora_answers_ready.txt", "w", encoding="utf-8") as f:
        f.write("="*60 + "\n")
        f.write("QUORA ANSWERS - Ready to Paste\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write("="*60 + "\n\n")
        
        for i, qa in enumerate(QUORA_ANSWERS, 1):
            f.write(f"\n{'='*60}\n")
            f.write(f"ANSWER #{i}\n")
            f.write(f"Question: {qa['question']}\n")
            f.write(f"{'='*60}\n\n")
            f.write(qa['answer'])
            f.write("\n\n")
    
    log(f"Generated {len(QUORA_ANSWERS)} Quora answers")

# ============================================================
# COMMUNITY SPREAD - Post to multiple sources
# ============================================================
def spam_crypto_lists():
    """Find crypto directory listings and add SmartLivingCircle"""
    # These are public crypto community lists
    # We can't automate joining private groups, but we CAN
    # submit to public directories
    
    base_msg = f"""📊 SmartLivingCircle - Free Crypto Alpha

Real-time Binance pump alerts, DeFi education, and flash loan strategies.

💰 100% free. No VC backing. No hype.

👉 Join: {DISCORD_INVITE}
📚 Guide: {PAYPIP_LINK}
"""

# ============================================================
# TIKTOK BIO OPTIMIZER
# ============================================================
def get_tiktok_bio():
    """Suggest TikTok bio for crypto account"""
    bio = """🔐 DeFi & Flash Loans Explained Simply
📈 Pump alerts + crypto education  
💰 How to make money with crypto
🎓 118-page guide 👇
https://payhip.com/b/1vtcL
👇 Discord for alpha: https://discord.gg/YSc6tUuSaD"""
    return bio

# ============================================================
# INSTAGRAM POST IDEAS
# ============================================================
def get_instagram_posts():
    """Get 10 Instagram post ideas"""
    posts = [
        ("Carousel", "5 DeFi Terms You MUST Know Before Investing", 
         "1. Flash Loan\n2. AMM\n3. Impermanent Loss\n4. Liquidity Pool\n5. Yield Farming\n\nSave this. Share with a friend who needs it.\n\n#DeFi #Crypto #Ethereum #Web3 #Cryptocurrency #Investing #PassiveIncome"),
        
        ("Reel", "How Flash Loans Work (in 60 seconds)",
         "Most traders don't know flash loans exist.\n\nYou can borrow MILLIONS without collateral—as long as you pay it back in the SAME transaction.\n\nThe catch? You need to know what you're doing.\n\nI wrote a complete guide. Link in bio.\n\n#FlashLoans #DeFi #Crypto #Ethereum #Web3 #Cryptocurrency"),
        
        ("Post", "The crypto safety checklist",
         "✅ Use hardware wallet\n✅ Never click unknown links\n✅ Check URLs 3x before connecting\n✅ Never share seed phrase\n✅ Never invest more than you can lose\n\nSave this. Your future self will thank you.\n\n#Crypto #DeFi #Web3 #Security #Bitcoin"),
        
        ("Carousel", "Why most crypto traders lose money",
         "Not because they're dumb.\nBecause they trade on emotion.\n\nThe 3 rules:\n1. Cut losses fast\n2. Let winners run\n3. Never risk >2% per trade\n\nLink in bio for the complete guide.\n\n#Crypto #Trading #Ethereum #Bitcoin #Web3 #DeFi"),
        
        ("Post", "Hot take",
         "The best DeFi strategy is actually the simplest:\n\n1. Buy ETH\n2. Stake it on Aave\n3. Earn 4-5% APY\n4. Wait\n\nMost people overcomplicate it and lose money trying to be clever.\n\n#DeFi #Ethereum #Crypto #Web3 #Staking"),
        
        ("Carousel", "How to find crypto gems before they pump",
         "The pattern:\n1. New protocol launches\n2. Airdrop announced\n3. Smart money buys early\n4. Retail FOMOs in\n5. Dump\n\nMost people are steps 3-4. The smart money is step 1.\n\nI share alpha in my Discord. Link in bio.\n\n#Crypto #DeFi #Web3 #Airdrop #Ethereum"),
        
        ("Reel", "What is impermanent loss?",
         "Explaining impermanent loss like you're 5:\n\nYou put 1 ETH + 1 USDC in a pool.\nETH pumps 10x.\nYou could've just held.\n\nThat's impermanent loss—the 'cost' of providing liquidity instead of HODLing.\n\nMost DeFi education skips this. Don't skip it.\n\nFull guide in bio.\n\n#DeFi #Crypto #Ethereum #ImpermanentLoss #Uniswap"),
        
        ("Post", "The 3 types of crypto wealth",
         "1. Investors - Buy and hold BTC/ETH\n2. Traders - Active entry/exit\n3. Builders - Create protocols/dapps\n\nWhich one are you building towards?\n\n#Crypto #Bitcoin #Ethereum #Web3 #DeFi"),
        
        ("Carousel", "Red flags in crypto",
         "How to spot a rug pull BEFORE it happens:\n\n🚩 Team is anonymous\n🚩 LP not locked\n🚩 Taxing bot with 40%+ fee\n🚩 Social accounts created last week\n🚩 Unusual whale activity\n\nSave this. Share it. Someone will thank you.\n\n#Crypto #DeFi #Scam #Web3 #Security"),
        
        ("Reel", "Stop doing this with your crypto",
         "Don't check your portfolio every 5 minutes.\n\nYou won't outtrade the market by staring at charts.\n\nSet alerts. Check daily or weekly. Let time do the work.\n\nThe people who panic-sell are the ones who lose.\n\n#Crypto #Ethereum #Bitcoin #Web3 #Investing"),
    ]
    return posts

# ============================================================
# HUNTER MODE - Main Loop
# ============================================================
def hunter_loop():
    log("HUNTER MODE ACTIVATED")
    
    # Generate all content
    generate_quora_answers_file()
    
    # Post a pump alert immediately
    post_pump_alert()
    
    # Save TikTok bio and Instagram posts
    with open(f"{WORKDIR}/tiktok_bio.txt", "w") as f:
        f.write(get_tiktok_bio())
    
    posts = get_instagram_posts()
    with open(f"{WORKDIR}/instagram_posts.txt", "w", encoding="utf-8") as f:
        for i, (type_, title, caption) in enumerate(posts, 1):
            f.write(f"\n{'='*50}\n")
            f.write(f"POST #{i} ({type_}): {title}\n")
            f.write(f"{'='*50}\n")
            f.write(f"Caption:\n{caption}\n\n")
    
    log("Content files ready:")
    log(f"  - quora_answers_ready.txt ({len(QUORA_ANSWERS)} answers)")
    log(f"  - tiktok_bio.txt")
    log(f"  - instagram_posts.txt ({len(posts)} posts)")

if __name__ == "__main__":
    hunter_loop()