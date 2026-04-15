# Crypto Tracker AI MCP Server

> By [MEOK AI Labs](https://meok.ai) — Track cryptocurrency prices, compare assets, and manage portfolios

## Installation

```bash
pip install crypto-tracker-ai-mcp
```

## Usage

```bash
python server.py
```

## Tools

### `track_price`
Get the current price, 24h change, and market cap for a cryptocurrency (BTC, ETH, SOL, ADA, DOT, AVAX, LINK, MATIC, DOGE, XRP).

**Parameters:**
- `symbol` (str): Cryptocurrency symbol (e.g., 'BTC')

### `compare_cryptos`
Compare multiple cryptocurrencies side by side ranked by market cap.

**Parameters:**
- `symbols` (str): Comma-separated symbols (e.g., 'BTC,ETH,SOL')

### `calculate_portfolio`
Calculate total portfolio value from holdings.

**Parameters:**
- `holdings` (str): Holdings as 'BTC:0.5,ETH:10,SOL:100' format

### `get_market_cap`
Get the top cryptocurrencies ranked by market capitalisation.

**Parameters:**
- `top_n` (int): Number of results (default 5)

## Authentication

Free tier: 15 calls/day. Upgrade at [meok.ai/pricing](https://meok.ai/pricing) for unlimited access.

## License

MIT — MEOK AI Labs
