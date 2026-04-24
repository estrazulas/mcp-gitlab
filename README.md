# MCP GitLab Issues Server

A Model Context Protocol (MCP) server for listing GitLab issues with filters.

## Features

- List issues from GitLab projects
- List accessible GitLab projects to infer the correct project path
- Filter by user, project, milestone, and labels
- Authenticate with GitLab application token (read-only)
- Run locally in Docker

## Setup

1. Clone the repository
2. Config .env using .env.example as base
3. Insert your gitlab personal token
4. Run docker
   
## Docker

Build and run with Docker:

```bash
# Start MCP SERVER
docker compose up -d --build

# GET LOGS
docker compose logs -f

# REMOVE MCP_SERVER FROM DOCKER
docker compose down
```

## Dev Containers (optional)

For a complete development environment without installing anything locally, use VS Code Dev Containers:

1. Open the project in VS Code
2. When prompted, click "Reopen in Container" or use Command Palette: `Dev Containers: Reopen in Container`
3. The container will build and start the MCP server automatically on port 8000

The Dev Container includes:
- Python environment with all dependencies
- VS Code extensions for Python development
- MCP server running in the background
- Port forwarding for easy access

## Configuration (required)

The server uses environment variables for configuration. You can set them directly or use a `.env` file:

- `GITLAB_BASE_URL`: Your GitLab instance URL (default: https://git.yourorg.edu.br)
- `GITLAB_TOKEN`: Your GitLab application token (required)

### Using .env file (recommended)

1. Copy the example file: `cp .env.example .env`
2. Edit `.env` with your actual values:
   ```env
   GITLAB_BASE_URL=https://git.yourorg.edu.br
   GITLAB_TOKEN=glpat-your-actual-token-here
   ```

The server will automatically load variables from the `.env` file.

## Claude Client Integration

### 1. Start the MCP Server

Make sure the server is running on `http://127.0.0.1:8000/sse`
With NodeJS you can confirm tools usage with

```bash
npx @modelcontextprotocol/inspector http://127.0.0.1:8000/sse

```

### 2. Configure 

Create the MCP Configuration File
Create .vscode/mcp.json in your project:

```json
{
  "servers": {
    "gitlab-issues": {
      "type": "sse",
      "url": "http://127.0.0.1:8000/sse",
      "headers": {},
      "tools": [
        "list_projects",
        "list_issues"
      ]
    }
  }
}
```

With Claude

```bash
claude mcp add gitlab-issues sse http://127.0.0.1:8000/sse

```

### 3. Restart VSCode or Claude

Close and reopen AI CLI for changes to take effect.

### 4. Examples

Once connected, simply ask about your GitLab issues:

- "List my GitLab projects"
- "Show me the tools available in this MCP server"
- "Find the GitLab projects named xyz and xpto, then list all issues assigned to daniel.estrazulas"
- "List all open issues for xyz assigned to daniel.estrazulas"
- *"List all open issues in project myproject"*
- *"Show me issues assigned to john.doe"*
- *"Get bugs with label 'critical'"*
- *"List all closed issues"*

Typical flow:

1. Call `list_projects` to find the correct project or namespace path.
2. Use the returned `path_with_namespace` as `project_id` in `list_issues`.
3. Filter issues with `assignee_username`, `milestone`, `labels`, or `state` as needed.

### Available Tools

- `list_projects`: lists accessible GitLab projects so the LLM can infer the right path.
- `list_issues`: lists issues for a single project with optional filters.

Claude/VSCode can call `list_projects` first to infer the right `path_with_namespace`, then call `list_issues` automatically.

## Available Tool: `list_issues`

Parameters:

- `project_id`: The ID or path of the GitLab project (required) 
- `assignee_username`: Filter by assignee username (optional)
- `milestone`: Filter by milestone title (optional)
- `labels`: Comma-separated list of labels (optional)
- `state`: Issue state - `opened`, `closed`, or `all` (default: `opened`)

## Available Tool: `list_projects`

Parameters:

- `search`: Optional search term to narrow the project list by name or path
- `membership`: Limit to projects the token has membership in, which is the default and usually the best fit for inference
- `per_page`: Page size used when fetching projects from GitLab

Use the returned `path_with_namespace` value with `list_issues`.

## Inspect MCP

```bash
npx @modelcontextprotocol/inspector http://127.0.0.1:8000/sse
```