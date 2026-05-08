<div align="center">

# Crypto Tracker Ai MCP

**MCP server for crypto tracker ai mcp operations**

[![PyPI](https://img.shields.io/pypi/v/meok-crypto-tracker-ai-mcp)](https://pypi.org/project/meok-crypto-tracker-ai-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MEOK AI Labs](https://img.shields.io/badge/MEOK_AI_Labs-MCP_Server-purple)](https://meok.ai)

</div>

## Overview

Crypto Tracker Ai MCP provides AI-powered tools via the Model Context Protocol (MCP).

## Tools

| Tool | Description |
|------|-------------|
| `track_price` | Get the current price, 24h change, and market cap for a cryptocurrency symbol (e |
| `compare_cryptos` | Compare multiple cryptocurrencies side by side. Provide comma-separated symbols  |
| `calculate_portfolio` | Calculate total portfolio value from holdings. Provide as 'BTC:0.5,ETH:10,SOL:10 |
| `get_market_cap` | Get the top cryptocurrencies ranked by market capitalisation. Returns up to top_ |

## Installation

```bash
pip install meok-crypto-tracker-ai-mcp
```

## Usage with Claude Desktop

Add to your Claude Desktop MCP config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "crypto-tracker-ai": {
      "command": "python",
      "args": ["-m", "meok_crypto_tracker_ai_mcp.server"]
    }
  }
}
```

## Usage with FastMCP

```python
from mcp.server.fastmcp import FastMCP

# This server exposes 4 tool(s) via MCP
# See server.py for full implementation
```

## License

MIT © [MEOK AI Labs](https://meok.ai)
