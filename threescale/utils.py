from typing import Union

import requests


def extract_response(response: requests.Response, entity: str = None,
                     collection: str = None) -> Union[dict, list]:
    """Extract the response from the response
    Args:
        response(requests.Response): Response
        entity(str): entity name to be extracted
        collection(str): collection name to be extracted
    Returns(Union[dict, list]): Extracted entity or list of entities
    """
    extracted: dict = response.json()
    if collection and collection in extracted:
        extracted = extracted.get(collection)
    if isinstance(extracted, list):
        return [value.get(entity) for value in extracted]
    if entity in extracted.keys():
        return extracted.get(entity)
    return extracted
