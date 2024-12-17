from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_currencies():
    response = client.get("/currencies")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_get_currency_by_name():
    response = client.get("/currency/Euro")
    assert response.status_code == 200
    assert response.json()["code"] == "EUR"


def test_get_currency_by_name_not_found():
    response = client.get("/currency/RUB")
    assert response.status_code == 404


def test_get_currency_by_name_validation_error():
    response = client.get("/currency/123")
    assert response.status_code == 400


def test_add_currency():
    currency_data = {
        "name": "Russian ruble",
        "code": "RUB",
        "sign": "₽"
    }
    response = client.post("/currencies", data=currency_data)
    assert response.status_code == 200
    assert response.json()["code"] == "RUB"


def test_add_currency_unique_error():
    currency_data = {
        "name": "Russian ruble",
        "code": "RUB",
        "sign": "₽"
    }
    response = client.post("/currencies", data=currency_data)
    assert response.status_code == 409

