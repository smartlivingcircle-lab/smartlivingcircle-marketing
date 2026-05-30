#!/usr/bin/env python3
"""
Bluesky Social Poster
Posts crypto content to Bluesky
"""

import os
import sys
import random
import requests
from datetime import datetime

WORKDIR = "C:/Users/INSPIRON/smartlivingcircle-marketing"
sys.path.insert(0, WORKDIR)

# Bluesky credentials (user must provide)
BLUESKY_HANDLE = os.environ.get('BLUESKY_HANDLE', '')  # yourname.bsky.social
BLUESKY_APP_PASSWORD = os.environ.get('BLUESKY_APP_PASSWORD', '')  # App-specific password

# Product link for bio
PAYPIP_LINK = "https://payhip.com/b/1vtcL"

def get_bluesky_token():
    """Get Bluesky access token"""
    if not BLUESKY_HANDLE or not BLUESKY_APP_PASSWORD:
        return None
    
    resp = requests.post(
        "https://bsky.social/xrpc/com.atproto.server.createSession",
        json={"identifier": BLUESKY_HANDLE, "password": BLUESKY_APP_PASSWORD},
        timeout=10
    )
    if resp.status_code == 200:
        return resp.json()
    return None

def post_to_bluesky(text, token):
    """Post to Bluesky"""
    resp = requests.post(
        "https://bsky.social/xrpc/com.atproto.server.createSession",
        json={"identifier": BLUESKY_HANDLE, "password": BLUESKY_APP_PASSWORD},
        timeout=10
    )
    if resp.status_code != 200:
        print(f"Auth failed: {resp.status_code}")
        return False
    
    session = resp.json()
    access_token = session.get('accessJwt')
    
    # Create post
    post_resp = requests.post(
        "https://bsky.social/xrpc/com.atproto.server.createSession",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"text": text},
        timeout=10
    )
    # Actually post to feed
    post_resp = requests.post(
        "https://bsky.social/xrpc/com.atproto.app.bsky.feed.post",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "text": text,
            "createdAt": datetime.utcnow().isoformat() + "Z"
        },
        timeout=10
    )
    return post_resp.status_code in [200, 201]

def post_thread_to_bluesky(text, token):
    """Post a thread to Bluesky"""
    if not token:
        return False, "No token"
    
    session = get_bluesky_token()
    if not session:
        return False, "Auth failed"
    
    access_token = session.get('accessJwt')
    
    # Post the thread
    post_data = {
        "text": text,
        "createdAt": datetime.utcnow().isoformat() + "Z"
    }
    
    resp = requests.post(
        "https://bsky.social/xrpc/com.atproto.app.bsky.feed.post",
        headers={"Authorization": f"Bearer {access_token}"},
        json=post_data,
        timeout=10
    )
    
    if resp.status_code in [200, 201]:
        return True, resp.json().get('uri', 'posted')
    return False, f"Error {resp.status_code}: {resp.text[:100]}"

def run_bluesky_campaign():
    """Main campaign runner"""
    from content_generator import get_content_for_platform, get_random_education
    
    # Test if we have credentials
    session = get_bluesky_token()
    if not session:
        print("Bluesky: No credentials - skipping. Set BLUESKY_HANDLE and BLUESKY_APP_PASSWORD")
        return
    
    print(f"Bluesky: Logged in as {session.get('handle', 'unknown')}")
    
    # Generate content
    content = get_random_education()
    success, result = post_thread_to_bluesky(content, session)
    
    if success:
        print(f"Bluesky: Posted OK → {result}")
    else:
        print(f"Bluesky: Failed → {result}")

if __name__ == "__main__":
    run_bluesky_campaign()