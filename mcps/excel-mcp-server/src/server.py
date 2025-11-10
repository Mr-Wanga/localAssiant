import json, os
from mcp.server.fastmcp import FastMCP
from mcp.types import CallToolResult, TextContent
from utils import find_candidate_blocks
from common.log import get_logger


logger = get_logger('excel-mcp')
folder = os.environ.get('EXCEL_FILES_PATH', '/app/data/uploadFiles')

mcp_server = FastMCP(
    "excel-mcp",
    host=os.environ.get("FASTMCP_HOST", "0.0.0.0"),
    port=int(os.environ.get("FASTMCP_PORT", "8017")),
    instructions="Excel MCP Server for manipulating Excel files"
)

@mcp_server.tool("detect_excel_tables")
def detect_excel_tables(excel_name: str) -> CallToolResult:
    """
    Args:
      excel_name (str): excel file name
    """
    path = os.path.join(folder, excel_name)
    try:
        blocks = find_candidate_blocks(path)
        if not blocks:
            logger.error(f"Extract Excel with {excel_name} failed: No tables detected in Excel")
            return CallToolResult(
                content=[TextContent(type='text', text="No tables detected in Excel")],
                isError=True
            )

        return CallToolResult(
                content=[TextContent(type='text', text=json.dumps(blocks, ensure_ascii=False, indent=2))],
            )
    except Exception as e:
        logger.error(f"Extract Excel with {excel_name} failed: {e}")
        return CallToolResult(
            content=[TextContent(type='text', text=f"Extract excel failed: {str(e)}")],
            isError=True
        )


if __name__ == "__main__":
    logger.info("Start Excel MCP")
    mcp_server.run(transport='streamable-http')