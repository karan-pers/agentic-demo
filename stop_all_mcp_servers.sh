#!/bin/bash
# Script to start all MCP servers in separate terminals on Mac/Linux
kill $(lsof -t -i:10000)
kill $(lsof -t -i:10001)
kill $(lsof -t -i:10002)
kill $(lsof -t -i:10003)
kill $(lsof -t -i:10004)
kill $(lsof -t -i:10005)
echo "All MCP servers stopped"
