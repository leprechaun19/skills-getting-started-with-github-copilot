from urllib.parse import quote


def test_root_redirect(client):
    # Arrange
    # Act
    response = client.get("/", follow_redirects=False)
    # Assert
    assert response.status_code == 307
    assert "/static/index.html" in response.headers["location"]


def test_get_activities_success(client):
    # Arrange
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_success(client):
    # Arrange
    activity = "Chess Club"
    email = "teststudent@mergington.edu"
    # Act
    response = client.post(f"/activities/{quote(activity)}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json().get("message", "")

    # Verify via GET
    get_resp = client.get("/activities")
    assert email in get_resp.json()[activity]["participants"]


def test_signup_duplicate(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # pre-existing
    # Act
    response = client.post(f"/activities/{quote(activity)}/signup?email={email}")
    # Assert
    assert response.status_code == 400


def test_signup_unknown_activity(client):
    # Arrange
    activity = "No Such Activity"
    email = "someone@mergington.edu"
    # Act
    response = client.post(f"/activities/{quote(activity)}/signup?email={email}")
    # Assert
    assert response.status_code == 404


def test_remove_participant_success(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"
    # Act
    response = client.delete(f"/activities/{quote(activity)}/participants?email={email}")
    # Assert
    assert response.status_code == 200

    # Verify via GET
    get_resp = client.get("/activities")
    assert email not in get_resp.json()[activity]["participants"]


def test_remove_participant_not_found(client):
    # Arrange
    activity = "Chess Club"
    email = "nonexistent@mergington.edu"
    # Act
    response = client.delete(f"/activities/{quote(activity)}/participants?email={email}")
    # Assert
    assert response.status_code == 404


def test_remove_participant_unknown_activity(client):
    # Arrange
    activity = "No Such Activity"
    email = "someone@mergington.edu"
    # Act
    response = client.delete(f"/activities/{quote(activity)}/participants?email={email}")
    # Assert
    assert response.status_code == 404
