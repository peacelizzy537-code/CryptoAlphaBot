import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class CryptoBot:
    """
    A cryptocurrency bot with various functions for tracking, analyzing,
    and managing crypto assets.
    """
    
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'CryptoBot/1.0',
            'Accept': 'application/json'
        })
        
    def get_price(self, coin_id: str = 'bitcoin', currency: str = 'usd') -> float:
        """
        Get the current price of a cryptocurrency in the specified currency.
        
        Args:
            coin_id: CoinGecko coin ID (e.g., 'bitcoin', 'ethereum')
            currency: Target currency (e.g., 'usd', 'eur', 'gbp')
            
        Returns:
            float: Current price
        """
        try:
            url = f"{self.base_url}/simple/price"
            params = {
                'ids': coin_id,
                'vs_currencies': currency
            }
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get(coin_id, {}).get(currency, 0.0)
        except requests.RequestException as e:
            print(f"Error fetching price: {e}")
            return 0.0
    
    def get_market_data(self, coin_id: str = 'bitcoin') -> Dict:
        """
        Get comprehensive market data for a cryptocurrency.
        
        Args:
            coin_id: CoinGecko coin ID
            
        Returns:
            Dict: Market data including price, volume, market cap, etc.
        """
        try:
            url = f"{self.base_url}/coins/{coin_id}"
            params = {
                'localization': 'false',
                'tickers': 'false',
                'market_data': 'true',
                'community_data': 'false',
                'developer_data': 'false'
            }
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get('market_data', {})
        except requests.RequestException as e:
            print(f"Error fetching market data: {e}")
            return {}
    
    def get_top_cryptos(self, limit: int = 10) -> List[Dict]:
        """
        Get top cryptocurrencies by market cap.
        
        Args:
            limit: Number of top cryptos to return
            
        Returns:
            List[Dict]: List of top cryptocurrencies with their data
        """
        try:
            url = f"{self.base_url}/coins/markets"
            params = {
                'vs_currency': 'usd',
                'order': 'market_cap_desc',
                'per_page': limit,
                'page': 1,
                'sparkline': 'false'
            }
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching top cryptos: {e}")
            return []
    
    def get_historical_price(self, coin_id: str = 'bitcoin', 
                           days: int = 30, currency: str = 'usd') -> List[List[float]]:
        """
        Get historical price data for a cryptocurrency.
        
        Args:
            coin_id: CoinGecko coin ID
            days: Number of days of historical data
            currency: Target currency
            
        Returns:
            List[List[float]]: Historical price data [timestamp, price]
        """
        try:
            url = f"{self.base_url}/coins/{coin_id}/market_chart"
            params = {
                'vs_currency': currency,
                'days': days
            }
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get('prices', [])
        except requests.RequestException as e:
            print(f"Error fetching historical data: {e}")
            return []
    
    def calculate_price_change(self, coin_id: str = 'bitcoin', 
                              days: int = 1) -> Tuple[float, float]:
        """
        Calculate the price change percentage over a specified period.
        
        Args:
            coin_id: CoinGecko coin ID
            days: Number of days to compare
            
        Returns:
            Tuple[float, float]: (current_price, change_percentage)
        """
        historical_data = self.get_historical_price(coin_id, days)
        if not historical_data or len(historical_data) < 2:
            return (0.0, 0.0)
        
        current_price = historical_data[-1][1]
        old_price = historical_data[0][1]
        
        if old_price == 0:
            return (current_price, 0.0)
        
        change_percent = ((current_price - old_price) / old_price) * 100
        return (current_price, change_percent)
    
    def get_coin_list(self) -> List[Dict]:
        """
        Get a list of all supported cryptocurrencies.
        
        Returns:
            List[Dict]: List of coins with their IDs and symbols
        """
        try:
            url = f"{self.base_url}/coins/list"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching coin list: {e}")
            return []
    
    def get_global_market_data(self) -> Dict:
        """
        Get global cryptocurrency market data.
        
        Returns:
            Dict: Global market statistics
        """
        try:
            url = f"{self.base_url}/global"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get('data', {})
        except requests.RequestException as e:
            print(f"Error fetching global data: {e}")
            return {}
    
    def monitor_price_alerts(self, coin_id: str = 'bitcoin', 
                           target_price: float = 50000, 
                           currency: str = 'usd') -> None:
        """
        Monitor price and alert when it crosses a target price.
        
        Args:
            coin_id: CoinGecko coin ID
            target_price: Target price to monitor
            currency: Target currency
        """
        print(f"Monitoring {coin_id} price for target: ${target_price} {currency.upper()}")
        print("Press Ctrl+C to stop monitoring...")
        
        try:
            while True:
                current_price = self.get_price(coin_id, currency)
                if current_price == 0:
                    print("Error fetching price. Retrying...")
                    time.sleep(5)
                    continue
                
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{timestamp}] Current {coin_id} price: ${current_price:.2f}")
                
                if current_price >= target_price:
                    print(f"🚨 ALERT: {coin_id} has reached ${current_price:.2f}!")
                    print(f"Target ${target_price} exceeded by ${current_price - target_price:.2f}")
                    
                    # Send alert (you can integrate with email, Telegram, etc.)
                    self.send_alert(coin_id, current_price, target_price)
                    break
                
                time.sleep(10)  # Check every 10 seconds
                
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user.")
    
    def send_alert(self, coin_id: str, current_price: float, target_price: float) -> None:
        """
        Send an alert for price target reached.
        
        Args:
            coin_id: CoinGecko coin ID
            current_price: Current price
            target_price: Target price
        """
        # This is a placeholder - you can implement email, Telegram, SMS, etc.
        print(f"\n📧 Sending alert: {coin_id} price alert triggered!")
        print(f"Current: ${current_price:.2f}, Target: ${target_price:.2f}")
    
    def portfolio_tracker(self, holdings: Dict[str, float]) -> Dict:
        """
        Track portfolio value across multiple cryptocurrencies.
        
        Args:
            holdings: Dictionary of {coin_id: amount_held}
            
        Returns:
            Dict: Portfolio valuation details
        """
        portfolio = {
            'total_value_usd': 0.0,
            'holdings': {},
            'timestamp': datetime.now().isoformat()
        }
        
        for coin_id, amount in holdings.items():
            price = self.get_price(coin_id, 'usd')
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
        """
        Analyze price trend over a period.
        
        Args:
            coin_id: CoinGecko coin ID
            days: Number of days to analyze
            
        Returns:
            Dict: Trend analysis
        """
        prices = self.get_historical_price(coin_id, days)
        if not prices:
            return {'error': 'No data available'}
        
        price_values = [p[1] for p in prices]
        
        trend = {
            'coin': coin_id,
            'period_days': days,
            'current_price': price_values[-1] if price_values else 0,
            'highest_price': max(price_values) if price_values else 0,
            'lowest_price': min(price_values) if price_values else 0,
            'average_price': sum(price_values) / len(price_values) if price_values else 0,
            'volatility': self.calculate_volatility(price_values),
            'price_change_7d': self.calculate_price_change(coin_id, days)[1]
        }
        
        return trend
    
    def calculate_volatility(self, prices: List[float]) -> float:
        """
        Calculate price volatility (standard deviation).
        
        Args:
            prices: List of prices
            
        Returns:
            float: Volatility measure
        """
        if len(prices) < 2:
            return 0.0
        
        mean = sum(prices) / len(prices)
        variance = sum((p - mean) ** 2 for p in prices) / len(prices)
        return variance ** 0.5

# Example usage and demonstration
def main():
    # Initialize the bot
    bot = CryptoBot()
    
    print("🚀 Crypto Bot Started!")
    print("=" * 50)
    
    # 1. Get current Bitcoin price
    btc_price = bot.get_price('bitcoin', 'usd')
    print(f"💰 Bitcoin Price: ${btc_price:,.2f}")
    
    # 2. Get Ethereum price
    eth_price = bot.get_price('ethereum', 'usd')
    print(f"💰 Ethereum Price: ${eth_price:,.2f}")
    
    # 3. Get top 5 cryptocurrencies
    print("\n📊 Top 5 Cryptocurrencies:")
    top_cryptos = bot.get_top_cryptos(5)
    for i, crypto in enumerate(top_cryptos, 1):
        print(f"{i}. {crypto['name']} (${crypto['symbol'].upper()})")
        print(f"   Price: ${crypto['current_price']:,.2f}")
        print(f"   Market Cap: ${crypto['market_cap']:,.0f}")
        print(f"   24h Change: {crypto['price_change_percentage_24h']:.2f}%\n")
    
    # 4. Bitcoin price change analysis
    current_price, change = bot.calculate_price_change('bitcoin', 7)
    print(f"📈 Bitcoin 7-day Change: {change:.2f}%")
    
    # 5. Portfolio tracker example
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
    
    # 6. Price trend analysis
    print(f"\n📊 Price Trend Analysis (Bitcoin):")
    trend = bot.get_price_trend('bitcoin', 7)
    print(f"Current: ${trend['current_price']:,.2f}")
    print(f"7-day High: ${trend['highest_price']:,.2f}")
    print(f"7-day Low: ${trend['lowest_price']:,.2f}")
    print(f"Average: ${trend['average_price']:,.2f}")
    print(f"Volatility: {trend['volatility']:.2f}")
    print(f"7-day Change: {trend['price_change_7d']:.2f}%")
    
    # 7. Global market data
    print(f"\n🌍 Global Market Stats:")
    global_data = bot.get_global_market_data()
    if global_data:
        print(f"Total Market Cap: ${global_data.get('total_market_cap', {}).get('usd', 0):,.0f}")
        print(f"24h Volume: ${global_data.get('total_volume', {}).get('usd', 0):,.0f}")
        print(f"BTC Dominance: {global_data.get('market_cap_percentage', {}).get('btc', 0):.1f}%")
        print(f"ETH Dominance: {global_data.get('market_cap_percentage', {}).get('eth', 0):.1f}%")
    
    # Uncomment to start price monitoring (will run continuously)
    # print("\n🔔 Starting price monitor for Bitcoin at $60,000...")
    # bot.monitor_price_alerts('bitcoin', 60000)
    
    print("\n✅ Demo completed successfully!")

if __name__ == "__main__":
    main()
