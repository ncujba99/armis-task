import time
import requests

from config import api_key, crowdstrike_url, logger 


def scroll_hosts(limit=1, skip=0, max_retries=5, retry_delay=65):
    retries = 0
    while True:
        params = {'skip': skip, 'limit': limit}
        
        try:
            logger.debug(f"Requesting hosts with params: {params}")
            response = requests.post(
                url=crowdstrike_url,
                params=params,
                headers={"token": api_key}
            )
            response.raise_for_status()
            
            data = response.json()
            
            if not data:
                logger.info("No more data returned from API. Stopping the generator.")
                break
            
            for item in data:
                yield item
            
            # Update skip for the next request
            skip += limit
            retries = 0 
        
        except requests.exceptions.RequestException as e:
            retries += 1
            if retries > max_retries:
                logger.error(f"Max retries reached. Last error: {e}")
                break
            
            logger.warning(f"Error occurred: {e}. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)



