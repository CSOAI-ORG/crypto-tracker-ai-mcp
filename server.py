#!/usr/bin/env python3
"""MEOK AI Labs — crypto-tracker-ai-mcp MCP Server. Track cryptocurrency prices and portfolio value."""

import asyncio
import json
from datetime import datetime, timezone
from typing import Any

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent)
import mcp.types as types
import sys, os
sys.path.insert(0, os.path.expanduser("~/clawd/meok-labs-engine/shared"))
from auth_middleware import check_access
from collections import defaultdict
import json

FREE_DAILY_LIMIT = 15
_usage = defaultdict(list)
def _rl(c="anon"):
    now = datetime.now(timezone.utc)
    _usage[c] = [t for t in _usage[c] if (now-t).total_seconds() < 86400]
    if len(_usage[c]) >= FREE_DAILY_LIMIT: return json.dumps({"error": f"Limit {FREE_DAILY_LIMIT}/day"})
    _usage[c].append(now); return None

# In-memory store (replace with DB in production)
_store = {}

server = Server("crypto-tracker-ai")

@server.list_resources()
async def handle_list_resources() -> list[Resource]:
    return []

@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    return [
        Tool(name="get_crypto_price", description="Get crypto price", inputSchema={"type":"object","properties":{"symbol":{"type":"string"}},"required":["symbol"]}),
        Tool(name="portfolio_value", description="Calculate portfolio value", inputSchema={"type":"object","properties":{"holdings":{"type":"object"}},"required":["holdings"]}),
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: Any | None) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    args = arguments or {}
    api_key = args.get("api_key", "")
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return [TextContent(type="text", text=json.dumps({"error": msg, "upgrade_url": "https://meok.ai/pricing"}))]
    if err := _rl(): return [TextContent(type="text", text=err)]
    if name == "get_crypto_price":
        prices = {"BTC": 65000, "ETH": 3400, "SOL": 145}
        return [TextContent(type="text", text=json.dumps({"symbol": args["symbol"], "price": prices.get(args["symbol"], 0)}, indent=2))]
    if name == "portfolio_value":
        prices = {"BTC": 65000, "ETH": 3400, "SOL": 145}
        total = sum(v * prices.get(k, 0) for k, v in args["holdings"].items())
        return [TextContent(type="text", text=json.dumps({"portfolio_value": total}, indent=2))]
    return [TextContent(type="text", text=json.dumps({"error": "Unknown tool"}, indent=2))]

async def main():
    async with stdio_server(server._read_stream, server._write_stream) as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="crypto-tracker-ai",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={})))

if __name__ == "__main__":
    asyncio.run(main())