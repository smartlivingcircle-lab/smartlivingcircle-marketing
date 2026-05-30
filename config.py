# SmartLivingCircle Marketing Config
# All secrets via environment variables only - DO NOT hardcode secrets here

import os

PAYPAL_EMAIL = "smartlivingcircle@gmail.com"
PAYHIP_LINK = "https://payhip.com/b/1vtcL"
PRODUCT_NAME = "Blockchain Technologies: How to Make Money with Flash Loans"

# Reddit OAuth credentials
# Get them at: https://www.reddit.com/prefs/apps
# Set as environment variables:
#   export REDDIT_CLIENT_ID="your_client_id"
#   export REDDIT_CLIENT_SECRET="your_client_secret"
#   export REDDIT_USERNAME="your_username"
#   export REDDIT_PASSWORD="your_password"

# Discord webhook URLs (no auth needed)
# Right-click channel -> Edit Channel -> Integrations -> Create Webhook
DISCORD_WEBHOOKS = [
    "https://discord.com/api/webhooks/1510211779924463748/kg-TcdfPw5e-dqCF7-9MuN6xZlReHsWZjoXKNwXn8UjChG7BBx3jvpEOBtoKPL6UHngC",
]

# Permanent Discord invite link
DISCORD_INVITE = "https://discord.gg/YSc6tUuSaD"

# Telegram bot token and targets
# Get bot token from @BotFather on Telegram
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '8889649869:AAFD9DiTckmtHn3lBqzAPmyjP7__aLYyR9o')
TELEGRAM_TARGETS = []

# Posting schedule (cron format)
REDDIT_POST_SCHEDULE = "0 */6 * * *"
DISCORD_POST_SCHEDULE = "0 */4 * * *"
TELEGRAM_POST_SCHEDULE = "0 */3 * * *"

MIN_POST_INTERVAL_HOURS = 4