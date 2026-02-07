# integrations.py
import httpx
from typing import Dict, Any
from config import config


class ComposioTwitter:
    """
    Handles Twitter/X actions via Composio
    """

    def __init__(self):
        self.api_key = config.COMPOSIO_API_KEY
        self.base_url = "https://backend.composio.dev/api/v3"
        self.entity_id = getattr(config, "COMPOSIO_ENTITY_ID", "debateshield")

    def _headers(self):
        return {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
        }

    async def get_tweet_text(self, tweet_url: str) -> str:
        """
        Fetch tweet content using Composio
        """
        payload = {
            "entity_id": self.entity_id,
            "tool": "twitter_get_tweet",
            "args": {"url": tweet_url},
        }

        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(
                f"{self.base_url}/execute",
                headers=self._headers(),
                json=payload,
            )
            r.raise_for_status()
            data = r.json()

        return data.get("output", {}).get("text", "")

    async def post_reply(self, tweet_url: str, text: str) -> Dict[str, Any]:
        """
        Reply to a tweet (manual or auto-post)
        """
        payload = {
            "entity_id": self.entity_id,
            "tool": "twitter_create_post",
            "args": {
                "text": text,
                "reply_to": tweet_url,
            },
        }

        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(
                f"{self.base_url}/execute",
                headers=self._headers(),
                json=payload,
            )
            r.raise_for_status()

        return r.json()


class ActionEngine:
    """
    Keeps Intercom support intact.
    Composio actions are explicit via endpoints.
    """

    async def execute_actions(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        # For now, do NOT auto-post anywhere
        return {
            "intercom": {"sent": False},
            "twitter": {"sent": False},
        }
