import aiohttp
from functools import lru_cache  # <-- Ligne ajoutée ici
from config import settings

class DexAnalyzer:
    @lru_cache(maxsize=100)  # <-- Ligne ajoutée ici
    async def fetch_new_tokens(self):
        # Le reste reste identique
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
