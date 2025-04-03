import json
import re
from pydantic import BaseModel
from typing import Dict, Type
from llm_query_compiler.model_builder import build_model_from_schema
from llm_query_compiler.model_drivers.prompt_builder import PromptBuilder
from llm_query_compiler.model_drivers.base import BaseModelDriver

class LLMQueryCompiler:
    def __init__(self, schema: Dict, model_driver: BaseModelDriver):
        self.schema_dict = schema
        self.model_class = build_model_from_schema(schema)
        self.schema_json = json.dumps(
            self.model_class.model_json_schema(),
            indent=2
        )
        self.model_driver = model_driver

    def compile(self, user_input: str) -> BaseModel:
        full_prompt = PromptBuilder().build(user_input, self.schema_json, self.schema_dict)
        raw_output = self.model_driver.chat(user_input, full_prompt)
        output = re.sub(r"```(?:json)?", "", raw_output)
        parsed = json.loads(output)
        print(parsed)

        if "error" in parsed:
            raise ValueError(f"LLM returned error: {parsed['error']} - missing: {parsed.get('missing')}")

        return self.model_class(**parsed)
