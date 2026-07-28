import requests
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from functools import lru_cache

class CryptoBot:
    """
    A cryptocurrency bot with rate limiting and error handling
    """
    
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'CryptoBot/1.0',
            'Accept': 'application/json'
        })
        self.last_request_time = 0
        self.min_request_interval = 2  # 2 seconds between requests to avoid rate limiting
        self.cache = {}
        self.cache_timeout = 60  # Cache data for 60 seconds
        
    def _rate_limit(self):
        """Implement rate limiting to avoid 429 errors"""
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
                    wait_time = (attempt + 1) * 5  # Exponential backoff
                    print(f"Rate limited. Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                
                response.raise_for_status()
                data = response.json()
                
                # Cache successful response
                self.cache[cache_key] = (data, current_time)
                return data
                
            except requests.RequestException as e:
                print(f"Error fetching data (attempt {attempt + 1}/{retry_count}): {e}")
                if attempt < retry_count - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    return {}
        
        return {}
    
    def get_price(self, coin_id: str = 'bitcoin', currency: str = 'usd') -> float:
        """Get current price of cryptocurrency"""
        url = f"{self.base_url}/simple/price"
        params = {'ids': coin_id, 'vs_currencies': currency}
        data = self._make_request(url, params)
        return data.get(coin_id, {}).get(currency, 0.0)
    
    def get_prices_batch(self, coin_ids: List[str], currency: str = 'usd') -> Dict:
        """Get prices for multiple cryptocurrencies in one request"""
        url = f"{self.base_url}/simple/price"
        params = {
            'ids': ','.join(coin_ids),
            'vs_currencies': currency
        }
        data = self._make_request(url, params)
        return data
    
    def get_market_data(self, coin_id: str = 'bitcoin') -> Dict:
        """Get comprehensive market data"""
        url = f"{self.base_url}/coins/{coin_id}"
        params = {
            'localization': 'false',
            'tickers': 'false',
            'market_data': 'true',
            'community_data': 'false',
            'developer_data': 'false'
        }
        data = self._make_request(url, params)
        return data.get('market_data', {})
    
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
        """Track portfolio value using batch requests"""
        portfolio = {
            'total_value_usd': 0.0,
            'holdings': {},
            'timestamp': datetime.now().isoformat()
        }
        
        # Get all prices in one request
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
    
    def get_price_trend(self, coin_id: str = 'bitcoin', 
                       days: int = 7) -> Dict[str, any]:
        """Analyze price trend over a period"""
        prices = self.get_historical_price(coin_id, days)
        
        # Return default trend data if no prices
        if not prices:
            return {
                'coin': coin_id,
                'period_days': days,
                'current_price': 0.0,
                'highest_price': 0.0,
                'lowest_price': 0.0,
                'average_price': 0.0,
                'volatility': 0.0,
                'price_change_7d': 0.0,
                'error': 'No data available'
            }
        
        price_values = [p[1] for p in prices]
        
        trend = {
            'coin': coin_id,
            'period_days': days,
            'current_price': price_values[-1] if price_values else 0,
            'highest_price': max(price_values) if price_values else 0,
            'lowest_price': min(price_values) if price_values else 0,
            'average_price': sum(price_values) / len(price_values) if price_values else 0,
            'volatility': self._calculate_volatility(price_values),
            'price_change_7d': self.calculate_price_change(coin_id, days)[1]
        }
        
        return trend
    
    def _calculate_volatility(self, prices: List[float]) -> float:
        """Calculate price volatility (standard deviation)"""
        if len(prices) < 2:
            return 0.0
        
        mean = sum(prices) / len(prices)
        variance = sum((p - mean) ** 2 for p in prices) / len(prices)
        return variance ** 0.5
    
    def get_global_market_data(self) -> Dict:
        """Get global cryptocurrency market data"""
        url = f"{self.base_url}/global"
        data = self._make_request(url)
        return data.get('data', {})

def main():
    """Main function with fixed error handling"""
    bot = CryptoBot()
    
    print("🚀 Crypto Bot Started!")
    print("=" * 50)
    
    # 1. Get Bitcoin and Ethereum prices in one batch
    prices = bot.get_prices_batch(['bitcoin', 'ethereum'], 'usd')
    btc_price = prices.get('bitcoin', {}).get('usd', 0)
    eth_price = prices.get('ethereum', {}).get('usd', 0)
    
    print(f"💰 Bitcoin Price: ${btc_price:,.2f}")
    print(f"💰 Ethereum Price: ${eth_price:,.2f}")
    
    # 2. Get top 5 cryptocurrencies
    print("\n📊 Top 5 Cryptocurrencies:")
    top_cryptos = bot.get_top_cryptos(5)
    if top_cryptos:
        for i, crypto in enumerate(top_cryptos, 1):
            print(f"{i}. {crypto.get('name', 'Unknown')} (${crypto.get('symbol', '').upper()})")
            print(f"   Price: ${crypto.get('current_price', 0):,.2f}")
            print(f"   Market Cap: ${crypto.get('market_cap', 0):,.0f}")
            print(f"   24h Change: {crypto.get('price_change_percentage_24h', 0):.2f}%\n")
    else:
        print("   Unable to fetch top cryptocurrencies\n")
    
    # 3. Bitcoin price change
    current_price, change = bot.calculate_price_change('bitcoin', 7)
    print(f"📈 Bitcoin 7-day Change: {change:.2f}%")
    
    # 4. Portfolio tracker using batch request
    print("\n💼 Portfolio Tracker:")
    holdings = {
        'bitcoin': 0.5,
        'ethereum': 2.0,
        'cardano': 100
    }
    portfolio = bot.portfolio_tracker(holdings)
    print(f"Total Portfolio Value: ${portfolio['total_value_usd']:,.2f}")
    for coin, data in portfolio['holdings'].items():
        print(f"  {coin}: {data['amount']} units (${data['value_usd']:,.2f})")
    
    # 5. Price trend analysis with safe error handling
    print(f"\n📊 Price Trend Analysis (Bitcoin):")
    trend = bot.get_price_trend('bitcoin', 7)
    
    # Safe access with fallback values
    current_price = trend.get('current_price', 0)
    highest = trend.get('highest_price', 0)
    lowest = trend.get('lowest_price', 0)
    average = trend.get('average_price', 0)
    volatility = trend.get('volatility', 0)
    change_7d = trend.get('price_change_7d', 0)
    
    print(f"Current: ${current_price:,.2f}")
    print(f"7-day High: ${highest:,.2f}")
    print(f"7-day Low: ${lowest:,.2f}")
    print(f"Average: ${average:,.2f}")
    print(f"Volatility: {volatility:.2f}")
    print(f"7-day Change: {change_7d:.2f}%")
    
    # 6. Global market data
    print(f"\n🌍 Global Market Stats:")
    global_data = bot.get_global_market_data()
    if global_data:
        total_mcap = global_data.get('total_market_cap', {}).get('usd', 0)
        total_volume = global_data.get('total_volume', {}).get('usd', 0)
        btc_dominance = global_data.get('market_cap_percentage', {}).get('btc', 0)
        eth_dominance = global_data.get('market_cap_percentage', {}).get('eth', 0)
        
        print(f"Total Market Cap: ${total_mcap:,.0f}")
        print(f"24h Volume: ${total_volume:,.0f}")
        print(f"BTC Dominance: {btc_dominance:.1f}%")
        print(f"ETH Dominance: {eth_dominance:.1f}%")
    
    print("\n✅ Bot completed successfully!")

if __name__ == "__main__":
    main()
