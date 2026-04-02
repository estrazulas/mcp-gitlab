import os
from pathlib import Path
from typing import Optional
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
import uvicorn
from urllib.parse import quote
from src.gitlab_client import GitLabClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set uvicorn host and port for Docker
os.environ['UVICORN_HOST'] = '0.0.0.0'
os.environ['UVICORN_PORT'] = '8000'
class Issue(BaseModel):
    id: int = Field(description="Issue ID")
    iid: int = Field(description="Internal Issue ID")
    title: str
    description: Optional[str]
    state: str
    created_at: str
    updated_at: str
    closed_at: Optional[str]
    labels: list[str]
    milestone: Optional[dict]
    assignee: Optional[dict]
    author: dict
    web_url: str

class ListIssuesResponse(BaseModel):
    issues: list[Issue]
    total_count: int
    message: Optional[str] = None

# Create MCP server with stateless HTTP
mcp = FastMCP("GitLab Issues Server")
app = mcp.sse_app

PROMPT_FILE_CANDIDATES = [
    Path(__file__).resolve().parent / "prompts" / "listar_issues_projetos.md",
    Path(__file__).resolve().parents[1] / "prompts" / "listar_issues_projetos.md",
]


def _load_prompt_text() -> str:
    for prompt_file in PROMPT_FILE_CANDIDATES:
        if prompt_file.exists():
            return prompt_file.read_text(encoding="utf-8")

    candidates = ", ".join(str(path) for path in PROMPT_FILE_CANDIDATES)
    raise FileNotFoundError(f"Prompt file not found. Checked: {candidates}")

@mcp.tool()
async def list_issues(
    project_id: str = Field(description="The ID or path of the GitLab project"),
    assignee_username: Optional[str] = Field(None, description="Filter by assignee username"),
    milestone: Optional[str] = Field(None, description="Filter by milestone title"),
    labels: Optional[str] = Field(None, description="Comma-separated list of labels"),
    state: str = Field("opened", description="Issue state: opened, closed, or all")
) -> ListIssuesResponse:
    """
    List GitLab issues for a project with optional filters.

    Returns issues matching the specified criteria. If no issues are found,
    returns an empty list with a message.
    """
    try:
        # Get config from environment
        base_url = os.getenv("GITLAB_BASE_URL")
        if not base_url:
            raise ValueError("GITLAB_BASE_URL environment variable is required")
        token = os.getenv("GITLAB_TOKEN")
        
        if not token:
            raise ValueError("GITLAB_TOKEN environment variable is required")
        
        client = GitLabClient(base_url, token)

        safe_project_id = quote(project_id, safe='')

        issues_data = await client.list_issues(
            project_id=safe_project_id,
            assignee_username=assignee_username,
            milestone=milestone,
            labels=labels,
            state=state
        )
        
        await client.close()
        
        issues = [Issue(**issue) for issue in issues_data]
        
        if not issues:
            return ListIssuesResponse(
                issues=[],
                total_count=0,
                message="No issues found matching the specified filters."
            )
        
        return ListIssuesResponse(
            issues=issues,
            total_count=len(issues)
        )
        
    except ValueError as e:
        # For expected errors like token expired, project not found
        return ListIssuesResponse(
            issues=[],
            total_count=0,
            message=str(e)
        )
    except Exception as e:
        return ListIssuesResponse(
            issues=[],
            total_count=0,
            message=f"Unexpected error: {str(e)}"
        )


@mcp.prompt(
    name="listar_issues_projetos",
    title="Listar issues por projetos",
    description="Prompt para gerar o relatório de issues dos projetos configurados"
)
def listar_issues_projetos_prompt() -> list[dict[str, str]]:
    return [
        {
            "role": "user",
            "content": _load_prompt_text()
        }
    ]
    
if __name__ == "__main__":
    # Deixamos o mcp.run gerenciar o servidor. 
    # Ele buscará as configurações de HOST e PORT nas variáveis de ambiente.
    mcp.run(transport="sse")