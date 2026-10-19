import lmstudio as lms
import re

from typing import TypeVar, Type
from pydantic import BaseModel

from rich import print as rprint

T = TypeVar("T", bound=BaseModel)


class TaxonomyLLM:
    """
    A large language model provided by LMStudio, used for a discrete
    text processing task.
    - api_key (str): Not used, for code compatibility only.
    - model (str): The name of the model to use in LMStudio.
    """
    def __init__(self, api_key: str = "", model: str = "qwen3.5-27b"):
        self.client = lms.llm(model)

    def _strip_reasoning(self, response: dict[str, str | None]) -> str:
        """ Strip the LMStudio reasoning block from the response. """
        content = response.get('nonReasoningContent') or response.get('content')
        if content is None:
            return ""
        if "LM_STUDIO_INTERNAL_" not in content:
            return content
        out = content
        last = -1
        marker = re.compile(r"__LM_STUDIO_INTERNAL_LSEP_SYNTHETIC_REASONING_END_[0-9a-f]+__")
        for match in marker.finditer(out):
            last = match.start() + len(match.group(0))
        if last >= 0:
            out = out[last:]
        return out.strip()

    def call_structured(
        self,
        system: str,
        user: str,
        schema_class: Type[T],
        max_tokens: int = 8096,
    ) -> dict:
        """ Call the LMStudio client to get a structured .json output. """
        chat = lms.Chat(initial_prompt=system) # Always spawn a new chat object for a clean history.
        chat.add_user_message(user)
        response = self.client.respond(
            chat,
            response_format=schema_class,
            config={
                "maxTokens": max_tokens
                }
            )
        return self._strip_reasoning(response)

    def complete(
        self,
        schema_class: Type[T],
        system: str,
        user: str,
        max_tokens: int = 8096,
        max_tries: int = 3
    ) -> T:
        """ Wrapper to validate the response, and to try again in case of failure. """
        for i in range(max_tries):
            try:
                result = self.call_structured(
                    system,
                    user,
                    schema_class,
                    max_tokens,
                )
                rprint(result) # Print the result
                return schema_class.model_validate(result)
            except Exception as e:
                print(f"Failed to validate LLM's response: {e}")
        raise ValueError(f"Failed to validate LLM's response after {max_tries} attempts.")