from llm_query_compiler.compiler import LLMQueryCompiler
from llm_query_compiler.model_drivers.openai_driver import OpenAIModelDriver
import os

schema = {
    "intent": {"type": "string", "required": True},
    "category": {
        "type": "string",
        "required": True,
        "categorical": ["전자기기", "음식", "패션", "부동산"]},
    "filters": {"type": "dict", "required": False},
    "sort": {"type": "string", "required": False}
}

driver = OpenAIModelDriver(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-3.5-turbo"
)

compiler = LLMQueryCompiler(schema=schema, model_driver=driver)

result = compiler.compile("가성비 좋은 AI 노트북 추천해줘")
print("Structured Result:")
print(result)