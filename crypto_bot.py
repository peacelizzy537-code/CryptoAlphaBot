import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from functools import lru_cache

class CryptoBot:
    """
    A persistent cryptocurrency bot with rate limiting and continuous monitoring
    """
    
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'CryptoBot/1.0',
            'Accept': 'application/json'
        })
        self.last_request_time = 0
        self.min_request_interval = 3  # 3 seconds between requests
        self.cache = {}
        self.cache_timeout = 120  # Cache for 2 minutes
        self.running = True
        
    def _rate_limit(self):
        """Implement rate limiting"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)
        self.last_request_time = time.time()
    
    def _make_request(self, url: str, params: Dict = None, retry_count: int = 3) -> Dict:
        """Make HTTP request with rate limiting and retries"""
        self._rate_limit()
        
        cache_key = f"{url}{str(params)}"
        current_time = time.time()
        
        # Check cache
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if current_time - timestamp < self.cache_timeout:
                return cached_data
        
        for attempt in range(retry_count):
            try:
                response = self.session.get(url, params=params, timeout=10)
                
                if response.status_code == 429:
                    wait_time = (attempt + 1) * 5
                    print(f"⚠️ Rate limited. Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                
                response.raise_for_status()
                data = response.json()
                self.cache[cache_key] = (data, current_time)
                return data
                
            except requests.RequestException as e:
                print(f"❌ Error (attempt {attempt + 1}/{retry_count}): {e}")
                if attempt < retry_count - 1:
                    time.sleep(2 ** attempt)
                else:
                    return {}
        
        return {}
    
    def get_prices_batch(self, coin_ids: List[str], currency: str = 'usd') -> Dict:
        """Get prices for multiple cryptocurrencies"""
        url = f"{self.base_url}/simple/price"
        params = {
            'ids': ','.join(coin_ids),
            'vs_currencies': currency
        }
        return self._make_request(url, params)
    
    def get_top_cryptos(self, limit: int = 10) -> List[Dict]:
        """Get top cryptocurrencies by market cap"""
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
    
    def get_historical_price(self, coin_id: str = 'bitcoin', 
                           days: int = 30, currency: str = 'usd') -> List[List[float]]:
        """Get historical price data"""
        url = f"{self.base_url}/coins/{coin_id}/market_chart"
        params = {'vs_currency': currency, 'days': days}
        data = self._make_request(url, params)
        return data.get('prices', [])
    
    def calculate_price_change(self, coin_id: str = 'bitcoin', 
                              days: int = 1) -> Tuple[float, float]:
        """Calculate price change percentage"""
        historical_data = self.get_historical_price(coin_id, days)
        if not historical_data or len(historical_data) < 2:
            return (0.0, 0.0)
        
        current_price = historical_data[-1][1]
        old_price = historical_data[0][1]
        
        if old_price == 0:
            return (current_price, 0.0)
        
        change_percent = ((current_price - old_price) / old_price) * 100
        return (current_price, change_percent)
    
    def portfolio_tracker(self, holdings: Dict[str, float]) -> Dict:
        """Track portfolio value"""
        portfolio = {
            'total_value_usd': 0.0,
            'holdings': {},
            'timestamp': datetime.now().isoformat()
        }
        
        coin_ids = list(holdings.keys())
        prices = self.get_prices_batch(coin_ids, 'usd')
        
        for coin_id, amount in holdings.items():
            price = prices.get(coin_id, {}).get('usd', 0.0)
            value = price * amount
            portfolio['holdings'][coin_id] = {
                'amount': amount,
                'price_usd': price,
                'value_usd': value
            }
            portfolio['total_value_usd'] += value
        
        return portfolio
    
    def get_global_market_data(self) -> Dict:
        """Get global cryptocurrency market data"""
        url = f"{self.base_url}/global"
        data = self._make_request(url)
        return data.get('data', {})
    
    def display_market_update(self):
        """Display a single market update"""
        print("\n" + "="*60)
        print(f"📊 Market Update - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        # Get prices
        prices = self.get_prices_batch(['bitcoin', 'ethereum', 'cardano'], 'usd')
        btc_price = prices.get('bitcoin', {}).get('usd', 0)
        eth_price = prices.get('ethereum', {}).get('usd', 0)
        ada_price = prices.get('cardano', {}).get('usd', 0)
        
        print(f"💰 Bitcoin (BTC): ${btc_price:,.2f}")
        print(f"💰 Ethereum (ETH): ${eth_price:,.2f}")
        print(f"💰 Cardano (ADA): ${ada_price:,.2f}")
        
        # Get top cryptos
        top_cryptos = self.get_top_cryptos(3)
        if top_cryptos:
            print("\n🏆 Top 3 Cryptocurrencies:")
            for i, crypto in enumerate(top_cryptos, 1):
                name = crypto.get('name', 'Unknown')
                symbol = crypto.get('symbol', '').upper()
                price = crypto.get('current_price', 0)
                change = crypto.get('price_change_percentage_24h', 0)
                print(f"  {i}. {name} (${symbol}): ${price:,.2f} ({change:+.2f}%)")
        
        # Portfolio value
        holdings = {
            'bitcoin': 0.5,
            'ethereum': 2.0,
            'cardano': 100
        }
        portfolio = self.portfolio_tracker(holdings)
        print(f"\n💼 Portfolio Value: ${portfolio['total_value_usd']:,.2f}")
        
        # Global stats
        global_data = self.get_global_market_data()
        if global_data:
            total_mcap = global_data.get('total_market_cap', {}).get('usd', 0)
            print(f"🌍 Global Market Cap: ${total_mcap:,.0f}")
        
        print("="*60)
    
    def run_continuously(self, interval: int = 60):
        """Run the bot continuously with updates every interval seconds"""
        print("🚀 Crypto Bot Started!")
        print(f"📡 Updating every {interval} seconds...")
        print("Press Ctrl+C to stop\n")
        
        try:
            while self.running:
                self.display_market_update()
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n🛑 Bot stopped by user")
            self.running = False
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(5)

def main():
    """Main entry point"""
    bot = CryptoBot()
    
    # Check if we should run continuously or one-time
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--once':
        # One-time execution
        bot.display_market_update()
        print("\n✅ One-time update completed!")
    else:
        # Continuous mode (default for Railway)
        bot.run_continuously(interval=60)  # Update every 60 seconds

if __name__ == "__main__":
    main()
