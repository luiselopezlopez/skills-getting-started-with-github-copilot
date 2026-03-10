"""Tests for the activities listing endpoints."""


def test_get_activities_returns_expected_structure(client):
    # Arrange
    expected_activity_names = {
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Soccer Team",
        "Basketball Team",
        "Drama Club",
        "Art Studio",
        "Debate Club",
        "Science Club",
    }

    # Act
    response = client.get("/activities")
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert isinstance(payload, dict)
    assert set(payload.keys()) == expected_activity_names


def test_get_activities_includes_participants_list(client):
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.get("/activities")
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert activity_name in payload
    assert isinstance(payload[activity_name]["participants"], list)
