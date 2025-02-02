import asyncio
import aiohttp
import json
import logging
from core.dex_analyzer import DexAnalyzer
from core.solscan_client import SolscanClient
from core.alert_manager import AlertManager
from config import settings

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class MemeTracker:
    def __init__(self):
        self.dex = DexAnalyzer()
        self.solscan = SolscanClient()
        self.alerter = AlertManager()
        self.processed_tokens = self._load_processed_tokens()

    def _load_processed_tokens(self):
        try:
            with open('data/processed_tokens.json', 'r') as f:
                return set(json.load(f))
        except FileNotFoundError:
            return set()

    def _save_processed_tokens(self):
        with open('data/processed_tokens.json', 'w') as f:
            json.dump(list(self.processed_tokens), f)

    async def check_new_listings(self):
        tokens = await self.dex.fetch_new_tokens()
        
        for token in tokens:
            if token['address'] in self.processed_tokens:
                continue
                
            solscan_data = await self.solscan.get_token_data(token['address'])
            
            if self._check_conditions(token, solscan_data):
                await self.alerter.send_alert(token, "no", "no")
                self.processed_tokens.add(token['address'])
        
        self._save_processed_tokens()

    def _check_conditions(self, token, solscan_data):
        return all([
            token['marketCap'] >= settings.FILTERS['min_mcap'],
            token['liquidity'] >= settings.FILTERS['min_liquidity'],
            token['holders'] >= settings.FILTERS['min_holders'],
            solscan_data['top10Holders'] <= settings.FILTERS['max_top10_holding'] * 100,
            not solscan_data['dev_transfers']
        ])

import traceback  # <-- Ligne ajoutée ici

async def main():
    tracker = MemeTracker()
    while True:
        try:  # <-- Début ajouté
            await tracker.check_new_listings()
        except Exception as e:
            logging.error(f"ERREUR: {traceback.format_exc()}")
            await tracker.alerter.send_error_alert(traceback.format_exc())
            await asyncio.sleep(60)
        await asyncio.sleep(settings.CHECK_INTERVAL)  # <-- Fin ajouté

if __name__ == "__main__":
    asyncio.run(main())
