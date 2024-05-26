from flask.testing import FlaskClient


def test_redirect_to_login(client: FlaskClient) -> None:
    """Test getting endpoint without session redirects to login page."""
    response = client.get("/", follow_redirects=True)
    assert len(response.history) == 1
    assert response.request.path == "/login"
