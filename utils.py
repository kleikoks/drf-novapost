import requests

from django.conf import settings


url = "https://api.novaposhta.ua/v2.0/json/"
api_key = getattr(settings, "NP_API_KEY", None)


def get_full_response(model: str, method: str, properties: dict = None) -> dict[str, list]:
    result = {"data": []}
    properties = properties or {}
    properties["Limit"] = 3000

    data = {
        "apiKey": api_key,
        "modelName": model,
        "calledMethod": method,
        "methodProperties": properties,
    }
    data["methodProperties"]["Page"] = 1
    while True:
        response = requests.post(url, json=data).json()

        if not response["data"]:
            break

        for obj in response["data"]:
            result["data"].append(obj)

        data["methodProperties"]["Page"] += 1
    return result


def get_response(model: str, method: str, properties: dict | None = None) -> dict:
    properties = properties or {}
    data = {
        "apiKey": api_key,
        "modelName": model,
        "calledMethod": method,
        "methodProperties": properties,
    }
    response = requests.post(url, json=data).json()
    return response


def test_api():
    response = get_response("Address", "getSettlementTypes")
    if response["errors"]:
        raise Exception(response["errors"])
