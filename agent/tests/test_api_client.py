from unittest.mock import Mock, patch

from app.services.api_client import SentinelAPIClient


@patch("app.services.api_client.requests.post")
def test_send_event_success(mock_post):

    mock_response = Mock()
    mock_response.raise_for_status.return_value = None

    mock_post.return_value = mock_response

    client = SentinelAPIClient()

    event = {
        "event_type": "PROCESS",
        "severity": "INFO",
        "source": "local-agent",
        "hostname": "test-machine",
        "description": "Test process",
    }

    result = client.send_event(event)

    assert result is True

    mock_post.assert_called_once()