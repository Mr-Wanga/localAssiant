import httpx


url = "http://192.168.31.40:9000/mcp"


async def get_mcp_session_id(url: str):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"
    }

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "roots": {},
                "sampling": {}
            },
            "clientInfo": {
                "name": "init-server",
                "version": "1.0.0"
            }
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()

        session_id = response.headers['mcp-session-id']
    
    return session_id

async def get_mcp_result(url: str, session_id: str, tool_name: str, tool_params: dict):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "mcp-session-id": session_id
    }

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": tool_params
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        
        result = response.text
    
    return result

