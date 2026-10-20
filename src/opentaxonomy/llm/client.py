from typing import TypeVar, Type, Any

import lmstudio as lms
from pydantic import BaseModel
from rich import print as rprint

T = TypeVar("T", bound=BaseModel)


class TaxonomyLLM:
    """
    A large language model provided by the LMStudio client, used for
    a discrete text processing task.
    - api_key (str): Not used here, for code compatibility only.
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
        """ Call LMStudio to get a structured .json output. """
        chat = lms.Chat(initial_prompt=system)
        chat.add_entry(role="user", content=user)
        response = self.client.respond(
            history=chat,
            response_format=input_schema,
            config={"maxTokens": max_tokens}
            )
        return response.parsed

    def complete(
        self,
        schema_class: Type[T],
        system: str,
        user: str,
        max_tokens: int = 8096,
        max_tries: int = 2
    ) -> T:
        """ Call LMStudio and parse the response into a Pydantic model. """
        input_schema = schema_class.model_json_schema()
        for i in range(max_tries):
            result = self.call_structured(
                system,
                user,
                input_schema,
                max_tokens
                )
            rprint(result)
            try:
                return schema_class.model_validate(result)
            except Exception:
                pass
        raise ValueError(f"Failed to validate LLM's response after {max_tries} attempts.")