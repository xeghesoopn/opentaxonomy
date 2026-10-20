import lmstudio as lms

from typing import TypeVar, Type, Any
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

    def call_structured(
        self,
        system: str,
        user: str,
        input_schema: dict[str, Any],
        max_tokens: int = 8096,
    ) -> dict[str, Any]:
        """ Call the LMStudio client to get a structured .json output. """
        chat = lms.Chat(initial_prompt=system)
        chat.add_entry(role="user", content=user)
        response = self.client.respond(
            history=chat,
            response_format=input_schema,
            config={"maxTokens": max_tokens}
            )
        result = response.parsed
        rprint(result)
        return result

    def complete(
        self,
        schema_class: Type[T],
        system: str,
        user: str,
        max_tokens: int = 8096,
        max_tries: int = 3
    ) -> T:
        """ Wrapper to validate the response, and to try again in case of failure. """
        input_schema = schema_class.model_json_schema()
        for i in range(max_tries):
            try:
                result = self.call_structured(
                    system,
                    user,
                    input_schema,
                    max_tokens
                    )
                return schema_class.model_validate(result)
            except Exception as e:
                print(f"Failed to validate LLM's response: {e}")
        raise ValueError(f"Failed to validate LLM's response after {max_tries} attempts.")