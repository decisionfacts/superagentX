import random
import logging

from openai.types.chat import ChatCompletion

from agentx.handler.base import BaseHandler
from agentx.llm import ChatCompletionParams, LLMClient

logger = logging.getLogger(__name__)


class FakeProductHandler(BaseHandler):

    def __init__(
            self,
            *,
            product_models: list[str],
            llm_client: LLMClient,
            total: int = 5
    ):
        self.total = total
        self.product_models = product_models
        self.llm_client: LLMClient = llm_client

    @staticmethod
    async def _random_rating():
        return {
            "rate": round(random.uniform(2.0, 5.0), 1),
            "count": random.randint(100, 500)
        }

    async def _random_product_description(
            self,
            model,
    ):
        messages = [
            {
                "role": "system",
                "content": f"You are a best product reviewer. Analyze and generate fake product short description for {model} and its features"
            }
        ]

        chat_completion_params = ChatCompletionParams(
            messages=messages,
        )
        response: ChatCompletion = await self.llm_client.achat_completion(chat_completion_params=chat_completion_params)
        description = response.choices[0].message.content
        logger.debug(f"Open AI Async ChatCompletion Response {description}")

        return description

    async def _generate_data_products(
            self,
            provider: str,
    ):
        # Generate the dataset
        products_list = []
        if self.product_models:
            for i in range(1, self.total):
                model = random.choice(self.product_models)
                product_data = {
                    "id": i,
                    "title": model,
                    "price": round(random.uniform(8000, 90000), 2),
                    "description": await self._random_product_description(model),
                    "category": "mobile phones",
                    "provider": provider,
                    "image": f"https://fake{provider.lower()}storeapi.com/img/{model}.jpg",
                    "rating": await self._random_rating()
                }
                products_list.append(product_data)
                # TODO: Random 5 comments generate using LLM!
        return products_list

    async def search(
            self,
            provider: str
    ):
        """
        Search for a product using the specified provider.

        This function interfaces with multiple e-commerce providers (e.g., Amazon, Flipkart)
        to search for products based on the specified provider.
        parameter:
            provider (str): The name of the e-commerce provider to search from. Supported providers include:
                - 'amazon': Search for products on Amazon.
                - 'flipkart': Search for products on Flipkart.
        Returns:
        The search results as a response object or parsed data, depending on the implementation for each provider.
        """
        return await self._generate_data_products(provider)

    def __dir__(self):
        return (
            "search"
        )
