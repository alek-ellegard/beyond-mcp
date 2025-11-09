#!/usr/bin/env python3
"""
Kalshi Prediction Markets HTTP Client
Direct API access without SDK dependencies - faster, cleaner, more reliable

API Documentation: https://docs.kalshi.com/
Base URL: https://api.elections.kalshi.com/trade-api/v2
"""

import httpx
import pandas as pd
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

from .constants import (
    CACHE_TTL_HOURS,
    API_BASE_URL,
    API_TIMEOUT,
    CACHE_PREFIX,
    CACHE_DIR_NAME,
)


class KalshiSearchCache:
    """
    Manages cached market data for fast pandas-based searching.

    Strategy:
    1. First search: Fetch ALL series & markets (OPEN only), save to CSV
    2. Subsequent searches: Load from CSV, search with pandas (instant!)
    3. Cache expires after 6 hours (filename contains timestamp)
    """

    def __init__(self, cache_dir: str = None, ttl_hours: int = None):
        if cache_dir is None:
            # Store cache in project root: /Users/.../beyond-mcp/.kalshi_cache/
            # From: apps/2_cli/kalshi_cli/modules/client.py
            # Need to go up 5 levels to reach beyond-mcp/
            # Resolve to absolute path first to handle relative invocations
            project_root = Path(__file__).resolve().parent.parent.parent.parent.parent
            cache_dir = project_root / CACHE_DIR_NAME

        if ttl_hours is None:
            ttl_hours = CACHE_TTL_HOURS

        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl_hours = ttl_hours
        self.cache_prefix = CACHE_PREFIX

    def _get_current_cache_file(self) -> Optional[Path]:
        """Find the most recent valid cache file."""
        cache_files = list(self.cache_dir.glob(f"{self.cache_prefix}*.csv"))
        if not cache_files:
            return None

        cache_files.sort(reverse=True)
        latest_cache = cache_files[0]

        try:
            filename = latest_cache.stem
            timestamp_str = filename.replace(self.cache_prefix, "")
            cache_time = datetime.strptime(timestamp_str, "%Y%m%d_%H%M")

            if datetime.now() - cache_time < timedelta(hours=self.ttl_hours):
                return latest_cache
        except:
            pass

        return None

    def _get_new_cache_filename(self) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        return self.cache_dir / f"{self.cache_prefix}{timestamp}.csv"

    def _clean_old_cache_files(self, quiet: bool = False):
        """Remove expired cache files."""
        cache_files = list(self.cache_dir.glob(f"{self.cache_prefix}*.csv"))
        for cache_file in cache_files:
            try:
                filename = cache_file.stem
                timestamp_str = filename.replace(self.cache_prefix, "")
                cache_time = datetime.strptime(timestamp_str, "%Y%m%d_%H%M")

                if datetime.now() - cache_time >= timedelta(hours=self.ttl_hours):
                    cache_file.unlink()
                    if not quiet:
                        print(f"[CACHE] Removed expired cache: {cache_file.name}")
            except:
                continue

    def build_cache(self, kalshi_client, quiet: bool = False) -> pd.DataFrame:
        """Build cache by fetching all series and their OPEN markets."""
        if not quiet:
            print(f"\n{'='*80}")
            print(f"[CACHE BUILD] Starting market data collection")
            print(f"{'='*80}")
            print(f"[CACHE BUILD] This is a ONE-TIME operation per hour")
            print(f"[CACHE BUILD] Expected time: 2-5 minutes")
            print(f"[CACHE BUILD] Collecting: OPEN markets only")
            print(f"[CACHE BUILD] Cache location: {self.cache_dir}")
            print(f"[CACHE BUILD] Cache TTL: {self.ttl_hours} hour(s)")
            print(f"{'='*80}\n")

        start_time = time.time()

        if not quiet:
            print(f"[CACHE BUILD] Step 1/3: Fetching series list...")
        series_response = kalshi_client.get_series_list()
        all_series = series_response.get('series', [])
        if not quiet:
            print(f"[CACHE BUILD] ✓ Found {len(all_series)} series to process\n")
            print(f"[CACHE BUILD] Step 2/3: Fetching markets from each series...")
            print(f"[CACHE BUILD] Filter: status='open' (active tradeable markets only)")
            print(f"[CACHE BUILD] Progress updates every 100 series...\n")

        all_markets = []
        errors = 0
        series_with_markets = 0

        for i, series in enumerate(all_series):
            series_ticker = series.get('ticker')
            series_title = series.get('title', '')
            series_category = series.get('category', '')

            if (i + 1) % 100 == 0 and not quiet:
                elapsed_so_far = time.time() - start_time
                rate = (i + 1) / elapsed_so_far
                remaining = (len(all_series) - i - 1) / rate if rate > 0 else 0
                print(f"[CACHE BUILD] Progress: {i + 1}/{len(all_series)} series ({100*(i+1)/len(all_series):.1f}%)")
                print(f"[CACHE BUILD]   ├─ Markets collected: {len(all_markets)}")
                print(f"[CACHE BUILD]   ├─ Series with markets: {series_with_markets}")
                print(f"[CACHE BUILD]   ├─ Time elapsed: {elapsed_so_far:.1f}s")
                print(f"[CACHE BUILD]   └─ Est. remaining: {remaining:.1f}s\n")

            try:
                markets_response = kalshi_client.get_markets(
                    series_ticker=series_ticker,
                    limit=100,
                    status="open"  # ONLY OPEN MARKETS
                )
                series_markets = markets_response.get('markets', [])

                if series_markets:
                    series_with_markets += 1

                for market in series_markets:
                    market['series_ticker'] = series_ticker
                    market['series_title'] = series_title
                    market['series_category'] = series_category
                    all_markets.append(market)

                if i % 50 == 0 and i > 0:
                    time.sleep(0.5)

            except Exception as e:
                errors += 1
                if "429" in str(e) or "too many" in str(e).lower():
                    if not quiet:
                        print(f"[CACHE BUILD] Rate limited at series {i}, pausing 2s...")
                    time.sleep(2)

                if errors > 50:
                    if not quiet:
                        print(f"[CACHE BUILD] ⚠ Too many errors ({errors}), stopping at {i}/{len(all_series)} series")
                    break
                continue

        elapsed = time.time() - start_time
        if not quiet:
            print(f"\n[CACHE BUILD] Step 3/3: Saving to CSV...")
            print(f"[CACHE BUILD] ✓ Collection complete!")
            print(f"[CACHE BUILD]   ├─ Total markets: {len(all_markets)}")
            print(f"[CACHE BUILD]   ├─ Series processed: {len(all_series)}")
            print(f"[CACHE BUILD]   ├─ Series with markets: {series_with_markets}")
            print(f"[CACHE BUILD]   ├─ Errors encountered: {errors}")
            print(f"[CACHE BUILD]   └─ Total time: {elapsed:.1f}s ({elapsed/60:.1f}m)\n")

        df = pd.DataFrame(all_markets)
        cache_file = self._get_new_cache_filename()
        df.to_csv(cache_file, index=False)

        file_size_mb = cache_file.stat().st_size / (1024 * 1024)
        if not quiet:
            print(f"[CACHE BUILD] ✓ Saved to: {cache_file.name}")
            print(f"[CACHE BUILD]   └─ File size: {file_size_mb:.2f} MB")

            print(f"\n[CACHE BUILD] Cleaning up old cache files...")
        self._clean_old_cache_files(quiet=quiet)

        if not quiet:
            print(f"{'='*80}")
            print(f"[CACHE BUILD] Cache ready! Subsequent searches will be instant.")
            print(f"{'='*80}\n")

        return df

    def load_cache(self, kalshi_client, quiet: bool = False) -> pd.DataFrame:
        """Load cache from file, or build if expired/missing."""
        cache_file = self._get_current_cache_file()

        if cache_file:
            if not quiet:
                print(f"[CACHE] Loading from cache: {cache_file.name}")
            df = pd.read_csv(cache_file, low_memory=False)
            if not quiet:
                print(f"[CACHE] Loaded {len(df)} markets (cache is fresh)")
            return df

        return self.build_cache(kalshi_client, quiet=quiet)

    def search(self, kalshi_client, keyword: str, limit: int = 20, quiet: bool = False) -> List[Dict[str, Any]]:
        """Search cached markets using pandas."""
        df = self.load_cache(kalshi_client, quiet=quiet)

        if df.empty:
            if not quiet:
                print("[CACHE] No markets in cache")
            return []

        keyword_lower = keyword.lower()

        mask = (
            df['title'].str.lower().str.contains(keyword_lower, na=False) |
            df['subtitle'].str.lower().str.contains(keyword_lower, na=False) |
            df['series_title'].str.lower().str.contains(keyword_lower, na=False) |
            df['series_ticker'].str.lower().str.contains(keyword_lower, na=False)
        )

        results_df = df[mask].head(limit)
        if not quiet:
            print(f"[CACHE] Found {len(results_df)} matches for '{keyword}'")

        return results_df.to_dict('records')


class KalshiClient:
    """
    HTTP client for Kalshi Prediction Markets API

    Provides clean, typed interfaces to all public Kalshi API endpoints.
    No authentication required for read-only market data access.
    """

    def __init__(self, timeout: float = None):
        """Initialize HTTP client with optional timeout"""
        if timeout is None:
            timeout = API_TIMEOUT

        self.client = httpx.Client(
            base_url=API_BASE_URL,
            timeout=timeout,
            follow_redirects=True
        )

    def __del__(self):
        """Clean up HTTP client"""
        if hasattr(self, 'client'):
            self.client.close()

    # ========================================
    # Exchange Status
    # ========================================

    def get_exchange_status(self) -> Dict[str, Any]:
        """
        Get current exchange status (trading hours, maintenance, etc.)

        Returns:
            Dict with exchange_active, trading_active, and estimated_resume_time
        """
        response = self.client.get("/exchange/status")
        response.raise_for_status()
        return response.json()

    # ========================================
    # Markets
    # ========================================

    def get_markets(
        self,
        limit: int = 100,
        cursor: Optional[str] = None,
        event_ticker: Optional[str] = None,
        series_ticker: Optional[str] = None,
        max_close_ts: Optional[int] = None,
        min_close_ts: Optional[int] = None,
        status: Optional[str] = None,
        tickers: Optional[str] = None,
        mve_filter: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get markets with various filters

        Args:
            limit: Number of results (1-1000, default 100)
            cursor: Pagination cursor
            event_ticker: Filter by event ticker (comma-separated list, max 10)
            series_ticker: Filter by series ticker
            max_close_ts: Filter markets closing before this Unix timestamp
            min_close_ts: Filter markets closing after this Unix timestamp
            status: Filter by status ('unopened', 'open', 'closed', 'settled')
            tickers: Filter by market tickers (comma-separated)
            mve_filter: Multivariate events filter ('only' or 'exclude')

        Returns:
            Dict with 'markets' list and 'cursor' for pagination
        """
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
        if event_ticker:
            params["event_ticker"] = event_ticker
        if series_ticker:
            params["series_ticker"] = series_ticker
        if max_close_ts:
            params["max_close_ts"] = max_close_ts
        if min_close_ts:
            params["min_close_ts"] = min_close_ts
        if status:
            params["status"] = status
        if tickers:
            params["tickers"] = tickers
        if mve_filter:
            params["mve_filter"] = mve_filter

        response = self.client.get("/markets", params=params)
        response.raise_for_status()
        return response.json()

    def get_market(self, ticker: str) -> Dict[str, Any]:
        """
        Get detailed information for a specific market

        Args:
            ticker: Market ticker symbol

        Returns:
            Dict with full market details including prices, volume, and metadata
        """
        response = self.client.get(f"/markets/{ticker}")
        response.raise_for_status()
        return response.json()

    def get_market_orderbook(
        self,
        ticker: str,
        depth: int = 0
    ) -> Dict[str, Any]:
        """
        Get orderbook for a specific market

        Args:
            ticker: Market ticker symbol
            depth: Orderbook depth (0 = all levels, 1-100 for specific depth)

        Returns:
            Dict with 'orderbook' containing yes/no bid arrays
        """
        params = {"depth": depth}
        response = self.client.get(f"/markets/{ticker}/orderbook", params=params)
        response.raise_for_status()
        return response.json()

    def get_trades(
        self,
        limit: int = 100,
        cursor: Optional[str] = None,
        ticker: Optional[str] = None,
        min_ts: Optional[int] = None,
        max_ts: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Get recent trades across markets or for a specific market

        Args:
            limit: Number of trades to return (1-1000, default 100)
            cursor: Pagination cursor
            ticker: Filter trades for specific market
            min_ts: Filter trades after this Unix timestamp
            max_ts: Filter trades before this Unix timestamp

        Returns:
            Dict with 'trades' list and 'cursor'
        """
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
        if ticker:
            params["ticker"] = ticker
        if min_ts:
            params["min_ts"] = min_ts
        if max_ts:
            params["max_ts"] = max_ts

        response = self.client.get("/markets/trades", params=params)
        response.raise_for_status()
        return response.json()

    def get_market_candlesticks(
        self,
        series_ticker: str,
        market_ticker: str,
        start_ts: int,
        end_ts: int,
        period_interval: int = 60
    ) -> Dict[str, Any]:
        """
        Get candlestick data for a specific market

        Args:
            series_ticker: Series ticker containing the market
            market_ticker: Market ticker
            start_ts: Start timestamp (Unix timestamp)
            end_ts: End timestamp (Unix timestamp)
            period_interval: Period length in minutes (1, 60, or 1440)

        Returns:
            Dict with 'ticker' and 'candlesticks' array
        """
        params = {
            "start_ts": start_ts,
            "end_ts": end_ts,
            "period_interval": period_interval
        }
        path = f"/series/{series_ticker}/markets/{market_ticker}/candlesticks"
        response = self.client.get(path, params=params)
        response.raise_for_status()
        return response.json()

    # ========================================
    # Events
    # ========================================

    def get_events(
        self,
        limit: int = 200,
        cursor: Optional[str] = None,
        with_nested_markets: bool = False,
        with_milestones: bool = False,
        status: Optional[str] = None,
        series_ticker: Optional[str] = None,
        min_close_ts: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Get events with various filters

        Args:
            limit: Number of results (1-200, default 200)
            cursor: Pagination cursor
            with_nested_markets: Include markets within each event
            with_milestones: Include related milestones
            status: Filter by status ('open', 'closed', 'settled')
            series_ticker: Filter by series ticker
            min_close_ts: Filter events with markets closing after this timestamp

        Returns:
            Dict with 'events' list, optional 'milestones', and 'cursor'
        """
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
        if with_nested_markets:
            params["with_nested_markets"] = "true"
        if with_milestones:
            params["with_milestones"] = "true"
        if status:
            params["status"] = status
        if series_ticker:
            params["series_ticker"] = series_ticker
        if min_close_ts:
            params["min_close_ts"] = min_close_ts

        response = self.client.get("/events", params=params)
        response.raise_for_status()
        return response.json()

    def get_event(
        self,
        event_ticker: str,
        with_nested_markets: bool = False
    ) -> Dict[str, Any]:
        """
        Get detailed information for a specific event

        Args:
            event_ticker: Event ticker
            with_nested_markets: Include markets within the event object

        Returns:
            Dict with 'event' object and 'markets' array
        """
        params = {}
        if with_nested_markets:
            params["with_nested_markets"] = "true"

        response = self.client.get(f"/events/{event_ticker}", params=params)
        response.raise_for_status()
        return response.json()

    def get_multivariate_events(
        self,
        limit: int = 100,
        cursor: Optional[str] = None,
        series_ticker: Optional[str] = None,
        collection_ticker: Optional[str] = None,
        with_nested_markets: bool = False,
    ) -> Dict[str, Any]:
        """
        Get multivariate (combo) events

        Args:
            limit: Number of results (1-200, default 100)
            cursor: Pagination cursor
            series_ticker: Filter by series ticker (mutually exclusive with collection_ticker)
            collection_ticker: Filter by collection ticker (mutually exclusive with series_ticker)
            with_nested_markets: Include markets within each event

        Returns:
            Dict with 'events' list and 'cursor'
        """
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
        if series_ticker:
            params["series_ticker"] = series_ticker
        if collection_ticker:
            params["collection_ticker"] = collection_ticker
        if with_nested_markets:
            params["with_nested_markets"] = "true"

        response = self.client.get("/events/multivariate", params=params)
        response.raise_for_status()
        return response.json()

    def get_event_candlesticks(
        self,
        series_ticker: str,
        event_ticker: str,
        start_ts: int,
        end_ts: int,
        period_interval: int = 60
    ) -> Dict[str, Any]:
        """
        Get candlestick data aggregated across all markets in an event

        Args:
            series_ticker: Series ticker
            event_ticker: Event ticker
            start_ts: Start timestamp (Unix timestamp)
            end_ts: End timestamp (Unix timestamp)
            period_interval: Period length in minutes (1, 60, or 1440)

        Returns:
            Dict with 'market_tickers', 'market_candlesticks', and 'adjusted_end_ts'
        """
        params = {
            "start_ts": start_ts,
            "end_ts": end_ts,
            "period_interval": period_interval
        }
        path = f"/series/{series_ticker}/events/{event_ticker}/candlesticks"
        response = self.client.get(path, params=params)
        response.raise_for_status()
        return response.json()

    # ========================================
    # Series
    # ========================================

    def get_series_list(
        self,
        category: Optional[str] = None,
        tags: Optional[str] = None,
        include_product_metadata: bool = False
    ) -> Dict[str, Any]:
        """
        Get list of series with optional filters

        Args:
            category: Filter by category
            tags: Filter by tags
            include_product_metadata: Whether to include product metadata

        Returns:
            Dict with 'series' array
        """
        params = {}
        if category:
            params["category"] = category
        if tags:
            params["tags"] = tags
        if include_product_metadata:
            params["include_product_metadata"] = "true"

        response = self.client.get("/series", params=params)
        response.raise_for_status()
        return response.json()

    def get_series(self, series_ticker: str) -> Dict[str, Any]:
        """
        Get information about a specific series

        Args:
            series_ticker: Series ticker

        Returns:
            Dict with 'series' object containing metadata, settlement sources, etc.
        """
        response = self.client.get(f"/series/{series_ticker}")
        response.raise_for_status()
        return response.json()
