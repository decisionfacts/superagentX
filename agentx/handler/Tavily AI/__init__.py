import logging
from abc import ABC

from tavily import TavilyClient

from agentx.handler.base import BaseHandler

logger = logging.getLogger(__name__)


class TavilyHandler(BaseHandler, ABC):

    def __init__(
            self,
            *,
            query: str,
            api_key: str
    ):
        self.query = query
        self._connection: TavilyClient = self._connect()
