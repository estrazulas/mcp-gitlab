#!/usr/bin/env python3
"""
Test script for the GitLab Issues MCP server
"""
import asyncio
import httpx
import json

async def test_mcp_server():
    """Test the MCP server by calling the list_issues tool"""

    # MCP server URL
    url = "http://127.0.0.1:8000/mcp"
    headers = {"Accept": "application/json"}

    async with httpx.AsyncClient() as client:
        try:
            # First, initialize the MCP session
            init_request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {
                        "name": "test-client",
                        "version": "1.0.0"
                    }
                }
            }

            print("Initializing MCP session...")
            response = await client.post(url, json=init_request, headers=headers)
            print(f"Init response: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"Response: {json.dumps(result, indent=2)}")
            else:
                print(f"Error: {response.text}")

            # List available tools
            tools_request = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list",
                "params": {}
            }

            print("\nListing available tools...")
            response = await client.post(url, json=tools_request, headers=headers)
            print(f"Tools response: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"Response: {json.dumps(result, indent=2)}")
            else:
                print(f"Error: {response.text}")

            # Call the list_issues tool with a real project ID
            call_request = {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {
                    "name": "list_issues",
                    "arguments": {
                        "project_id": "545",  # Real project ID found
                        "state": "opened"
                    }
                }
            }

            print("\nCalling list_issues tool...")
            response = await client.post(url, json=call_request, headers=headers)
            print(f"Call response: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"Result: {json.dumps(result, indent=2)}")
            else:
                print(f"Error response: {response.text}")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_mcp_server())