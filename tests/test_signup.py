"""Tests for the signup endpoint (POST /activities/{activity_name}/signup)"""

import pytest


def test_signup_success_with_valid_activity_and_email(client, valid_activity_name, valid_email):
    """Test successful signup with valid activity and new email
    
    Arrange: Prepare valid activity name and email that is not pre-registered
    Act: Make a POST request to signup endpoint
    Assert: Verify response indicates success and participant is added
    """
    # Arrange
    activity_name = valid_activity_name  # "Chess Club"
    email = valid_email  # "newstudent@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]


def test_signup_adds_participant_to_activity(client, valid_activity_name, valid_email):
    """Test that signup actually adds the participant to the activity
    
    Arrange: Prepare valid activity and email, get initial participant list
    Act: Make a POST request to signup endpoint, then GET activities
    Assert: Verify participant appears in the activity's participant list
    """
    # Arrange
    activity_name = valid_activity_name  # "Chess Club"
    email = valid_email  # "newstudent@mergington.edu"
    
    # Get initial activities to verify email is not already present
    initial_response = client.get("/activities")
    initial_participants = initial_response.json()[activity_name]["participants"]
    assert email not in initial_participants
    
    # Act
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert signup_response.status_code == 200
    
    # Verify participant was added
    activities_response = client.get("/activities")
    updated_participants = activities_response.json()[activity_name]["participants"]
    assert email in updated_participants
    assert len(updated_participants) == len(initial_participants) + 1


def test_signup_fails_with_invalid_activity(client, invalid_activity_name, valid_email):
    """Test signup fails when activity name does not exist
    
    Arrange: Prepare invalid activity name and valid email
    Act: Make a POST request to signup with non-existent activity
    Assert: Verify 404 error response
    """
    # Arrange
    activity_name = invalid_activity_name  # "NonExistentClub"
    email = valid_email
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_signup_fails_with_duplicate_email(client, valid_activity_name, registered_email):
    """Test signup fails when email is already registered for the activity
    
    Arrange: Prepare activity and an email already registered
    Act: Make a POST request to signup with duplicate email
    Assert: Verify 400 error response indicating already signed up
    """
    # Arrange
    activity_name = valid_activity_name  # "Chess Club"
    email = registered_email  # "michael@mergington.edu" (already in Chess Club)
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already" in data["detail"].lower() or "signed up" in data["detail"].lower()


def test_signup_multiple_students_for_same_activity(client):
    """Test that multiple students can sign up for the same activity
    
    Arrange: Prepare activity and multiple different emails
    Act: Sign up multiple students for the same activity
    Assert: Verify all signups succeed and participants are added
    
    Note: Current app implementation does not enforce max_participants limit
    """
    # Arrange
    activity_name = "Basketball Team"  # Has max_participants: 15
    
    # Get current participant count
    activities = client.get("/activities").json()
    initial_count = len(activities[activity_name]["participants"])
    
    # Act: Sign up 3 additional students
    new_emails = ["new1@mergington.edu", "new2@mergington.edu", "new3@mergington.edu"]
    for email in new_emails:
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
    
    # Assert: Verify all were added
    activities = client.get("/activities").json()
    final_participants = activities[activity_name]["participants"]
    assert len(final_participants) == initial_count + 3
    for email in new_emails:
        assert email in final_participants


def test_signup_accepts_any_email_string(client, valid_activity_name):
    """Test that signup accepts various email formats (no strict validation)
    
    Arrange: Prepare activity and various email strings
    Act: Make POST requests with different email formats
    Assert: Verify signup accepts various email strings
    
    Note: Current app does not validate email format
    """
    # Arrange
    activity_name = valid_activity_name
    test_emails = [
        "simple@test.com",
        "with.dot@test.com",
        "with-dash@test.com",
        "number123@test.com"
    ]
    
    # Act & Assert
    for email in test_emails:
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # All should succeed since app doesn't validate format
        assert response.status_code == 200
        
        # Verify email was added
        activities = client.get("/activities").json()
        assert email in activities[activity_name]["participants"]


def test_signup_response_format(client, valid_activity_name, valid_email):
    """Test that signup response has expected format
    
    Arrange: Prepare valid signup request
    Act: Make signup request and examine response structure
    Assert: Verify response contains expected fields and format
    """
    # Arrange
    activity_name = valid_activity_name
    email = valid_email
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "message" in data
    assert isinstance(data["message"], str)
