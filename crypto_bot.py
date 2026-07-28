#!/usr/bin/env python3
"""
CryptoAlphaBot - Simple Crypto Price Tracker
Runs continuously on Railway
"""
import time
import sys
from datetime import datetime

# Force output immediately (important for Railway logs)
sys.stdout.reconfigure(line_buffering=True)

print("🚀 CryptoAlphaBot Starting...")
print(f"⏰ Start Time: {datetime.now().isoformat()}")
print("=" * 50)
sys.stdout.flush()

# Import requests with auto-install fallback
try:
    import requests
    print("✅ requests module loaded")
except ImportError:
    print("⚠️ Installing requests...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests
    print("✅ requests installed")
sys.stdout.flush()

class CryptoAlphaBot:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'CryptoAlphaBot/1.0',
            'Accept': 'application/json'
        })
        self.last_request = 0
        print("✅ Bot initialized successfully!")
        sys.stdout.flush()
    
    def get_price(self, coin_id='bitcoin'):
        """Get current price of a cryptocurrency"""
        try:
            # Rate limiting (avoid 429 errors)
            now = time.time()
            if now - self.last_request < 3:
                time.sleep(3 - (now - self.last_request))
            self.last_request = time.time()
            
            url = f"{self.base_url}/simple/price"
            params = {'ids': coin_id, 'vs_currencies': 'usd'}
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get(coin_id, {}).get('usd', 0)
            elif response.status_code == 429:
                print("⚠️ Rate limited, waiting...")
                time.sleep(10)
                return self.get_price(coin_id)  # Retry
            else:
                print(f"⚠️ API Error: {response.status_code}")
                return 0
                
        except Exception as e:
            print(f"❌ Error getting price: {e}")
            return 0
    
    def get_multiple_prices(self, coin_ids):
        """Get prices for multiple coins in one request"""
        try:
            now = time.time()
            if now - self.last_request < 3:
                time.sleep(3 - (now - self.last_request))
            self.last_request = time.time()
            
            url = f"{self.base_url}/simple/price"
            params = {
                'ids': ','.join(coin_ids),
                'vs_currencies': 'usd'
            }
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            return {}
        except Exception as e:
            print(f"❌ Error: {e}")
            return {}
    
    def get_top_cryptos(self, limit=5):
        """Get top cryptocurrencies by market cap"""
        try:
            now = time.time()
            if now - self.last_request < 3:
                time.sleep(3 - (now - self.last_request))
            self.last_request = time.time()
            
            url = f"{self.base_url}/coins/markets"
            params = {
                'vs_currency': 'usd',
                'order': 'market_cap_desc',
                'per_page': limit,
                'page': 1,
                'sparkline': 'false'
            }
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"❌ Error getting top cryptos: {e}")
            return []
    
    def get_global_stats(self):
        """Get global cryptocurrency market stats"""
        try:
            now = time.time()
            if now - self.last_request < 3:
                time.sleep(3 - (now - self.last_request))
            self.last_request = time.time()
            
            url = f"{self.base_url}/global"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('data', {})
            return {}
        except Exception as e:
            print(f"❌ Error getting global stats: {e}")
            return {}
    
    def display_update(self):
        """Display a single market update"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n📊 [{timestamp}] Market Update")
        print("-" * 40)
        
        # Get prices in batch
        prices = self.get_multiple_prices(['bitcoin', 'ethereum', 'cardano', 'solana'])
        
        btc = prices.get('bitcoin', {}).get('usd', 0)
        eth = prices.get('ethereum', {}).get('usd', 0)
        ada = prices.get('cardano', {}).get('usd', 0)
        sol = prices.get('solana', {}).get('usd', 0)
        
        print(f"💰 Bitcoin (BTC): ${btc:,.2f}")
        print(f"💰 Ethereum (ETH): ${eth:,.2f}")
        print(f"💰 Cardano (ADA): ${ada:,.4f}")
        print(f"💰 Solana (SOL): ${sol:,.2f}")
        
        # Get top cryptos
        top = self.get_top_cryptos(3)
        if top:
            print("\n🏆 Top 3 Cryptocurrencies:")
            for i, coin in enumerate(top, 1):
                name = coin.get('name', 'Unknown')
                symbol = coin.get('symbol', '').upper()
                price = coin.get('current_price', 0)
                change = coin.get('price_change_percentage_24h', 0)
                print(f"  {i}. {name} (${symbol}): ${price:,.2f} ({change:+.2f}%)")
        
        # Get global stats
        global_stats = self.get_global_stats()
        if global_stats:
            mcap = global_stats.get('total_market_cap', {}).get('usd', 0)
            volume = global_stats.get('total_volume', {}).get('usd', 0)
            btc_dom = global_stats.get('market_cap_percentage', {}).get('btc', 0)
            print(f"\n🌍 Global Market Cap: ${mcap:,.0f}")
            print(f"📊 24h Volume: ${volume:,.0f}")
            print(f"📊 BTC Dominance: {btc_dom:.1f}%")
        
        print("-" * 40)
        print("✅ Update complete")
        sys.stdout.flush()
    
    def run(self):
        """Main loop - RUNS FOREVER"""
        print("\n🔄 Bot is now running continuously...")
        print("📊 Updates every 60 seconds")
        print("🛑 Press Ctrl+C to stop")
        print("=" * 50)
        sys.stdout.flush()
        
        update_count = 0
        while True:  # INFINITE LOOP - keeps the bot alive
            try:
                update_count += 1
                print(f"\n📈 Update #{update_count}")
                self.display_update()
                
                # Wait 60 seconds before next update
                print(f"💤 Next update in 60 seconds...")
                time.sleep(60)
                
            except KeyboardInterrupt:
                print("\n🛑 Bot stopped by user")
                sys.stdout.flush()
                break
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                print("🔄 Restarting in 10 seconds...")
                sys.stdout.flush()
                time.sleep(10)

# Main entry point
if __name__ == "__main__":
    try:
        bot = CryptoAlphaBot()
        bot.run()  # This never returns!
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.stdout.flush()
        # Keep container alive even if bot crashes
        while True:
            print("💓 Container still alive, waiting...")
            sys.stdout.flush()
            time.sleep(60)
