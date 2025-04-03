from llm_query_compiler.compiler import LLMQueryCompiler
from llm_query_compiler.model_drivers.openai_driver import OpenAIModelDriver
import os
import json

def test_compile_with_valid_input():
    with open("tests/schema.json", "r", encoding="utf-8") as f:
        schema = json.load(f)
    
    print(schema)
    
    driver = OpenAIModelDriver(api_key=os.getenv("OPENAI_API_KEY"))
    compiler = LLMQueryCompiler(schema=schema,model_driver=driver)

    result = compiler.compile("서울 근처 맛집 추천해줘")
    assert result.intent
    assert result.category
