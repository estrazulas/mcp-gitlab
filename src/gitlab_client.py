import httpx
from typing import List, Dict, Optional
import os
import yaml

def expand_env_vars(obj):
    """Recursively expand environment variables in strings within a dict/list structure."""
    if isinstance(obj, str):
        return os.path.expandvars(obj)
    elif isinstance(obj, dict):
        return {k: expand_env_vars(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [expand_env_vars(item) for item in obj]
    else:
        return obj

class GitLabClient:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url.rstrip('/')
        self.token = token
        self.client = httpx.AsyncClient(timeout=30.0)

    async def list_projects(
        self,
        search: Optional[str] = None,
        membership: bool = True,
        per_page: int = 100,
    ) -> List[Dict]:
        url = f"{self.base_url}/api/v4/projects"
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {
            "simple": "true",
            "membership": str(membership).lower(),
            "per_page": per_page,
            "page": 1,
            "order_by": "last_activity_at",
            "sort": "desc",
        }

        if search:
            params["search"] = search

        projects: List[Dict] = []
        page = 1

        try:
            while True:
                request_params = params.copy()
                request_params["page"] = page

                response = await self.client.get(url, headers=headers, params=request_params)
                if response.status_code == 401:
                    raise ValueError("Token expired or invalid")
                elif response.status_code != 200:
                    raise ValueError(f"GitLab API error: {response.status_code} - {response.text}")

                page_items = response.json()
                if not isinstance(page_items, list):
                    raise ValueError("Unexpected GitLab response for project listing")

                projects.extend(page_items)

                next_page = response.headers.get("X-Next-Page")
                if not next_page:
                    break

                page = int(next_page)

            return projects
        except httpx.RequestError as e:
            raise ValueError(f"Request failed: {str(e)}")

    async def list_issues(
        self,
        project_id: str,
        assignee_username: Optional[str] = None,
        milestone: Optional[str] = None,
        labels: Optional[str] = None,
        state: str = 'opened'
    ) -> List[Dict]:
        url = f"{self.base_url}/api/v4/projects/{project_id}/issues"
        params = {'state': state}
        if assignee_username:
            params['assignee_username'] = assignee_username
        if milestone:
            params['milestone'] = milestone
        if labels:
            params['labels'] = labels

        headers = {"Authorization": f"Bearer {self.token}"}

        try:
            response = await self.client.get(url, headers=headers, params=params)
            if response.status_code == 401:
                raise ValueError("Token expired or invalid")
            elif response.status_code == 404:
                raise ValueError("Project not found")
            elif response.status_code != 200:
                raise ValueError(f"GitLab API error: {response.status_code} - {response.text}")
            
            issues = response.json()
            return issues
        except httpx.RequestError as e:
            raise ValueError(f"Request failed: {str(e)}")

    async def close(self):
        await self.client.aclose()

def load_config(config_path: str = 'config.yaml') -> Dict:
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return expand_env_vars(config)

def create_client() -> GitLabClient:
    config = load_config()
    token = os.getenv(config['gitlab']['token_env_var'])
    if not token:
        raise ValueError(f"Environment variable {config['gitlab']['token_env_var']} not set")
    return GitLabClient(config['gitlab']['base_url'], token)