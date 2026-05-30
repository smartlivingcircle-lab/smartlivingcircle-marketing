#!/usr/bin/env python3
# SmartLivingCircle Marketing Engine
# Autonomous marketing bot for DeFi ebook

import os
import random
import sqlite3
import hashlib
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'posts.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS posted
                 (platform TEXT, content_hash TEXT, posted_at TEXT, url TEXT)''')
    conn.commit()
    conn.close()

def is_posted(platform, content_hash):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT 1 FROM posted WHERE platform=? AND content_hash=?', (platform, content_hash))
    result = c.fetchone() is not None
    conn.close()
    return result

def mark_posted(platform, content_hash, url=''):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO posted VALUES (?, ?, ?, ?)',
               (platform, content_hash, datetime.utcnow().isoformat(), url))
    conn.commit()
    conn.close()

def hash_content(content):
    return hashlib.md5(content.encode()).hexdigest()

PAYHIP_LINK = "https://payhip.com/b/1vtcL"

CONTENT_POOL = [
    {
        "title": "What is a Flash Loan?",
        "body": """Ever wonder how DeFi traders make money with zero collateral?

A flash loan is a type of uncollateralized loan that must be borrowed and repaid within a SINGLE blockchain transaction.

No collateral. No credit check. Just code.

How it works:
1. Borrow asset X from a protocol like Aave
2. Do something profitable (arbitrage, liquidations, etc.)
3. Repay the loan + fees - all in one tx

The key: if you do not repay, the entire transaction reverses. No one loses money.

Most common use cases:
- Arbitrage between DEXes
- Collateral swapping
- Self-liquidation to avoid liquidation
- Governance manipulation

The trick is finding opportunities where the profit exceeds the flash loan fee (usually 0.09% on Aave).

I wrote a complete guide on flash loan strategies - 118 pages covering how flash loans work technically, finding arbitrage opportunities, real code examples, and risk management.""",
        "platforms": ["reddit", "discord", "telegram"]
    },
    {
        "title": "DeFi Arbitrage: Finding the Gaps",
        "body": """The DeFi arbitrage game is simple in theory: buy low on DEX A, sell high on DEX B, pocket the difference.

In practice? It is a speed game between bots.

But here is the thing - most retail traders do not know WHERE to look. The gaps exist in:
- Newly listed tokens with low liquidity
- Cross-chain opportunities
- Compliance arbitrage (same token different price on CEX vs DEX)

The most profitable window is usually the first 24-48 hours after a new listing.

Tools I use: DEXTools, CoinGecko for price comparison, MEV protection tools to avoid front-running.

What is your biggest challenge with DeFi arbitrage?""",
        "platforms": ["reddit", "discord", "telegram"]
    },
    {
        "title": "Why Most DeFi Newbies Lose Money",
        "body": """I have seen the same pattern repeatedly:

1. Deposit into a yield farm
2. Earn tokens
3. See earnings climb
4. Withdraw - actually lost money due to token inflation

This is called impermanent loss combined with token inflation attack.

The farms look profitable on paper. The APY numbers are huge. But the farm token is being minted faster than you are earning.

The projects with sustainable yields:
- Have real revenue (trading fees, interest)
- Do not print tokens to pay farmers
- Have lock-up periods aligning incentives

Before you deposit anywhere:
1. Check the TVL (real money committed)
2. Check token velocity (is it inflating?)
3. Check if audits passed
4. Understand the revenue model

I have a full DeFi due diligence checklist in my guide.""",
        "platforms": ["reddit", "discord", "telegram"]
    },
    {
        "title": "Smart Contract Risk: What They Do Not Tell You",
        "body": """DeFi has lost billions to smart contract bugs. Here are the real risks:

1. REENTRANCY ATTACKS (most common in older contracts)
   A contract calls back into itself before state updates

2. PRICE ORACLE MANIPULATION
   Using Uniswap price as an oracle - attacker manipulates and exploits

3. FLASH LOAN ATTACKS
   Manipulate governance tokens during vote, take out massive loans

4. LOGIC BUGS
   Integer overflows, wrong calculation order

How to protect yourself:
- Read the audit report (at least the summary)
- Check if Protocol has a bug bounty
- Start with small amounts
- Use protocols with multi-sig admin keys""",
        "platforms": ["reddit", "discord", "telegram"]
    },
    {
        "title": "The Simplest DeFi Strategy That Actually Works",
        "body": """Forget the complex strategies. Here is what works for most people:

LIQUIDITY PROVISIONING with capital you can afford to lose.

Pick a stable pair like USDC/USDT on Curve or Uniswap v3 with concentrated liquidity in the stable range.

Why it works:
- Earn trading fees (not token rewards)
- If both assets stay stable in price, you keep the fees
- No impermanent loss if prices stay equal

The risk:
- If one asset depegs, you could lose more than fees
- Smart contract risk
- Non-permanent means it is very much permanent in a crash

Best practices:
- Use protocols with $100M+ TVL (harder to exploit)
- Never provide more than 10% of your portfolio""",
        "platforms": ["reddit", "discord", "telegram"]
    },
    {
        "title": "How to Find Safe Yield",
        "body": """High APY = High risk. Here is how to evaluate:

RED FLAGS:
- APY over 1000%
- No clear revenue source
- Anonymous team
- No audits

GREEN FLAGS:
- APY 5-30% from real fees
- Public team
- Multiple audits
- TVL over $50M
- Governance token with actual utility

Where I look for safe yield:
- Aave (stablecoin lending): 5-10%
- Curve (stable LPs): 3-8%
- Compound: 3-5%
- Lido ETH staking: 4-5%

When a protocol offers 100%+ APY, they are paying you in their token. When that token dumps 50%, you are underwater.""",
        "platforms": ["reddit", "discord", "telegram"]
    },
]

CTA = """

---

I am the author of 'Blockchain Technologies: How to Make Money with Flash Loans' - a 118-page guide covering flash loan mechanics, finding DeFi arbitrage opportunities, smart contract risk assessment, and building a DeFi strategy from scratch.

Get it here: {link}

(Not financial advice)
"""

def get_cta():
    return CTA.format(link=PAYHIP_LINK)

def format_for_reddit(post):
    body = post['body']
    if len(body) > 8000:
        body = body[:7900] + "..."
    return "**" + post['title'] + "**\n\n" + body + get_cta()

def format_for_discord(post):
    body = post['body'][:600] + "..." if len(post['body']) > 600 else post['body']
    cta = "\n\n---\n" + post['title'] + " - Full Guide: " + PAYHIP_LINK
    return body + cta

def format_for_telegram(post):
    body = post['body'][:500] + "..." if len(post['body']) > 500 else post['body']
    cta = "\n\nFull guide: " + PAYHIP_LINK
    return body + cta

def get_unposted_content(platform):
    for post in CONTENT_POOL:
        h = hash_content(post['title'])
        if not is_posted(platform, h) and platform in post['platforms']:
            return post
    # If all posted, reset tracking and pick random
    post = random.choice(CONTENT_POOL)
    return post

if __name__ == "__main__":
    init_db()
    print("SmartLivingCircle Marketing Engine loaded")
    print(f"Content items: {len(CONTENT_POOL)}")