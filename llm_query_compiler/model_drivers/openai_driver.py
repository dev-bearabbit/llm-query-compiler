import json
from openai import OpenAI
from .base import BaseModelDriver

class OpenAIModelDriver(BaseModelDriver):
    def __init__(self, api_key: str, model: str = "o3-mini"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def chat(self, user_input: str, prompt: str) -> str:

        print(prompt)

        system_prompt = "You are a helpful assistant that converts unstructured natural language into a structured JSON query based on a given schema."

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "assistant", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content
