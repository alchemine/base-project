"""Requests module for handling HTTP requests."""

import asyncio
from typing import Any

import requests
from requests import Response, HTTPError
import aiohttp
from aiohttp import ClientResponse, ClientResponseError

from src.common.logger import log_api


DEFAULT_HEADERS = {"accept": "application/json", "Content-Type": "application/json"}


class APIError(Exception):
    """API Error exception.

    Args:
        url (str): The URL of the API.
        headers (dict): The headers of the API.
        json (dict): The JSON data of the API.
        response (Response): The response of the API.

    Returns:
        str: The API error message.
    """

    def __init__(self, url: str, headers: dict, json: dict, response: Response):
        self.url = url
        self.headers = headers
        self.json = json
        self.response = response

    def __str__(self):
        return f"""APIError: <Response [{self.response.status_code}]>
requests.post(
    url="{self.url}",
    headers={self.headers},
    json={self.json}
) -> {self.response.json()}"""


def get_request_log(
    url: str,
    headers: dict,
    json: dict,
    response: Response | ClientResponse | None = None,
) -> dict:
    """Get the request log.

    Args:
        url (str): The URL of the API.
        headers (dict): The headers of the API.
        json (dict): The JSON data of the API.
        response (Response): The response of the API.

    Returns:
        dict: The request log.
    """
    log = dict(
        url=url,
        headers=headers,
        json=json,
        reproduction_code=f"import requests; requests.post(url='{url}', headers={headers}, json={json})",
    )

    if response:
        log.update(
            response=dict(status_code=response.status_code, json=response.json())
        )

    return log


def safe_request(url: str, json: dict, headers: dict = DEFAULT_HEADERS) -> dict:
    """Requests with validation.

    Args:
        url (str): The URL of the API.
        json (dict): The JSON data of the API.
        headers (dict): The headers of the API.

    Returns:
        Response: The response of the API.
    """
    # Check the API communication validness
    try:
        response = requests.post(url=url, headers=headers, json=json)
        response.raise_for_status()
        log = get_request_log(url, headers, json, response)
        log_api(log)
        return response.json()
    except HTTPError:
        log = get_request_log(url, headers, json)
        log_api(log, error=True)
        raise


async def async_safe_request(
    session: aiohttp.ClientSession,
    url: str,
    data: dict,
    headers: dict = DEFAULT_HEADERS,
) -> list | dict:
    """Post request using aiohttp.

    Args:
        session (aiohttp.ClientSession): aiohttp session.
        url (str): URL to post.
        data (dict): Data to post.
        headers (dict): The headers of the API.

    Returns:
        list | dict: Response data.
    """
    async with session.post(
        url=url,
        headers=headers,
        json=data,
    ) as response:
        try:
            response.raise_for_status()
            log = get_request_log(url, headers, data, response)
            log_api(log)
            return await response.json()
        except ClientResponseError:
            log = get_request_log(url, headers, data)
            log_api(log, error=True)
            raise


async def async_safe_requests(batch: list[dict]) -> list[Any]:
    """Post requests asynchronously.

    Args:
        batch (list[dict]): List of data to post.

    Returns:
        list[Any]: List of response data.

    Examples:
        import asyncio
        asyncio.run(async_safe_requests(batch))
    """
    async with aiohttp.ClientSession() as session:
        futures = [async_safe_request(session, **input) for input in batch]
        responses = await asyncio.gather(*futures)
    return responses


if __name__ == "__main__":
    url = "https://httpbin.org/post"
    json = {"key": "value"}
    response = safe_request(url, json)
