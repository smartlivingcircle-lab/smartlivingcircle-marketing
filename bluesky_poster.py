#!/usr/bin/env python3
"""
Bluesky Social Poster
"""

import os, sys, requests
from datetime import datetime

PAYPIP_LINK = "https://payhip.com/b/1vtcL"
BLUESKY_HANDLE = "smartlivingcircle.bsky.social"
BLUESKY_APP_PASSWORD = "p2r7-cb7g-ffj2-6i3s"

def get_session():
    r = requests.post(
        "https://bsky.social/xrpc/com.atproto.server.createSession",
        json={"identifier": BLUESKY_HANDLE, "password": BLUESKY_APP_PASSWORD},
        timeout=10
    )
    if r.status_code == 200:
        return r.json()
    return None

def post_text(text):
    sess = get_session()
    if not sess:
        print("Auth failed")
        return False
    r = requests.post(
        "https://bsky.social/xrpc/com.atproto.app.bsky.feed.post",
        headers={"Authorization": f"Bearer {sess['accessJwt']}"},
        json={"text": text, "createdAt": datetime.utcnow().isoformat() + "Z"},
        timeout=10
    )
    return r.status_code in [200, 201], r.status_code, r.text[:200]

def test():
    print(f"Testing Bluesky login as {BLUESKY_HANDLE}...")
    sess = get_session()
    if sess:
        print(f"✅ Auth OK — did={sess.get('did','')[:30]}...")
        # Post a test
        test_post = """🚀 Just set up automated crypto alerts!

Following DeFi signals, pump alerts, and trading education.

What's your biggest crypto mistake? Drop it below 👇

#Crypto #DeFi #Web3"""
        ok, code, resp = post_text(test_post)
        if ok:
            print(f"✅ First post OK")
        else:
            print(f"Post failed: {code} {resp}")
    else:
        print("❌ Auth failed")

if __name__ == "__main__":
    test()