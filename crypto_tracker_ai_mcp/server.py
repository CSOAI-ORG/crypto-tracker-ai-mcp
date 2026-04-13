from mcp.server.fastmcp import FastMCP

mcp = FastMCP("crypto-tracker")

CRYPTO_PRICES = {
    "BTC": 67500.0,
    "ETH": 3450.0,
    "SOL": 145.0,
    "ADA": 0.55,
    "DOT": 7.2,
    "XRP": 0.62,
    "DOGE": 0.16,
    "AVAX": 35.4,
}

@mcp.tool()
def get_price(symbol: str) -> dict:
    """Get current crypto price."""
    sym = symbol.upper()
    price = CRYPTO_PRICES.get(sym)
    if price is None:
        return {"error": "Symbol not supported", "supported": list(CRYPTO_PRICES.keys())}
    return {"symbol": sym, "price_usd": price}

@mcp.tool()
def calculate_portfolio_value(holdings: dict) -> dict:
    """Calculate portfolio value from holdings dict {symbol: amount}."""
    total = 0.0
    breakdown = {}
    for sym, amount in holdings.items():
        price = CRYPTO_PRICES.get(sym.upper(), 0.0)
        value = amount * price
        breakdown[sym.upper()] = {"amount": amount, "price": price, "value": round(value, 2)}
        total += value
    return {"total_value_usd": round(total, 2), "breakdown": breakdown}

@mcp.tool()
def calculate_pnl(symbol: str, amount: float, cost_basis: float) -> dict:
    """Calculate profit/loss."""
    sym = symbol.upper()
    current_price = CRYPTO_PRICES.get(sym)
    if current_price is None:
        return {"error": "Symbol not supported"}
    current_value = amount * current_price
    invested = amount * cost_basis
    pnl = current_value - invested
    pnl_percent = (pnl / invested) * 100 if invested != 0 else 0.0
    return {
        "symbol": sym,
        "pnl_usd": round(pnl, 2),
        "pnl_percent": round(pnl_percent, 2),
        "current_value_usd": round(current_value, 2),
    }

def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
