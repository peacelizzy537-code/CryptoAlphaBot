#!/usr/bin/env python3
"""
CryptoAlphaBot - Working Version
"""
import time
import sys
from datetime import datetime

print("=" * 50)
print("🚀 CryptoAlphaBot STARTING")
print(f"⏰ Time: {datetime.now().isoformat()}")
print("=" * 50)
sys.stdout.flush()

# Try to import requests, install if not available
try:
    import requests
    print("✅ requests loaded")
except ImportError:
    print("⚠️ Installing requests...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests
    print("✅ requests installed and loaded")

def get_price(coin='bitcoin'):
    """Get crypto price"""
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get(coin, {}).get('usd', 0)
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return 0

print("\n🔄 Bot is running...")
print("📊 Updates every 30 seconds")
print("=" * 50)
sys.stdout.flush()

counter = 0
while True:
    try:
        counter += 1
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"\n📊 [{timestamp}] Update #{counter}")
        print("-" * 40)
        
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
        sys.stdout.flush()
        time.sleep(10)
