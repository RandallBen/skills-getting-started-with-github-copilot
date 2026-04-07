"""Tests for the activities endpoint (GET /activities)"""

import pytest


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all activities in the database
    
    Arrange: Prepare the test client
    Act: Make a GET request to /activities
    Assert: Verify response contains all 9 activities
    """
    # Arrange
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Swimming Club",
        "Art Studio",
        "Music Ensemble",
        "Debate Team",
        "Science Club"
    ]
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 9
    for activity_name in expected_activities:
        assert activity_name in data


def test_get_activities_returns_correct_structure(client):
    """Test that each activity has all required fields
    
    Arrange: Prepare the test client and define required fields
    Act: Make a GET request to /activities
    Assert: Verify each activity has description, schedule, max_participants, participants
    """
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    for activity_name, activity_details in data.items():
        assert isinstance(activity_details, dict)
        for field in required_fields:
            assert field in activity_details


def test_get_activities_participant_counts_are_correct(client):
    """Test that participant counts match the list of participants
    
    Arrange: Prepare the test client
    Act: Make a GET request to /activities
    Assert: Verify participant count equals length of participants list
    """
    # Arrange
    # Client is provided by conftest.py fixture
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    for activity_name, activity_details in data.items():
        participants = activity_details["participants"]
        assert isinstance(participants, list)
        # Verify list contains strings (emails)
        for participant in participants:
            assert isinstance(participant, str)


def test_get_activities_chess_club_has_initial_participants(client):
    """Test that Chess Club has the correct initial participants
    
    Arrange: Prepare the test client and expected initial participants
    Act: Make a GET request to /activities
    Assert: Verify Chess Club participants list is correct
    """
    # Arrange
    expected_chess_participants = ["michael@mergington.edu", "daniel@mergington.edu"]
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    chess_club = data["Chess Club"]
    assert set(chess_club["participants"]) == set(expected_chess_participants)


def test_get_activities_max_participants_are_positive_integers(client):
    """Test that max_participants are valid positive integers
    
    Arrange: Prepare the test client
    Act: Make a GET request to /activities
    Assert: Verify all max_participants values are positive integers
    """
    # Arrange
    # Client is provided by conftest.py fixture
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    for activity_name, activity_details in data.items():
        max_participants = activity_details["max_participants"]
        assert isinstance(max_participants, int)
        assert max_participants > 0
