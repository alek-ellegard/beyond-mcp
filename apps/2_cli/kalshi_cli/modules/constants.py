"""
Kalshi CLI Configuration Constants
"""

# Cache configuration
CACHE_TTL_HOURS = 6  # Cache expires after 6 hours

# API configuration
API_BASE_URL = "https://api.elections.kalshi.com/trade-api/v2"
API_TIMEOUT = 30.0  # seconds

# Cache file naming
CACHE_PREFIX = "kalshi_markets_"
CACHE_DIR_NAME = ".kalshi_cache"
