import os

API_KEY = os.environ.get("API_KEY")
ACCOUNT_ID = os.environ.get("ACCOUNT_ID")
OANDA_URL = "https://api-fxpractice.oanda.com/v3"
SECURE_HEADER = {
    "Authorization": f"Bearer {API_KEY}",
     "Content-Type": "application/json"}
BUY = 1
SELL = -1
NONE = 0
