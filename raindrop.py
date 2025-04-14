import os
import requests
import logging
from datetime import datetime
from feedgen.feed import FeedGenerator
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class RaindropClient:
    def __init__(self, access_token, perpage, page):
        self.access_token = access_token
        self.perpage = perpage
        self.page = page
        if not self.access_token:
            raise ValueError("Raindrop.io access token is required")
        
        self.base_url = "https://api.raindrop.io/rest/v1"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        # Test authentication on initialization
        self._test_auth()

    def _test_auth(self):
        """Test if the authentication token is valid"""
        try:
            response = requests.get(
                f"{self.base_url}/user",
                headers=self.headers
            )
            response.raise_for_status()
            logger.info("Successfully authenticated with Raindrop.io API")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                logger.error("Authentication failed. Please check your access token.")
                raise ValueError("Invalid Raindrop.io access token")
            raise

    def get_raindrops(self):
        """Get all raindrops"""
        url = f"{self.base_url}/raindrops/0"
        params = {
            "perpage": int(self.perpage),
            "page": self.page,
            "sort": "-created"  # Sort by creation date in descending order
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            items = response.json()['items']
            return items
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                logger.error("Authentication failed while fetching raindrops")
                raise ValueError("Invalid Raindrop.io access token")
            raise

    def generate_feed(self, title="Raindrop.io Feed", description="Latest items from Raindrop.io"):
        """Generate RSS feed from all Raindrop.io items"""
        try:
            fg = FeedGenerator()
            fg.title(title)
            fg.description(description)
            fg.link(href="https://raindrop.io")
            fg.language('en')

            raindrops = self.get_raindrops()
            logger.info(f"Successfully fetched {len(raindrops)} raindrops")
            
            # Reverse the order of items to show newest first
            for item in reversed(raindrops):
                try:
                    fe = fg.add_entry()
                    fe.title(item['title'])
                    fe.link(href=item['link'])
                    fe.description(item.get('excerpt', ''))
                    
                    # Use created time for pubDate
                    created = item.get('created')
                    if created:
                        try:
                            # Parse ISO format date
                            date_obj = datetime.fromisoformat(created.replace('Z', '+00:00'))
                            fe.pubDate(date_obj)
                        except (ValueError, TypeError) as e:
                            logger.warning(f"Invalid timestamp for item {item.get('title')}: {created}")
                            fe.pubDate(datetime.now())
                except Exception as e:
                    logger.error(f"Error processing item {item.get('title')}: {str(e)}")
                    continue

            return fg.rss_str(pretty=True)
        except Exception as e:
            logger.error(f"Error generating feed: {str(e)}")
            raise 