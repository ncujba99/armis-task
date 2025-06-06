import time
import requests
from typing import Iterator

from config import logger
from crowdstrike.models import HostItem


class CrowdStrikeClient:
    def __init__(self, api_key: str, url: str):

        self.api_key = api_key
        self.url = url
        self.logger = logger

    def scroll_hosts(
        self, limit: int = 1, skip: int = 0, max_retries: int = 1, retry_delay: int = 1
    ) -> Iterator[HostItem]:
        retries = 0
        while True:
            params = {"skip": skip, "limit": limit}
            try:
                self.logger.debug(f"Requesting hosts with params: {params}")
                response = requests.post(
                    url=self.url, params=params, headers={"token": self.api_key}
                )
                response.raise_for_status()

                raw_data = response.json()

                if not isinstance(raw_data, list) or not raw_data:
                    self.logger.info(
                        "No more data returned from API. Stopping the generator."
                    )
                    break

                yield from map(HostItem.model_validate, raw_data)

                skip += limit
                retries = 0

            except requests.exceptions.RequestException as e:
                retries += 1
                if retries > max_retries:
                    self.logger.error(f"Max retries reached. Last error: {e}")
                    break

                self.logger.warning(
                    f"Request failed: {e}. Retrying in {retry_delay} seconds..."
                )
                time.sleep(retry_delay)

            except Exception as e:
                self.logger.error(f"Unexpected error: {e}")
                break
