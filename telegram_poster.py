#!/usr/bin/env python3
"""
Telegram Marketing Bot
Posts DeFi content to Telegram groups/channels
Uses python-telegram-bot v20+ (async)
"""

import os
import sys
import json
import random
import asyncio
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import PAYHIP_LINK, PRODUCT_NAME

BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '8889649869:AAFD9DiTckmtHn3lBqzAPmyjP7__aLYyR9o')
TARGETS = []  # Add chat IDs here: [-1001234567890] or [123456789]

# Content library - rotating DeFi/crypto posts
POSTS = [
    {
        "title": "🔓 What is a Flash Loan?",
        "body": "A flash loan lets you borrow ANY amount without collateral - as long as you return it in the SAME transaction.\n\nNo collateral. No KYC. Just pure DeFi logic.\n\nBook I read to understand this: {link}",
        "emoji": "💰",
        "hashtags": "#DeFi #FlashLoan #Crypto #Blockchain"
    },
    {
        "title": "⚖️ Arbitrage in DeFi",
        "body": "Price differences between DEXes = free money for those who move fast.\n\nAutomated arbitrage bots scan multiple exchanges simultaneously and execute trades in milliseconds.\n\nThis is how serious DeFi traders make consistent gains.",
        "emoji": "📊",
        "hashtags": "#DeFi #Arbitrage #CryptoTrading #Blockchain"
    },
    {
        "title": "🛡️ Smart Contract Security",
        "body": "Before investing in any DeFi protocol:\n\n1. Check audit from CertiK or Hacken\n2. Verify contract on Etherscan\n3. Start with small amounts\n\nDon't trust. Verify.",
        "emoji": "🔍",
        "hashtags": "#DeFi #SmartContracts #Security #Crypto"
    },
    {
        "title": "💡 LP Tokens Explained",
        "body": "When you provide liquidity to a DEX, you get LP tokens.\n\nThese represent your share of the pool.\n\nYield farms reward you with extra tokens for staking LP.\n\nBut impermanent loss is real - know the risks.",
        "emoji": "📈",
        "hashtags": "#DeFi #LiquidityPool #YieldFarming #Crypto"
    },
    {
        "title": "🔗 Cross-Chain DeFi",
        "body": "The future is multi-chain.\n\nBridge assets to access:\n- Higher yields\n- Exclusive pools\n- Lower fees\n\nLayerZero, Wormhole, and Synapse make cross-chain DeFi accessible to everyone.",
        "emoji": "🌉",
        "hashtags": "#DeFi #CrossChain #LayerZero #Crypto"
    },
    {
        "title": "📚 My DeFi Reading List",
        "body": "Start here if you want to understand DeFi properly:\n\nBlockchain Technologies: How to Make Money with Flash Loans\n\n118 pages covering:\n• Flash loan mechanics\n• Arbitrage strategies\n• Smart contract fundamentals\n\n{link}",
        "emoji": "📖",
        "hashtags": "#DeFi #FlashLoan #CryptoEducation #Blockchain"
    },
]

def get_post():
    post = random.choice(POSTS)
    text = f"{post['emoji']} *{post['title']}*\n\n{post['body'].format(link=PAYHIP_LINK)}\n\n{post['hashtags']}"
    return text

async def send_telegram_message(chat_id, text):
    """Send a message to a Telegram chat"""
    try:
        from telegram import Bot
        bot = Bot(token=BOT_TOKEN)
        await bot.send_message(chat_id=chat_id, text=text, parse_mode='Markdown')
        print(f"  Sent to {chat_id}")
        return True
    except Exception as e:
        print(f"  Error to {chat_id}: {e}")
        return False

async def run_telegram_campaign():
    """Main campaign runner"""
    print("=" * 50)
    print("Telegram Marketing Campaign")
    print("=" * 50)
    
    if not BOT_TOKEN or BOT_TOKEN == 'YOUR_TELEGRAM_BOT_TOKEN':
        print("TELEGRAM BOT TOKEN NOT SET - skipping")
        return
    
    if not TARGETS:
        print("No Telegram targets configured - skipping")
        print("Add chat IDs to TELEGRAM_TARGETS in config.py")
        print("Note: Bot must be admin/member of the channel/group")
        return
    
    post_text = get_post()
    print(f"\nPost: {post_text[:80]}...")
    
    success = 0
    for target in TARGETS:
        if await send_telegram_message(target, post_text):
            success += 1
    
    print(f"\nSent to {success}/{len(TARGETS)} Telegram chats")

def run_telegram_campaign_sync():
    """Sync wrapper"""
    try:
        asyncio.run(run_telegram_campaign())
    except KeyboardInterrupt:
        print("\nInterrupted")

if __name__ == "__main__":
    run_telegram_campaign_sync()