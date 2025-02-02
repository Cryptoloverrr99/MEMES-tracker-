import aiohttp
from config import settings

class SolscanClient:
    async def get_token_data(self, token_address):
        headers = {'X-API-KEY': settings.SOLSCAN_API_KEY}
        
        async with aiohttp.ClientSession() as session:
            # Récupération des holders
            holders_url = f"https://pro-api.solscan.io/v2.0/token/holders?token={token_address}"
            async with session.get(holders_url, headers=headers) as resp:
                holders_data = await resp.json()
            
            # Récupération des transactions du dev
            balance_url = f"https://pro-api.solscan.io/v2.0/account/balance_change?token={token_address}"
            async with session.get(balance_url, headers=headers) as resp:
                balance_data = await resp.json()
            
            return self._parse_solscan_data(holders_data, balance_data)

    def _parse_solscan_data(self, holders_data, balance_data):
        top10 = sum([h['amount'] for h in holders_data['data'][:10]])
        total = holders_data['total']
        
        return {
            'top10Holders': (top10 / total) * 100 if total > 0 else 0,
            'devHolding': balance_data.get('dev_holding_percent', 0),
            'dev_transfers': balance_data.get('transfer_count', 0) > 0
  }
