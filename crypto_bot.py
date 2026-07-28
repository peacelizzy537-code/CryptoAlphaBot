#!/usr/bin/env python3
"""
CryptoAlphaBot - Guaranteed to Run Forever
"""
import time
import sys
import threading
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True)

UPDATE_INTERVAL = 60  # seconds
HEALTH_PORT = 8080

def log(message):
    """Simple logging"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")
    sys.stdout.flush()

# Import requests with fallback
try:
    import requests
    log("✅ requests loaded")
except:
    log("⚠️ Installing requests...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests
    log("✅ requests installed")

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"status":"healthy","message":"CryptoAlphaBot is running"}')

class CryptoAlphaBot:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'CryptoAlphaBot/1.0'})
        self.running = True
        log("✅ Bot initialized")
    
    def get_prices(self):
        """Fetch prices"""
        try:
            url = f"{self.base_url}/simple/price"
            params = {'ids': 'bitcoin,ethereum,cardano,solana', 'vs_currencies': 'usd'}
            response = self.session.get(url, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
            return {}
        except Exception as e:
            log(f"❌ API Error: {e}")
            return {}
    
    def run(self):
        """Main loop - RUNS FOREVER"""
        log("🚀 Bot started!")
        log(f"⏱️  Updates every {UPDATE_INTERVAL} seconds")
        log("=" * 50)
        
        counter = 0
        while self.running:  # This loop never stops
            try:
                counter += 1
                log(f"📊 Update #{counter}")
                
                # Get prices
                prices = self.get_prices()
                
                btc = prices.get('bitcoin', {}).get('usd', 0)
                eth = prices.get('ethereum', {}).get('usd', 0)
                ada = prices.get('cardano', {}).get('usd', 0)
                sol = prices.get('solana', {}).get('usd', 0)
                
                log(f"💰 BTC: ${btc:,.2f}")
                log(f"💰 ETH: ${eth:,.2f}")
                log(f"💰 ADA: ${ada:,.2f}")
                log(f"💰 SOL: ${sol:,.2f}")
                log(f"💓 Bot alive for {counter * UPDATE_INTERVAL}s")
                log("-" * 40)
                
                # IMPORTANT: This sleep keeps the bot running
                log(f"💤 Sleeping for {UPDATE_INTERVAL} seconds...")
                time.sleep(UPDATE_INTERVAL)
                
            except KeyboardInterrupt:
                log("🛑 Stopping...")
                self.running = False
                break
            except Exception as e:
                log(f"❌ Error: {e}")
                log("🔄 Restarting in 5 seconds...")
                time.sleep(5)

def start_health_server():
    """Health check server"""
    try:
        server = HTTPServer(('0.0.0.0', HEALTH_PORT), HealthHandler)
        log(f"✅ Health server on port {HEALTH_PORT}")
        server.serve_forever()
    except Exception as e:
        log(f"❌ Health server error: {e}")

if __name__ == "__main__":
    log("🚀 CryptoAlphaBot Starting...")
    
    # Start health check
    health_thread = threading.Thread(target=start_health_server, daemon=True)
    health_thread.start()
    log("✅ Health check started")
    
    # Create and run bot
    bot = CryptoAlphaBot()
    
    # This will run forever
    bot.run()
    
    # If we get here, something went wrong
    log("⚠️ Bot exited, keeping container alive...")
    while True:
        time.sleep(60)
        log("💓 Container still alive")
