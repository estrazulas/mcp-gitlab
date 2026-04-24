import pytest
from unittest.mock import Mock, patch
import httpx
from src.gitlab_client import GitLabClient


@pytest.mark.asyncio
async def test_list_projects_success():
    client = GitLabClient("https://example.com", "token")

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {
            "id": 1,
            "name": "Project One",
            "path": "project-one",
            "path_with_namespace": "group/project-one",
            "description": "Demo project",
            "web_url": "https://example.com/group/project-one",
            "visibility": "private",
        }
    ]
    mock_response.headers = {}

    with patch.object(client.client, 'get', return_value=mock_response):
        projects = await client.list_projects()
        assert projects == [
            {
                "id": 1,
                "name": "Project One",
                "path": "project-one",
                "path_with_namespace": "group/project-one",
                "description": "Demo project",
                "web_url": "https://example.com/group/project-one",
                "visibility": "private",
            }
        ]


@pytest.mark.asyncio
async def test_list_projects_with_search_and_pagination():
    client = GitLabClient("https://example.com", "token")

    first_page = Mock()
    first_page.status_code = 200
    first_page.json.return_value = [
        {"id": 1, "name": "Project One", "path": "project-one", "path_with_namespace": "group/project-one", "web_url": "https://example.com/group/project-one"}
    ]
    first_page.headers = {"X-Next-Page": "2"}

    second_page = Mock()
    second_page.status_code = 200
    second_page.json.return_value = [
        {"id": 2, "name": "Project Two", "path": "project-two", "path_with_namespace": "group/project-two", "web_url": "https://example.com/group/project-two"}
    ]
    second_page.headers = {}

    with patch.object(client.client, 'get', side_effect=[first_page, second_page]) as mock_get:
        projects = await client.list_projects(search="project")

        assert len(projects) == 2
        assert projects[0]["path_with_namespace"] == "group/project-one"

        first_call_kwargs = mock_get.call_args_list[0].kwargs
        assert first_call_kwargs["params"]["search"] == "project"
        assert first_call_kwargs["params"]["page"] == 1
        assert first_call_kwargs["params"]["membership"] == "true"
        assert first_call_kwargs["headers"] == {"Authorization": "Bearer token"}

@pytest.mark.asyncio
async def test_list_issues_success():
    client = GitLabClient("https://example.com", "token")
    
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"id": 1, "title": "Test Issue"}]
    
    with patch.object(client.client, 'get', return_value=mock_response):
        issues = await client.list_issues("123")
        assert issues == [{"id": 1, "title": "Test Issue"}]

@pytest.mark.asyncio
async def test_list_issues_token_expired():
    client = GitLabClient("https://example.com", "token")
    
    mock_response = Mock()
    mock_response.status_code = 401
    mock_response.text = "Unauthorized"
    
    with patch.object(client.client, 'get', return_value=mock_response):
        with pytest.raises(ValueError, match="Token expired or invalid"):
            await client.list_issues("123")

@pytest.mark.asyncio
async def test_list_issues_project_not_found():
    client = GitLabClient("https://example.com", "token")
    
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.text = "Not Found"
    
    with patch.object(client.client, 'get', return_value=mock_response):
        with pytest.raises(ValueError, match="Project not found"):
            await client.list_issues("123")

@pytest.mark.asyncio
async def test_list_issues_with_filters():
    client = GitLabClient("https://example.com", "token")
    
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = []
    
    with patch.object(client.client, 'get', return_value=mock_response) as mock_get:
        await client.list_issues("123", assignee_username="user", milestone="v1.0", labels="bug,feature")
        
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert kwargs['params'] == {
            'state': 'opened',
            'assignee_username': 'user',
            'milestone': 'v1.0',
            'labels': 'bug,feature'
        }
        assert kwargs['headers'] == {"Authorization": "Bearer token"}