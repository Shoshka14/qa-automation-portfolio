import os

import pytest
import requests

BASE_URL = os.getenv("API_BASE_URL", "https://restful-booker.herokuapp.com")
TIMEOUT = 15

pytestmark = pytest.mark.api

BOOKING = {
    "firstname": "QA",
    "lastname": "Portfolio",
    "totalprice": 120,
    "depositpaid": True,
    "bookingdates": {"checkin": "2027-01-10", "checkout": "2027-01-12"},
    "additionalneeds": "Breakfast",
}


@pytest.fixture(scope="session")
def token():
    # Public practice credentials documented by the demo API.
    creds = {
        "username": os.getenv("API_USER", "admin"),
        "password": os.getenv("API_PASSWORD", "password123"),
    }
    response = requests.post(f"{BASE_URL}/auth", json=creds, timeout=TIMEOUT)
    assert response.status_code == 200
    return response.json()["token"]


@pytest.fixture
def booking_id(token):
    """Create a booking for one test and delete it afterwards, so tests stay independent."""
    response = requests.post(f"{BASE_URL}/booking", json=BOOKING, timeout=TIMEOUT)
    assert response.status_code == 200
    new_id = response.json()["bookingid"]
    yield new_id
    requests.delete(f"{BASE_URL}/booking/{new_id}",
                    cookies={"token": token}, timeout=TIMEOUT)


def test_created_booking_can_be_read(booking_id):
    response = requests.get(f"{BASE_URL}/booking/{booking_id}", timeout=TIMEOUT)
    assert response.status_code == 200
    assert response.json()["lastname"] == BOOKING["lastname"]


def test_update_requires_auth(booking_id):
    changed = {**BOOKING, "firstname": "NoAuth"}
    response = requests.put(f"{BASE_URL}/booking/{booking_id}", json=changed, timeout=TIMEOUT)
    assert response.status_code == 403


def test_update_with_auth(booking_id, token):
    changed = {**BOOKING, "totalprice": 200}
    response = requests.put(f"{BASE_URL}/booking/{booking_id}", json=changed,
                            cookies={"token": token}, timeout=TIMEOUT)
    assert response.status_code == 200
    assert response.json()["totalprice"] == 200


def test_deleted_booking_is_gone(token):
    created = requests.post(f"{BASE_URL}/booking", json=BOOKING, timeout=TIMEOUT).json()
    booking = created["bookingid"]
    requests.delete(f"{BASE_URL}/booking/{booking}", cookies={"token": token}, timeout=TIMEOUT)
    response = requests.get(f"{BASE_URL}/booking/{booking}", timeout=TIMEOUT)
    assert response.status_code == 404
