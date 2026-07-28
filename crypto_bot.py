#!/usr/bin/env python3
"""
CryptoAlphaBot - Rock Solid Version for Railway
No crashes, always runs!
"""
import time
import sys
import traceback
from datetime import datetime

# Force unbuffered output
try:
    sys.stdout.reconfigure(line_buffering=True)
except:
    pass

def safe_print(message):
    """Safely print with timestamp"""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")
        sys.stdout.flush()
    except:
        pass

# Start with minimal logging
safe_print("=" * 50)
safe_print("🚀 CryptoAlphaBot Starting...")
safe_print("=" * 50)

# Try to import requests with fallback
try:
    import requests
    safe_print("✅ requests module loaded")
except ImportError as e:
    safe_print(f"⚠️ Import error: {e}")
    safe_print("🔄 Installing requests...")
    try:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
        import requests
        safe_print("✅ requests installed")
    except Exception as e:
        safe_print(f"❌ Failed to install requests: {e}")
        safe_print("⚠️ Continuing without requests...")
        requests = None

class CryptoAlphaBot:
    def __init__(self):
        safe_print("🔄 Initializing bot...")
        self.base_url = "https://api.coingecko.com/api/v3"
        self.session = None
        self.last_request = 0
        
        if requests:
            self.session = requests.Session()
            self.session.headers.update({
                'User-Agent': 'CryptoAlphaBot/1.0',
                'Accept': 'application/json'
            })
            safe_print("✅ Bot initialized with requests")
        else:
            safe_print("⚠️ Bot initialized without requests")
        
        self.running = True
        self.update_count = 0
    
    def get_price_simple(self, coin_id='bitcoin'):
        """Get price with built-in HTTP if requests unavailable"""
        try:
            import urllib.request
            import json
            
            url = f"{self.base_url}/simple/price?ids={coin_id}&vs_currencies=usd"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                return data.get(coin_id, {}).get('usd', 0)
        except Exception as e:
            safe_print(f"❌ Error getting price: {e}")
            return 0
    
    def get_price(self, coin_id='bitcoin'):
        """Get price using requests if available"""
        if self.session:
            try:
                # Rate limiting
                now = time.time()
                if now - self.last_request < 2:
                    time.sleep(2 - (now - self.last_request))
                self.last_request = time.time()
                
                url = f"{self.base_url}/simple/price"
                params = {'ids': coin_id, 'vs_currencies': 'usd'}
                response = self.session.get(url, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get(coin_id, {}).get('usd', 0)
                elif response.status_code == 429:
                    safe_print("⚠️ Rate limited, waiting...")
                    time.sleep(10)
                    return self.get_price(coin_id)
                else:
                    safe_print(f"⚠️ API error: {response.status_code}")
                    return 0
            except Exception as e:
                safe_print(f"❌ Request error: {e}")
                return self.get_price_simple(coin_id)  # Fallback
        else:
            return self.get_price_simple(coin_id)  # Fallback
    
    def get_prices_batch(self, coin_ids):
        """Get multiple prices"""
        if self.session:
            try:
                now = time.time()
                if now - self.last_request < 2:
                    time.sleep(2 - (now - self.last_request))
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
                safe_print(f"❌ Batch request error: {e}")
                return {}
        return {}
    
    def update(self):
        """Perform a single update"""
        try:
            self.update_count += 1
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            safe_print(f"")
            safe_print(f"📊 Update #{self.update_count} at {timestamp}")
            safe_print("-" * 40)
            
            # Get prices
            prices = self.get_prices_batch(['bitcoin', 'ethereum', 'cardano', 'solana'])
            
            btc = prices.get('bitcoin', {}).get('usd', 0)
            eth = prices.get('ethereum', {}).get('usd', 0)
            ada = prices.get('cardano', {}).get('usd', 0)
            sol = prices.get('solana', {}).get('usd', 0)
            
            safe_print(f"💰 Bitcoin (BTC): ${btc:,.2f}")
            safe_print(f"💰 Ethereum (ETH): ${eth:,.2f}")
            safe_print(f"💰 Cardano (ADA): ${ada:,.4f}")
            safe_print(f"💰 Solana (SOL): ${sol:,.2f}")
            
            safe_print("-" * 40)
            safe_print(f"✅ Update #{self.update_count} complete")
            safe_print(f"💓 Bot uptime: {self.update_count * 60}s")
            
            return True
            
        except Exception as e:
            safe_print(f"❌ Update error: {e}")
            safe_print(traceback.format_exc())
            return False
    
    def run(self):
        """Main loop - NEVER STOPS"""
        safe_print("")
        safe_print("🔄 Bot running continuously...")
        safe_print("⏱️  Updates every 60 seconds")
        safe_print("🛑 Press Ctrl+C to stop")
        safe_print("=" * 50)
        safe_print("")
        
        while self.running:
            try:
                # Perform update
                success = self.update()
                
                if not success:
                    safe_print("⚠️ Update had errors, continuing...")
                
                # Wait - THIS KEEPS IT RUNNING
                safe_print(f"💤 Sleeping for 60 seconds...")
                for i in range(60):
                    if not self.running:
                        break
                    time.sleep(1)
                
            except KeyboardInterrupt:
                safe_print("\n🛑 Stopping...")
                self.running = False
                break
            except Exception as e:
                safe_print(f"❌ Loop error: {e}")
                safe_print(traceback.format_exc())
                safe_print("🔄 Restarting loop in 10 seconds...")
                time.sleep(10)

# ===== MAIN =====
try:
    safe_print("")
    safe_print("🚀 Creating bot instance...")
    
    # Create bot
    bot = CryptoAlphaBot()
    
    # Run bot - THIS NEVER RETURNS
    bot.run()
    
    # If we get here, something went wrong
    safe_print("⚠️ Bot exited unexpectedly")
    
except Exception as e:
    safe_print(f"❌ Fatal error: {e}")
    safe_print(traceback.format_exc())

# KEEP CONTAINER ALIVE NO MATTER WHAT
safe_print("🔄 Container is still alive...")
while True:
    try:
        safe_print("💓 Heartbeat - Container running")
        time.sleep(60)
    except:
        time.sleep(60)
