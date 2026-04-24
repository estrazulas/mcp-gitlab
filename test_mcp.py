#!/usr/bin/env python3
"""
Test script for the GitLab Issues MCP server
"""
import asyncio

import json

from mcp.client.session import ClientSession
from mcp.client.sse import sse_client

async def test_mcp_server():
    """Test the MCP server through the SSE transport."""

    # MCP server URL
    url = "http://127.0.0.1:8000/sse"

    async with sse_client(url) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            print("Initializing MCP session...")
            init_result = await session.initialize()
            print(f"Initialized: {json.dumps(init_result.model_dump(mode='json'), indent=2)}")

            print("\nListing available tools...")
            tools_result = await session.list_tools()
            print(f"Tools: {json.dumps(tools_result.model_dump(mode='json'), indent=2)}")

            print("\nListing available prompts...")
            prompts_result = await session.list_prompts()
            print(f"Prompts: {json.dumps(prompts_result.model_dump(mode='json'), indent=2)}")

            print("\nFetching prompt content...")
            prompt_result = await session.get_prompt("listar_issues_projetos")
            print(f"Prompt: {json.dumps(prompt_result.model_dump(mode='json'), indent=2)}")

            print("\nCalling list_issues tool...")
            try:
                call_result = await session.call_tool(
                    "list_issues",
                    {
                        "project_id": "545",
                        "state": "opened",
                    },
                )
                print(f"Call result: {json.dumps(call_result.model_dump(mode='json'), indent=2)}")
            except Exception as exc:
                print(f"Tool call error: {exc}")

if __name__ == "__main__":
    asyncio.run(test_mcp_server())