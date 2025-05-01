import logging
from typing import List, Dict
from app.weather_api import get_current_weather, get_forecast, get_historical_weather

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class FavoriteLocationModel:

    def __init__(self):
        self.user_favorites: Dict[int, List[str]] = {}

    def add_favorite(self, user_id: int, location: str) -> None:
        logger.info(f"adding favorite for user {user_id}: {location}")
        self.user_favorites.setdefault(user_id, [])
        if location in self.user_favorites[user_id]:
            raise ValueError(f"{location} is already favorited")
        self.user_favorites[user_id].append(location)

    def remove_favorite(self, user_id: int, location: str) -> None:
        logger.info(f"remove favorite - {user_id}: {location}")
        if user_id not in self.user_favorites or location not in self.user_favorites[user_id]:
            raise ValueError(f"{location} not favorited")
        self.user_favorites[user_id].remove(location)

    def get_favorites(self, user_id: int) -> List[str]:
        logger.info(f"fetching favorites for user {user_id}")
        return self.user_favorites.get(user_id, [])
    
    def get_weather_for_all(self, user_id: int) -> Dict[str, dict]:
        logger.info(f"getting current weather for all favorites of user {user_id}")
        return {loc: get_current_weather(loc) for loc in self.get_favorites(user_id)}
    
    def get_forecast_for_all(self, user_id: int) -> Dict[str, dict]:
        logger.info(f"getting forecast for all favorites of user {user_id}")
        return {loc: get_forecast(loc) for loc in self.get_favorites(user_id)}
    
    def get_historical_for_city(self, city: str, days_ago: int) -> dict:
        logger.info(f"Getting historical weather for {city}, {days_ago} days ago")
        from time import time
        now = int(time())
        timestamp = now - days_ago * 86400

        coord_data = get_current_weather(city).get("coord")
        if not coord_data:
            raise ValueError("Could not fetch coordinates for city")

        lat = coord_data["lat"]
        lon = coord_data["lon"]
        return get_historical_weather(lat, lon, timestamp)