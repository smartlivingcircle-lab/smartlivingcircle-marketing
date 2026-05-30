#!/usr/bin/env python3
"""
Content Generator for SmartLivingCircle
Creates viral crypto content for all channels
"""

import random
from datetime import datetime

PAYPIP_LINK = "https://payhip.com/b/1vtcL"
WALLET = "4dX3VmkGFJHj1XZbWN1MbRYnCaxYWEEN21LjkmCe9JRE"
PRODUCT = "Blockchain Technologies: How to Make Money with Flash Loans"

# Viral crypto content templates
PUMP_ALERT_TEMPLATE = """
🚀 #{ticker} PUMP ALERT

{ticker} just flashed a {signal} signal!
📈 +{gain}% in the last hour
💎 Volume: {volume}x normal

What's moving:
→ {reason}

DM for more alpha 📊
"""

EDUCATION_POST = [
    "⚡ FLASH LOANS: The secret weapon of DeFi whales\n\nMost traders don't know they exist.\nA flash loan lets you borrow ANY amount without collateral—as long as you return it in the SAME transaction.\n\nHow whales use them:\n→ Arbitrage between DEXs\n→ Collateral swaps\n→ Liquidate underwater positions\n\nMy new guide covers 7 proven flash loan strategies:\n{payhip}\n\n#DeFi #FlashLoans #Crypto #Ethereum #Web3",
    
    "💰 Why most crypto traders LOSE money\n\nNot because they're stupid.\nBecause they trade on emotion, not data.\n\nThe 3 rules of profitable trading:\n1️⃣ Cut losses fast, let winners run\n2️⃣ Never risk more than 2% per trade\n3️⃣ Use leverage ONLY when odds are in your favor\n\nI made {profit} last month following these rules.\nLearn the exact strategies:\n{payhip}\n\n#Crypto #Trading #Bitcoin #Ethereum",
    
    "🧵 What I've learned from 5 years in crypto:\n\n→ 90% of 'opportunities' are scams\n→ The best time to buy is when news is bad\n→ Dollar-cost averaging beats timing the market\n→ Flash loans can generate risk-free profits\n→ Most people will never understand DeFi\n\nMy 118-page guide covers everything I wish I knew sooner:\n{payhip}\n\nSave this. Come back to it in 2 years. #Crypto #DeFi #Web3",
    
    "🔍 How to spot a rug pull BEFORE it happens:\n\n1️⃣ Check team doxx (real names? LinkedIn?)\n2️⃣ LP locked? (Uniswap shows this)\n3️⃣ Taxing bot? (40%+ fee = red flag)\n4️⃣ Social accounts created recently?\n5️⃣ Unusual whale activity (someone dumping)\n\nThe guide I've linked covers 12 more warning signs:\n{payhip}\n\nStay safe out there 🛡️\n#Crypto #DeFi #BSC #Ethereum",
    
    "📊 THE BIGGEST CRYPTO OPPORTUNITY nobody talks about:\n\nFlash loans.\n\nYou borrow millions WITHOUT collateral.\nYou execute a trade.\nYou return the loan.\nAll in one transaction.\n\nRisk-free profit IF you know what you're doing.\n\nI wrote a complete 118-page guide on this:\n{payhip}\n\nFree to read for the next 24 hours.\n\n#Crypto #FlashLoans #Arbitrage #DeFi",
]

AIRDROP_POST = """
🎁 {$CHAIN} AIRDROP ALERT

{$CHAIN} is rewarding early adopters!

How to qualify:
→ Bridge assets to {$CHAIN}
→ Use 3+ dApps
→ Hold for 60+ days

Estimated value: ${est}
Current stage: {$stage}

Tutorial in my bio link 📱
{payhip}
\n#Airdrop #{$CHAIN} #Crypto #Web3
"""

SIGNAL_POST = """
📡 {$PAIR} SIGNAL

Direction: {direction}
Entry: ${entry}
TP: ${tp}
SL: ${sl}
Confidence: {conf}%

Risk: {risk}
Timeframe: {tf}

{reason}

Follow for more alpha 🚀
"""

def generate_pump_alert(ticker, gain, reason, volume, signal="bullish"):
    return PUMP_ALERT_TEMPLATE.format(
        ticker=ticker.upper(),
        gain=gain,
        reason=reason,
        volume=volume,
        signal=signal
    )

def get_random_education():
    post = random.choice(EDUCATION_POST)
    return post.format(payhip=PAYPIP_LINK, profit="$2,400")

def get_content_for_platform(platform):
    """Get platform-specific content"""
    base = get_random_education()
    
    if platform == "discord":
        return base
    
    elif platform == "telegram":
        # Telegram prefers shorter, emoji-heavy
        lines = base.split("\n")
        return "\n".join(l for l in lines if len(l) < 200)
    
    elif platform == "bluesky":
        # Bluesky max 300 chars
        return base[:280] + f"\n\n{payhip}"
    
    elif platform == "threads":
        return base + f"\n\n👆 Link in bio"
    
    return base

def generate_thread_prompt():
    """Generate a discussion thread for Threads"""
    threads = [
        "What's your biggest crypto mistake? I'll start: I sold my ETH at $1,800 in 2022. Still hurts.",
        "Hot take: 90% of 'DeFi influencers' have never actually used flash loans. Change my mind.",
        "If you had to start over in crypto today, what would you do first?",
        "The best DeFi strategy nobody talks about: liquidity provision on small-cap DEXs.",
        "Why I'm still bullish on Solana despite the outages.",
    ]
    topic = random.choice(threads)
    return f"""Create a casual, engaging Threads post about:

Topic: {topic}

Requirements:
- Casual, conversational tone
- End with a question to drive replies
- Include 2-3 relevant hashtags
- Keep under 500 characters
- Don't be salesy - just genuine opinion
- Add emoji where appropriate
- Include this link somewhere natural: {PAYPIP_LINK}
"""

def get_seo_post():
    """Long-form SEO content for Quora/Medium"""
    return f"""
Q: How can I make money with flash loans?

A: Flash loans are one of DeFi's most powerful (and underutilized) features. Here's how they work and how you can profit:

**What is a flash loan?**
A flash loan lets you borrow any amount of crypto WITHOUT collateral—as long as you return it within the SAME blockchain transaction.

**How to profit:**

1. **Arbitrage** - Borrow at one DEX, sell at another where price is higher, return loan, keep profit

2. **Collateral swap** - Swap your collateral from one asset to another without paying back the debt

3. **Liquidity extraction** - Exploit impermanent loss differentials

**Requirements:**
- Technical knowledge of smart contracts
- Understanding of DEXs (Uniswap, SushiSwap, PancakeSwap)
- Knowledge of gas optimization

I wrote a complete 118-page guide covering 7 proven strategies:\n{PAYPIP_LINK}

It includes step-by-step tutorials, profit calculations, and risk management.
"""

if __name__ == "__main__":
    print("=== CONTENT GENERATOR TEST ===\n")
    print("📱 Discord:")
    print(get_content_for_platform("discord")[:200] + "...")
    print("\n📱 Telegram:")
    print(get_content_for_platform("telegram")[:200] + "...")
    print("\n📱 Bluesky:")
    print(get_content_for_platform("bluesky")[:200] + "...")
    print("\n📝 SEO Post (Quora):")
    print(get_seo_post()[:500] + "...")