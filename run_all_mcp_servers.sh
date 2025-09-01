#!/bin/bash
# Script to start all MCP servers in separate terminals on Mac/Linux
uv run src/mcp/accounts.py &
uv run src/mcp/address_book.py &
uv run src/mcp/mcd.py &
uv run src/mcp/messages.py &
uv run src/mcp/preferences.py &
uv run src/mcp/tasks.py &
echo "All MCP servers started in background"
