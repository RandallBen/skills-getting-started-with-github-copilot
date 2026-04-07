"""Tests for the unregister endpoint (DELETE /activities/{activity_name}/unregister)"""

import pytest


def test_unregister_success_with_registered_email(client, valid_activity_name):
    """Test successful unregister when email is registered for an activity
    
    Arrange: Prepare activity with a registered participant
    Act: Make a DELETE request to unregister the participant
    Assert: Verify successful unregister response
    """
    # Arrange
    activity_name = valid_activity_name  # "Chess Club"
    email = "michael@mergington.edu"  # Pre-registered in Chess Club
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]


def test_unregister_removes_participant_from_activity(client, valid_activity_name):
    """Test that unregister actually removes the participant from the activity
    
    Arrange: Get initial state, prepare registered email
    Act: Make DELETE request to unregister, then GET activities
    Assert: Verify participant is removed and participant count decreases
    """
    # Arrange
    activity_name = valid_activity_name  # "Chess Club"
    email = "michael@mergington.edu"
    
    # Get initial state
    initial_response = client.get("/activities")
    initial_participants = initial_response.json()[activity_name]["participants"]
    initial_count = len(initial_participants)
    assert email in initial_participants
    
    # Act
    unregister_response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert unregister_response.status_code == 200
    
    # Verify participant was removed
    activities_response = client.get("/activities")
    updated_participants = activities_response.json()[activity_name]["participants"]
    assert email not in updated_participants
    assert len(updated_participants) == initial_count - 1


def test_unregister_fails_with_invalid_activity(client):
    """Test unregister fails when activity name does not exist
    
    Arrange: Prepare invalid activity name and valid email
    Act: Make DELETE request with non-existent activity
    Assert: Verify 404 error response
    """
    # Arrange
    activity_name = "NonExistentClub"
    email = "student@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_unregister_fails_when_email_not_registered(client, valid_activity_name, valid_email):
    """Test unregister fails when email is not registered for the activity
    
    Arrange: Prepare activity and email that is not registered
    Act: Make DELETE request with unregistered email
    Assert: Verify 400 error response
    """
    # Arrange
    activity_name = valid_activity_name  # "Chess Club"
    email = valid_email  # "newstudent@mergington.edu" - never signed up
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "not registered" in data["detail"].lower() or "not" in data["detail"].lower()


def test_unregister_response_format(client, valid_activity_name):
    """Test that unregister response has expected format
    
    Arrange: Prepare valid unregister request with registered email
    Act: Make DELETE request and examine response
    Assert: Verify response contains expected fields
    """
    # Arrange
    activity_name = valid_activity_name
    email = "michael@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "message" in data
    assert isinstance(data["message"], str)


def test_unregister_then_signup_again(client, valid_activity_name):
    """Test that a participant can unregister and then signup again
    
    Arrange: Prepare activity with participant registered
    Act: Unregister, then signup the same email again
    Assert: Verify participant can re-register after unregistering
    """
    # Arrange
    activity_name = valid_activity_name  # "Chess Club"
    email = "michael@mergington.edu"
    
    # Act: First unregister
    unregister_response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    assert unregister_response.status_code == 200
    
    # Verify unregistered
    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]
    
    # Act: Sign up again
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert signup_response.status_code == 200
    activities = client.get("/activities").json()
    assert email in activities[activity_name]["participants"]


def test_unregister_double_unregister_fails(client, valid_activity_name):
    """Test that unregistering twice fails the second time
    
    Arrange: Prepare activity with registered participant
    Act: Unregister once (success), then attempt to unregister again
    Assert: First succeeds, second fails with 400
    """
    # Arrange
    activity_name = valid_activity_name  # "Chess Club"
    email = "michael@mergington.edu"
    
    # Act: First unregister
    response1 = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert: First should succeed
    assert response1.status_code == 200
    
    # Act: Try to unregister again
    response2 = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert: Second should fail (not registered anymore)
    assert response2.status_code == 400
