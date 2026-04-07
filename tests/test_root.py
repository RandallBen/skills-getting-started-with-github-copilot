"""Tests for the root endpoint (GET /)"""

import pytest


def test_root_redirects_to_index_html(client):
    """Test that the root endpoint redirects to /static/index.html
    
    Arrange: Prepare the test client
    Act: Make a GET request to the root endpoint
    Assert: Verify redirect status code and location
    """
    # Arrange
    # Client is provided by conftest.py fixture
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code in [301, 302, 303, 307, 308]  # Any redirect status
    assert response.headers["location"] == "/static/index.html"


def test_root_redirect_follows_to_html(client):
    """Test that following the root redirect leads to the HTML file
    
    Arrange: Prepare the test client
    Act: Make a GET request following redirects
    Assert: Verify the final response contains HTML content
    """
    # Arrange
    # Client is provided by conftest.py fixture
    
    # Act
    response = client.get("/", follow_redirects=True)
    
    # Assert
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
