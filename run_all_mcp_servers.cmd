@echo off
REM Script to start all MCP servers in separate terminals
start cmd /k "uv run src\mcp\accounts.py"
start cmd /k "uv run src\mcp\mcd.py"
start cmd /k "uv run src\mcp\preferences.py"
start cmd /k "uv run src\mcp\tasks.py"
start cmd /k "uv run src\mcp\messages.py"
start cmd /k "uv run src\mcp\address_book.py"
echo All MCP servers started in separate terminals.
