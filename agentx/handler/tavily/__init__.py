import logging
from typing import Sequence

from tavily import TavilyClient
from agentx.handler.base import BaseHandler
from agentx.handler.jira import AuthException
from agentx.utils.helper import sync_to_async

from agentx.handler.tavily.exceptions import AuthException, SearchException
logger = logging.getLogger(__name__)


class TavilyHandler(BaseHandler):

    def __init__(
            self,
            *,
            query: str,
            api_key: str
    ):
        self.query = query
        self.api_key = api_key
        self._connection: TavilyClient = self._connect()

    def _connect(self) -> TavilyClient:
        try:
            # Instantiate TavilyClient with the API key
            tav_client = TavilyClient(self.api_key)
            return tav_client

        except Exception as ex:
            message = f'Tavily Handler Authentication Problem: {ex}'
            logger.error(message, exc_info=True)
            raise AuthException(message)

    async def do_search(self):
        """Execute a search using the Tavily client."""
        try:
            return await sync_to_async(
                self._connection.search,
                query=self.query
            )
        except Exception as ex:
            message = f'Error executing search: {ex}'
            logger.error(message, exc_info=True)
            raise SearchException(message)

    def __dir__(self):
        return (
            'do_search'
        )
