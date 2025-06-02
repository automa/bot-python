def test_healthcheck_endpoint(client):
    """Test the healthcheck endpoint returns a 200 OK status."""
    response = client.get("/health")

    assert response.status_code == 200

    assert response.content == b""
