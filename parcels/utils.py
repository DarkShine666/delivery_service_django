import requests
import logging

logger = logging.getLogger(__name__)

CBR_URL = "https://www.cbr-xml-daily.ru/daily_json.js"


def get_usd_exchange_rate() -> float:
    try:
        response = requests.get(CBR_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data["Valute"]["USD"]["Value"]
    except Exception as e:
        logger.warning(f"Failed to get USD exchange rate: {e}")
        return 90.0  # fallback rate
