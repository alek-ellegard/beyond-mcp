#!/usr/bin/env python3
"""
Formatting and display helper functions for Kalshi CLI
"""

from typing import Dict, Any, Optional
from datetime import datetime


def format_price_cents(cents: Optional[int]) -> str:
    """Format price from cents"""
    if cents is None:
        return "N/A"
    return f"{cents}¢"


def format_price_dollars(cents: Optional[int]) -> str:
    """Format price as dollars"""
    if cents is None:
        return "$0.00"
    return f"${cents / 100:.2f}"


def format_percentage(cents: Optional[int]) -> str:
    """Format price as percentage"""
    if cents is None:
        return "0%"
    return f"{cents}%"


def format_timestamp(ts: Optional[str]) -> str:
    """Format ISO timestamp to human-readable"""
    if not ts:
        return "N/A"
    try:
        dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
    except:
        return str(ts)


def format_market_summary(market: Dict[str, Any]) -> str:
    """Format a market as a single line summary"""
    ticker = market.get('ticker', 'N/A')
    title = market.get('title', market.get('yes_sub_title', 'N/A'))
    yes_price = market.get('yes_bid', market.get('last_price', 0))
    volume = market.get('volume', 0)

    # Truncate long titles
    if len(title) > 60:
        title = title[:57] + "..."

    return f"{ticker}: {title} | Yes: {yes_price}¢ | Vol: {format_price_dollars(volume)}"


def print_market_detail(market: Dict[str, Any]) -> None:
    """Pretty print detailed market information"""
    print(f"\n{'='*80}")
    print(f"Market: {market.get('ticker', 'N/A')}")
    print(f"{'='*80}")

    print(f"\nTitle: {market.get('title', 'N/A')}")
    print(f"Subtitle: {market.get('subtitle', 'N/A')}")
    print(f"Status: {market.get('status', 'N/A')}")
    print(f"Category: {market.get('category', 'N/A')}")

    # Prices
    yes_bid = market.get('yes_bid')
    yes_ask = market.get('yes_ask')
    no_bid = market.get('no_bid')
    no_ask = market.get('no_ask')
    last_price = market.get('last_price')

    print(f"\nCurrent Prices:")
    print(f"  Yes Bid: {format_price_cents(yes_bid)} | Yes Ask: {format_price_cents(yes_ask)}")
    print(f"  No Bid:  {format_price_cents(no_bid)} | No Ask:  {format_price_cents(no_ask)}")
    print(f"  Last Trade: {format_price_cents(last_price)}")

    # Volume and Interest
    volume = market.get('volume', 0)
    volume_24h = market.get('volume_24h', 0)
    open_interest = market.get('open_interest', 0)

    print(f"\nTrading Activity:")
    print(f"  Total Volume: {format_price_dollars(volume)}")
    print(f"  24h Volume: {format_price_dollars(volume_24h)}")
    print(f"  Open Interest: {format_price_dollars(open_interest)}")

    # Timing
    print(f"\nSchedule:")
    print(f"  Opens: {format_timestamp(market.get('open_time'))}")
    print(f"  Closes: {format_timestamp(market.get('close_time'))}")
    if market.get('expected_expiration_time'):
        print(f"  Expected Expiration: {format_timestamp(market.get('expected_expiration_time'))}")

    # Rules
    if market.get('rules_primary'):
        print(f"\nRules: {market.get('rules_primary')[:200]}")

    print(f"\n{'='*80}")


def print_event_detail(event_data: Dict[str, Any]) -> None:
    """Pretty print event information"""
    event = event_data.get('event', event_data)

    print(f"\n{'='*80}")
    print(f"Event: {event.get('event_ticker', 'N/A')}")
    print(f"{'='*80}")

    print(f"\nTitle: {event.get('title', 'N/A')}")
    print(f"Series: {event.get('series_ticker', 'N/A')}")
    print(f"Category: {event.get('category', 'N/A')}")
    print(f"Mutually Exclusive: {event.get('mutually_exclusive', False)}")

    # Markets
    markets = event_data.get('markets', event.get('markets', []))
    if markets:
        print(f"\nMarkets ({len(markets)}):")
        for i, market in enumerate(markets[:5], 1):
            ticker = market.get('ticker', 'N/A')
            title = market.get('title', market.get('yes_sub_title', 'N/A'))[:50]
            print(f"  {i}. {ticker}: {title}")

        if len(markets) > 5:
            print(f"  ... and {len(markets) - 5} more")

    print(f"\n{'='*80}")


def json_serial(obj: Any) -> Any:
    """JSON serializer for objects not serializable by default"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")
