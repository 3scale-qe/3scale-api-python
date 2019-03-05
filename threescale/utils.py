from typing import Union

import requests


def extract_response(response: requests.Response, entity: str = None,
                     collection: str = None) -> Union[dict, list]:
    extracted: dict = response.json()
    if collection:
        extracted = extracted.get(collection)
    if isinstance(extracted, list):
        return [value.get(entity) for value in extracted]
    if entity in extracted.keys():
        return extracted.get(entity)
    return extracted
