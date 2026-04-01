import pytest
from unittest.mock import Mock, patch
import httpx
from src.gitlab_client import GitLabClient

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