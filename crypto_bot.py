import time
import sys
from datetime import datetime
import requests
import json

print("🚀 CryptoAlphaBot Starting...")
print(f"⏰ Start time: {datetime.now().isoformat()}")
print("=" * 50)
sys.stdout.flush()

class CryptoAlphaBot:
    """Simple cryptocurrency bot for Railway"""
    
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'CryptoAlphaBot/1.0',
            'Accept': 'application/json'
        })
        print("✅ Bot initialized successfully!")
        sys.stdout.flush()
    
    def get_price(self, coin_id='bitcoin'):
        """Get current price"""
        try:
            url = f"{self.base_url}/simple/price"
            params = {'ids': coin_id, 'vs_currencies': 'usd'}
            response = self.session.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get(coin_id, {}).get('usd', 0)
            return 0
        except Exception as e:
            print(f"❌ Error getting price: {e}")
            return 0
    
    def run(self):
        """Main loop - keeps bot alive"""
        print("🔄 Bot is now running continuously...")
        print("📊 Updates every 30 seconds")
        print("=" * 50)
        sys.stdout.flush()
        
        counter = 0
        while True:
            try:
                counter += 1
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Get Bitcoin price
                btc_price = self.get_price('bitcoin')
                eth_price = self.get_price('ethereum')
                
                print(f"\n[{timestamp}] 📊 Update #{counter}")
                print(f"💰 Bitcoin (BTC): ${btc_price:,.2f}")
                print(f"💰 Ethereum (ETH): ${eth_price:,.2f}")
                print(f"💓 Bot is alive (Uptime: {counter * 30}s)")
                print("-" * 40)
                sys.stdout.flush()
                
                # Wait 30 seconds before next update
                time.sleep(30)
                
            except KeyboardInterrupt:
                print("\n🛑 Bot stopped by user")
                sys.stdout.flush()
                break
            except Exception as e:
                print(f"❌ Error in main loop: {e}")
                print("🔄 Restarting loop in 10 seconds...")
                sys.stdout.flush()
                time.sleep(10)

# Run the bot
if __name__ == "__main__":
    try:
        bot = CryptoAlphaBot()
        bot.run()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.stdout.flush()
        # Keep the container alive even on error
        while True:
            print("🔄 Container still alive...")
            sys.stdout.flush()
            time.sleep(60)
