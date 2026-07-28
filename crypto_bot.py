#!/usr/bin/env python3
"""
CryptoAlphaBot - Optimized for Railway
"""
import time
import sys
import os
import json
import threading
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True)

# Configuration
UPDATE_INTERVAL = 60  # seconds between updates
HEALTH_PORT = 8080    # Port for health checks

def log(message, level="INFO"):
    """Unified logging"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")
    sys.stdout.flush()

log("🚀 CryptoAlphaBot Starting...")
log(f"📁 Directory: {os.getcwd()}")
log(f"📄 Files: {os.listdir('.')}")

try:
    import requests
    log("✅ requests module loaded")
except ImportError as e:
    log(f"❌ requests not found: {e}", "ERROR")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests
    log("✅ requests installed")

class HealthCheckHandler(BaseHTTPRequestHandler):
    """Simple health check endpoint for Railway"""
    def do_GET(self):
        if self.path == '/health' or self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'uptime': str(datetime.now() - bot_start_time) if 'bot_start_time' in globals() else 'N/A'
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

class CryptoAlphaBot:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'CryptoAlphaBot/1.0',
            'Accept': 'application/json'
        })
        self.last_request_time = 0
        self.min_interval = 5  # Minimum seconds between requests
        self.cache = {}
        self.cache_timeout = 120  # Cache for 2 minutes
        log("✅ Bot initialized")
    
    def _rate_limit(self):
        """Rate limiting to avoid 429 errors"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_interval:
            time.sleep(self.min_interval - time_since_last)
        self.last_request_time = time.time()
    
    def _make_request(self, url, params=None, retries=3):
        """Make API request with rate limiting and retries"""
        self._rate_limit()
        
        # Check cache
        cache_key = f"{url}{str(params)}"
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_timeout:
                return cached_data
        
        for attempt in range(retries):
            try:
                response = self.session.get(url, params=params, timeout=10)
                
                if response.status_code == 429:
                    wait_time = (attempt + 1) * 10
                    log(f"⚠️ Rate limited, waiting {wait_time}s", "WARNING")
                    time.sleep(wait_time)
                    continue
                
                if response.status_code == 200:
                    data = response.json()
                    self.cache[cache_key] = (data, time.time())
                    return data
                else:
                    log(f"⚠️ API returned {response.status_code}", "WARNING")
                    
            except Exception as e:
                log(f"❌ Request failed (attempt {attempt+1}): {e}", "ERROR")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)
        
        return {}
    
    def get_prices(self, coin_ids):
        """Get prices for multiple coins in one request"""
        url = f"{self.base_url}/simple/price"
        params = {
            'ids': ','.join(coin_ids),
            'vs_currencies': 'usd'
        }
        data = self._make_request(url, params)
        return data
    
    def get_top_coins(self, limit=5):
        """Get top cryptocurrencies"""
        url = f"{self.base_url}/coins/markets"
        params = {
            'vs_currency': 'usd',
            'order': 'market_cap_desc',
            'per_page': limit,
            'page': 1,
            'sparkline': 'false'
        }
        data = self._make_request(url, params)
        return data if isinstance(data, list) else []
    
    def get_global_stats(self):
        """Get global market stats"""
        url = f"{self.base_url}/global"
        data = self._make_request(url)
        return data.get('data', {})
    
    def update(self):
        """Perform a single update"""
        try:
            # Get prices for all coins in one request
            prices = self.get_prices(['bitcoin', 'ethereum', 'cardano', 'solana'])
            
            btc_price = prices.get('bitcoin', {}).get('usd', 0)
            eth_price = prices.get('ethereum', {}).get('usd', 0)
            ada_price = prices.get('cardano', {}).get('usd', 0)
            sol_price = prices.get('solana', {}).get('usd', 0)
            
            log("📊 Market Update:")
            log(f"💰 BTC: ${btc_price:,.2f}")
            log(f"💰 ETH: ${eth_price:,.2f}")
            log(f"💰 ADA: ${ada_price:,.2f}")
            log(f"💰 SOL: ${sol_price:,.2f}")
            
            # Get top coins
            top_coins = self.get_top_coins(3)
            if top_coins:
                log("🏆 Top Cryptos:")
                for i, coin in enumerate(top_coins, 1):
                    name = coin.get('name', 'Unknown')
                    symbol = coin.get('symbol', '').upper()
                    price = coin.get('current_price', 0)
                    change = coin.get('price_change_percentage_24h', 0)
                    log(f"  {i}. {name} (${symbol}): ${price:,.2f} ({change:+.2f}%)")
            
            # Get global stats
            global_stats = self.get_global_stats()
            if global_stats:
                total_mcap = global_stats.get('total_market_cap', {}).get('usd', 0)
                log(f"🌍 Total Market Cap: ${total_mcap:,.0f}")
            
            log("-" * 50)
            return True
            
        except Exception as e:
            log(f"❌ Update error: {e}", "ERROR")
            return False
    
    def run(self):
        """Main loop"""
        log("🔄 Bot running continuously...")
        log(f"⏱️  Updates every {UPDATE_INTERVAL} seconds")
        log("=" * 50)
        
        update_count = 0
        while True:
            try:
                update_count += 1
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log(f"📊 Update #{update_count} at {timestamp}")
                
                # Perform update
                success = self.update()
                
                if success:
                    log(f"✅ Update #{update_count} completed")
                else:
                    log(f"⚠️ Update #{update_count} had errors", "WARNING")
                
                # Wait for next update
                time.sleep(UPDATE_INTERVAL)
                
            except KeyboardInterrupt:
                log("🛑 Bot stopped by user")
                break
            except Exception as e:
                log(f"❌ Loop error: {e}", "ERROR")
                log("🔄 Restarting in 30 seconds...")
                time.sleep(30)

def start_health_server():
    """Start health check server for Railway"""
    try:
        server = HTTPServer(('0.0.0.0', HEALTH_PORT), HealthCheckHandler)
        log(f"✅ Health check server running on port {HEALTH_PORT}")
        server.serve_forever()
    except Exception as e:
        log(f"❌ Health server error: {e}", "ERROR")

# Global variable for uptime tracking
bot_start_time = datetime.now()

if __name__ == "__main__":
    try:
        # Start health check server in background
        health_thread = threading.Thread(target=start_health_server, daemon=True)
        health_thread.start()
        log(f"✅ Health check thread started")
        
        # Start bot
        bot = CryptoAlphaBot()
        bot.run()
        
    except Exception as e:
        log(f"❌ Fatal error: {e}", "ERROR")
        # Keep container alive
        log("🔄 Container alive, waiting...")
        while True:
            time.sleep(60)
            log("💓 Heartbeat")
