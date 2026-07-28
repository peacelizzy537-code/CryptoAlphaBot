#!/usr/bin/env python3
"""
CryptoAlphaBot - FORCED START
"""
import time
import sys
from datetime import datetime

# FORCE output immediately
print("=" * 60)
print("🚀 CRYPTOALPHABOT IS STARTING NOW!")
print("=" * 60)
sys.stdout.flush()
sys.stderr.flush()

# Import with immediate feedback
try:
    print("📥 Importing requests...")
    sys.stdout.flush()
    import requests
    print("✅ Requests imported successfully!")
    sys.stdout.flush()
except Exception as e:
    print(f"❌ Failed to import requests: {e}")
    print("🔄 Installing requests...")
    sys.stdout.flush()
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests
    print("✅ Requests installed and imported!")
    sys.stdout.flush()

class CryptoAlphaBot:
    def __init__(self):
        print("🏗️ Initializing bot...")
        sys.stdout.flush()
        self.base_url = "https://api.coingecko.com/api/v3"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'CryptoAlphaBot/1.0'
        })
        print("✅ Bot initialized!")
        sys.stdout.flush()
    
    def get_price(self, coin='bitcoin'):
        """Get crypto price"""
        try:
            print(f"🔄 Fetching {coin} price...")
            sys.stdout.flush()
            
            url = f"{self.base_url}/simple/price"
            params = {'ids': coin, 'vs_currencies': 'usd'}
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                price = data.get(coin, {}).get('usd', 0)
                print(f"✅ {coin} price: ${price:,.2f}")
                sys.stdout.flush()
                return price
            else:
                print(f"❌ API error: {response.status_code}")
                sys.stdout.flush()
                return 0
        except Exception as e:
            print(f"❌ Error fetching {coin}: {e}")
            sys.stdout.flush()
            return 0
    
    def run(self):
        """Main loop - IMMEDIATELY STARTS"""
        print("=" * 60)
        print("🔄 BOT IS NOW RUNNING!")
        print("📊 Updates every 60 seconds")
        print("=" * 60)
        sys.stdout.flush()
        
        update_count = 0
        
        # DO FIRST UPDATE IMMEDIATELY - NO WAITING
        print("\n⏰ Running first update IMMEDIATELY...")
        sys.stdout.flush()
        
        while True:  # INFINITE LOOP
            try:
                update_count += 1
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                print(f"\n📊 [{timestamp}] UPDATE #{update_count}")
                print("-" * 40)
                sys.stdout.flush()
                
                # Get prices
                btc = self.get_price('bitcoin')
                eth = self.get_price('ethereum')
                
                print(f"💰 Bitcoin (BTC): ${btc:,.2f}")
                print(f"💰 Ethereum (ETH): ${eth:,.2f}")
                print(f"⏱️  Uptime: {update_count * 60}s")
                print("-" * 40)
                print(f"💤 Next update in 60 seconds...")
                print("=" * 60)
                sys.stdout.flush()
                
                # Wait 60 seconds
                time.sleep(60)
                
            except KeyboardInterrupt:
                print("\n🛑 Bot stopped by user")
                sys.stdout.flush()
                break
            except Exception as e:
                print(f"❌ Error in loop: {e}")
                print("🔄 Continuing...")
                sys.stdout.flush()
                time.sleep(10)

# ===== MAIN - IMMEDIATE EXECUTION =====
print("\n🎯 Starting main() function...")
sys.stdout.flush()

if __name__ == "__main__":
    print("✅ __main__ block executing!")
    sys.stdout.flush()
    
    try:
        print("🚀 Creating bot instance...")
        sys.stdout.flush()
        
        bot = CryptoAlphaBot()
        
        print("▶️ Starting bot.run()...")
        sys.stdout.flush()
        
        # THIS NEVER RETURNS
        bot.run()
        
        print("⚠️ WARNING: bot.run() returned! This should never happen!")
        sys.stdout.flush()
        
    except Exception as e:
        print(f"❌ FATAL ERROR: {e}")
        print("🔄 Keeping container alive...")
        sys.stdout.flush()
        
        # Keep container alive
        while True:
            print("💓 Container still alive")
            sys.stdout.flush()
            time.sleep(60)
