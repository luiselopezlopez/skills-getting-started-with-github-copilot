"""Tests for activity sign-up endpoint behavior."""


def test_signup_succeeds_for_new_student(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    activities_response = client.get("/activities")
    activities_payload = activities_response.json()

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in activities_payload[activity_name]["participants"]


def test_signup_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_returns_400_for_duplicate_student(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup", params={"email": existing_email}
    )

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up"}


def test_signup_flow_is_consistent_across_requests(client):
    # Arrange
    activity_name = "Debate Club"
    email = "flow.student@mergington.edu"

    # Act
    before_response = client.get("/activities")
    signup_response = client.post(
        f"/activities/{activity_name}/signup", params={"email": email}
    )
    after_response = client.get("/activities")

    before_payload = before_response.json()
    after_payload = after_response.json()

    # Assert
    assert before_response.status_code == 200
    assert signup_response.status_code == 200
    assert after_response.status_code == 200
    assert email not in before_payload[activity_name]["participants"]
    assert email in after_payload[activity_name]["participants"]