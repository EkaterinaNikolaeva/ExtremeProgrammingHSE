import requests

URL = "http://localhost:9001"


def add_key_value(key: str, value: str):
    data = {
        "key": key,
        "value": value,
    }
    response = requests.put(f"{URL}/storage", json=data)
    response.raise_for_status()


def get_key(key: str):
    response = requests.get("{}/storage".format(URL), params={"key": key})
    response.raise_for_status()
    response_json = response.json()
    return response_json["value"]


if __name__ == "__main__":
    add_key_value("aba", "caba")
    assert get_key("aba") == "caba"
