#!/bin/bash
echo "$(date): Starting MCP server..." >> /workspaces/mcp_gitlab_list_issues/server.log
cd /workspaces/mcp_gitlab_list_issues
python -m src.server >> /workspaces/mcp_gitlab_list_issues/server.log 2>&1 &
echo "$(date): Server started with PID $!" >> /workspaces/mcp_gitlab_list_issues/server.log