#!/usr/bin/env python3
"""
CryptoAlphaBot - Working Version for Railway
"""
import time
import sys
from datetime import datetime

print("=" * 50)
print("🚀 CryptoAlphaBot STARTING")
print(f"⏰ Time: {datetime.now().isoformat()}")
print("=" * 50)
sys.stdout.flush()

# Try to import requests
try:
    import requests
    print("✅ requests loaded")
    HAS_REQUESTS = True
except ImportError:
    print("⚠️ requests not found, using urllib")
    HAS_REQUESTS = False
    import urllib.request
    import json
sys.stdout.flush()

def get_price(coin='bitcoin'):
    """Get crypto price"""
    try:
        if HAS_REQUESTS:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data.get(coin, {}).get('usd', 0)
        else:
            # Fallback to urllib
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
            response = urllib.request.urlopen(url, timeout=5)
            data = json.loads(response.read().decode())
            return data.get(coin, {}).get('usd', 0)
        return 0
    except Exception as e:
        print(f"❌ Error getting {coin}: {e}")
        return 0

# Main loop - Runs forever
counter = 0
print("\n🔄 Bot is running...")
print("📊 Updates every 30 seconds")
print("=" * 50)
sys.stdout.flush()

while True:
    try:
        counter += 1
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"\n📊 [{timestamp}] Update #{counter}")
        print("-" * 40)
        
        # Get prices
        btc = get_price('bitcoin')
        eth = get_price('ethereum')
        
        print(f"💰 Bitcoin (BTC): ${btc:,.2f}")
        print(f"💰 Ethereum (ETH): ${eth:,.2f}")
        print(f"💓 Uptime: {counter * 30}s")
        print("-" * 40)
        sys.stdout.flush()
        
        time.sleep(30)
        
    except KeyboardInterrupt:
        print("\n🛑 Stopping...")
        sys.stdout.flush()
        break
    except Exception as e:
        print(f"❌ Error: {e}")
        print("🔄 Continuing...")
        sys.stdout.flush()
        time.sleep(10)
