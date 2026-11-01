import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Student Result Application" in response.data


def test_passing_result(client):
    response = client.post(
        "/",
        data={"name": "Asha", "mark1": "80", "mark2": "70", "mark3": "90"},
    )
    assert response.status_code == 200
    assert b"Total: 240" in response.data
    assert b"Average: 80.00" in response.data
    assert b"PASS" in response.data


def test_failing_result(client):
    response = client.post(
        "/",
        data={"name": "Ravi", "mark1": "80", "mark2": "30", "mark3": "90"},
    )
    assert b"FAIL" in response.data


def test_invalid_marks_show_error(client):
    response = client.post(
        "/",
        data={"name": "Asha", "mark1": "120", "mark2": "70", "mark3": "90"},
    )
    assert b"Enter a name" in response.data