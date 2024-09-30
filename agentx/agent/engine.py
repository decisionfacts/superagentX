import inspect
import typing

from agentx.exceptions import ToolError
from agentx.handler.base import BaseHandler
from agentx.handler.exceptions import InvalidHandler
from agentx.llm import LLMClient, ChatCompletionParams
from agentx.prompt import PromptTemplate
from agentx.utils.helper import iter_to_aiter, sync_to_async
from agentx.utils.parsers.base import BaseParser


class Engine:

    def __init__(
            self,
            *,
            handler: BaseHandler,
            llm: LLMClient,
            prompt_template: PromptTemplate,
            tools: list[dict] | list[str] | None = None,
            output_parser: BaseParser | None = None
    ):
        self.handler = handler
        self.llm = llm
        self.prompt_template = prompt_template
        self.tools = tools
        self.output_parser = output_parser

    async def __funcs_props(self, funcs: list[str] | list[dict]) -> list[dict]:
        _funcs_props: list[dict] = []
        async for _func_name in iter_to_aiter(funcs):
            _func = None
            if isinstance(_func_name, str):
                _func_name = _func_name.split('.')[-1]
                _func = getattr(self.handler, _func_name)
            else:
                # TODO: Needs to fix this for tools contains list of dict
                pass
            if inspect.isfunction(_func):
                _funcs_props.append(await self.llm.get_tool_json(func=_func))
        return _funcs_props

    async def _construct_tools(self) -> list[dict]:
        funcs = dir(self.handler)
        if not funcs:
            raise InvalidHandler(str(self.handler))

        _tools: list[dict] = []
        if self.tools:
            _tools = await self.__funcs_props(funcs=self.tools)
        if not _tools:
            _tools = await self.__funcs_props(funcs=funcs)
        return _tools

    async def start(
            self,
            input_prompt: str,
            **kwargs
    ) -> list[typing.Any]:
        if not kwargs:
            kwargs = {}
        prompt_messages = await self.prompt_template.get_messages(
            input_prompt=input_prompt,
            **kwargs
        )
        tools = await self._construct_tools()
        chat_completion_params = ChatCompletionParams(
            messages=prompt_messages,
            tools=tools
        )
        messages = await self.llm.afunc_chat_completion(
            chat_completion_params=chat_completion_params
        )
        if not messages:
            raise ToolError("Tool not found for the inputs!")

        results = []
        async for message in iter_to_aiter(messages):
            async for tool in iter_to_aiter(message.tool_calls):
                if tool.tool_type == 'function':
                    func = getattr(self.handler, tool.name)
                    if func and inspect.isfunction(func):
                        _kwargs = tool.arguments or {}
                        if inspect.iscoroutinefunction(func):
                            res = await func(**_kwargs)
                        else:
                            res = await sync_to_async(func, **_kwargs)

                        if res:
                            if not self.output_parser:
                                results.append(res)
                            else:
                                results.append(await self.output_parser.parse(res))
        return results
