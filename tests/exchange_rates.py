from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_add_exchange_rate_unique_error():
    payload = {"baseCurrencyCode": "USD", "targetCurrencyCode": "EUR", "rate": 0.92}
    response = client.post("/exchangeRates", data=payload)
    assert response.status_code == 409


def test_add_exchange_rate_not_found_error():
    payload = {"baseCurrencyCode": "XXX", "targetCurrencyCode": "YYY", "rate": 0.92}
    response = client.post("/exchangeRates", data=payload)
    assert response.status_code == 404


def test_get_all_exchange_rates():
    response = client.get("/exchangeRates")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 0


def test_get_exchange_rate():
    response = client.get("/exchangeRate/USDEUR")
    assert response.status_code == 200
    assert response.json()["baseCurrency"]["code"] == "USD"
    assert response.json()["targetCurrency"]["code"] == "EUR"


def test_get_exchange_rate_validation_error():
    response = client.get("/exchangeRate/INVALID")
    assert response.status_code == 400


def test_get_exchange_rate_not_found():
    response = client.get("/exchangeRate/XXXYYY")
    assert response.status_code == 404


def test_calculate_exchange():
    params = {"from": "USD", "to": "EUR", "amount": 100}
    response = client.get("/exchange", params=params)
    assert response.status_code == 200
    assert response.json()["baseCurrency"]["code"] == "USD"
    assert response.json()["targetCurrency"]["code"] == "EUR"
    assert response.json()["amount"] == 100
    assert "convertedAmount" in response.json()


def test_calculate_exchange_not_found():
    params = {"from": "XXX", "to": "YYY", "amount": 100}
    response = client.get("/exchange", params=params)
    assert response.status_code == 404  # DatabaseNotFoundError


def test_update_exchange_rate():
    data = {"rate": "1.10"}
    response = client.patch("/exchangeRate/USDEUR", data=data)
    assert response.status_code == 200
    assert response.json()["baseCurrency"]["code"] == "USD"
    assert response.json()["targetCurrency"]["code"] == "EUR"
    assert response.json()["rate"] == 1.10


def test_update_exchange_rate_validation_error():
    data = {"rate": "-1.00"}
    response = client.patch("/exchangeRate/USD-EUR", data=data)
    assert response.status_code == 400  # ServiceValidationError


def test_update_exchange_rate_not_found():
    data = {"rate": "1.10"}
    response = client.patch("/exchangeRate/XXXYYY", data=data)
    assert response.status_code == 404  # DatabaseNotFoundError
