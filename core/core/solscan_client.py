import aiohttp

class SolscanClient:
    async def get_token_data(self, token_address):
        headers = {'X-API-KEY': ''}  # Laisser vide pour API publique
        
        async with aiohttp.ClientSession() as session:
            # Récupération des holders
            holders_url = f"https://public-api.solscan.io/token/holders?tokenAddress={token_address}"
            async with session.get(holders_url, headers=headers) as resp:
                holders_data = await resp.json()
            
            return {
                'top10Holders': sum([h['amount'] for h in holders_data['data'][:10]]) / holders_data['total'] * 100,
                'dev_transfers': False  # Temporaire
            }
