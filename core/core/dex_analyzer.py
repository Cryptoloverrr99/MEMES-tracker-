import aiohttp
from functools import lru_cache

class DexAnalyzer:
    @lru_cache(maxsize=100)
    async def fetch_new_tokens(self):
        url = "https://api.dexscreener.com/token-profiles/latest/v1"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                return self._process_tokens(data['data'])

    def _process_tokens(self, raw_tokens):
        processed = []
        for token in raw_tokens:
            processed.append({
                'address': token['address'],
                'symbol': token['symbol'],
                'marketCap': token.get('marketCap', 0),
                'liquidity': token.get('liquidity', 0),
                'volume': token.get('volume24h', 0),
                'holders': token.get('holders', 0),
                'url': f"https://dexscreener.com/solana/{token['address']}"
            })
        return processed
