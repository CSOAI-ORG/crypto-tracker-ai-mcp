#!/usr/bin/env python3
"""Crypto Tracker AI — track cryptocurrency prices, portfolios, and market data. MEOK AI Labs."""
import sys, os
sys.path.insert(0, os.path.expanduser('~/clawd/meok-labs-engine/shared'))
from auth_middleware import check_access

import json
from datetime import datetime, timezone
from collections import defaultdict
from mcp.server.fastmcp import FastMCP

FREE_DAILY_LIMIT = 15
_usage = defaultdict(list)
def _rl(c="anon"):
    now = datetime.now(timezone.utc)
    _usage[c] = [t for t in _usage[c] if (now-t).total_seconds() < 86400]
    if len(_usage[c]) >= FREE_DAILY_LIMIT: return json.dumps({"error": f"Limit {FREE_DAILY_LIMIT}/day"})
    _usage[c].append(now); return None

# Simulated market data (replace with live API in production)
_PRICES = {
    "BTC": {"price": 65000.00, "change_24h": 2.3, "market_cap": 1280000000000},
    "ETH": {"price": 3400.00, "change_24h": -0.8, "market_cap": 408000000000},
    "SOL": {"price": 145.00, "change_24h": 5.1, "market_cap": 63000000000},
    "ADA": {"price": 0.45, "change_24h": -1.2, "market_cap": 16000000000},
    "DOT": {"price": 7.20, "change_24h": 0.4, "market_cap": 10000000000},
    "AVAX": {"price": 35.50, "change_24h": 3.7, "market_cap": 13000000000},
    "LINK": {"price": 14.80, "change_24h": 1.9, "market_cap": 8700000000},
    "MATIC": {"price": 0.72, "change_24h": -0.3, "market_cap": 7200000000},
    "DOGE": {"price": 0.082, "change_24h": -2.1, "market_cap": 11500000000},
    "XRP": {"price": 0.52, "change_24h": 0.6, "market_cap": 28000000000},
}

# In-memory portfolio store
_portfolios: dict[str, dict[str, float]] = {}

mcp = FastMCP("crypto-tracker-ai", instructions="Track cryptocurrency prices, compare assets, and manage portfolios. By MEOK AI Labs.")


@mcp.tool()
def track_price(symbol: str, api_key: str = "") -> str:
    """Get the current price, 24h change, and market cap for a cryptocurrency symbol (e.g. BTC, ETH, SOL)."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": "https://meok.ai/pricing"})
    if err := _rl(): return err
    sym = symbol.upper()
    if sym not in _PRICES:
        available = ", ".join(sorted(_PRICES.keys()))
        return json.dumps({"error": f"Unknown symbol '{sym}'. Available: {available}"})
    data = _PRICES[sym]
    return json.dumps({
        "symbol": sym,
        "price_usd": data["price"],
        "change_24h_pct": data["change_24h"],
        "market_cap_usd": data["market_cap"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }, indent=2)


@mcp.tool()
def compare_cryptos(symbols: str, api_key: str = "") -> str:
    """Compare multiple cryptocurrencies side by side. Provide comma-separated symbols (e.g. 'BTC,ETH,SOL')."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": "https://meok.ai/pricing"})
    if err := _rl(): return err
    syms = [s.strip().upper() for s in symbols.split(",") if s.strip()]
    if len(syms) < 2:
        return json.dumps({"error": "Provide at least 2 comma-separated symbols to compare"})
    results = []
    for sym in syms:
        if sym in _PRICES:
            d = _PRICES[sym]
            results.append({
                "symbol": sym,
                "price_usd": d["price"],
                "change_24h_pct": d["change_24h"],
                "market_cap_usd": d["market_cap"],
            })
        else:
            results.append({"symbol": sym, "error": "not found"})
    # Rank by market cap
    ranked = sorted([r for r in results if "error" not in r], key=lambda x: x["market_cap_usd"], reverse=True)
    return json.dumps({
        "comparison": results,
        "ranked_by_market_cap": [r["symbol"] for r in ranked],
        "best_24h_performer": max([r for r in results if "error" not in r], key=lambda x: x["change_24h_pct"])["symbol"] if ranked else None,
    }, indent=2)


@mcp.tool()
def calculate_portfolio(holdings: str, api_key: str = "") -> str:
    """Calculate total portfolio value from holdings. Provide as 'BTC:0.5,ETH:10,SOL:100' format."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": "https://meok.ai/pricing"})
    if err := _rl(): return err
    items = {}
    for pair in holdings.split(","):
        pair = pair.strip()
        if ":" not in pair:
            return json.dumps({"error": f"Invalid format '{pair}'. Use SYMBOL:AMOUNT (e.g. BTC:0.5)"})
        sym, amt = pair.split(":", 1)
        try:
            items[sym.strip().upper()] = float(amt.strip())
        except ValueError:
            return json.dumps({"error": f"Invalid amount in '{pair}'"})
    breakdown = []
    total = 0.0
    for sym, amount in items.items():
        if sym not in _PRICES:
            breakdown.append({"symbol": sym, "amount": amount, "error": "price not found"})
            continue
        value = amount * _PRICES[sym]["price"]
        total += value
        breakdown.append({
            "symbol": sym,
            "amount": amount,
            "price_usd": _PRICES[sym]["price"],
            "value_usd": round(value, 2),
        })
    # Add allocation percentages
    for item in breakdown:
        if "value_usd" in item and total > 0:
            item["allocation_pct"] = round(item["value_usd"] / total * 100, 1)
    return json.dumps({
        "total_value_usd": round(total, 2),
        "holdings": breakdown,
        "num_assets": len(items),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }, indent=2)


@mcp.tool()
def get_market_cap(top_n: int = 5, api_key: str = "") -> str:
    """Get the top cryptocurrencies ranked by market capitalisation. Returns up to top_n results (default 5)."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": "https://meok.ai/pricing"})
    if err := _rl(): return err
    top_n = max(1, min(top_n, len(_PRICES)))
    ranked = sorted(_PRICES.items(), key=lambda x: x[1]["market_cap"], reverse=True)[:top_n]
    entries = []
    for rank, (sym, data) in enumerate(ranked, 1):
        entries.append({
            "rank": rank,
            "symbol": sym,
            "price_usd": data["price"],
            "market_cap_usd": data["market_cap"],
            "change_24h_pct": data["change_24h"],
        })
    total_market_cap = sum(d["market_cap"] for d in _PRICES.values())
    return json.dumps({
        "top_assets": entries,
        "total_tracked_market_cap_usd": total_market_cap,
        "assets_tracked": len(_PRICES),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }, indent=2)


if __name__ == "__main__":
    mcp.run()
