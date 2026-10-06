import aiohttp
import config

class APIProvider:
    def __init__(self):
        self.base_url = config.YT_API_URL
        self.api_key = config.YT_API_KEY
        self.plans = {
            "free": {"price": 0, "limit": 100},
            "lite": {"price": 49, "limit": 1500},
            "basic": {"price": 79, "limit": 3000},
            "starter": {"price": 99, "limit": 5000},
            "standard": {"price": 199, "limit": 10000},
            "pro": {"price": 329, "limit": 25000},
            "business": {"price": 569, "limit": 50000},
            "enterprise": {"price": 1099, "limit": 100000},
        }

    async def fetch_track(self, query: str):
        """
        ShrutiBots API provider के ज़रिए गाने या ट्रैक की डिटेल्स सर्च और फेच करने का फंक्शन।
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "query": query
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{self.base_url}/search", 
                    json=payload, 
                    headers=headers, 
                    timeout=config.YT_TOKEN_TIMEOUT
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        return None
            except Exception as e:
                print(f"[API Provider Error] Failed to fetch track: {e}")
                return None

    def get_plan_details(self, plan_name: str):
        """
        दिए गए प्लान का नाम और उसकी डेली लिमिट्स रिटर्न करता है।
        """
        return self.plans.get(plan_name.lower(), self.plans["free"])

# Instance create karein taaki baaki modules mein seedha import kiya ja sake
api_client = APIProvider()
