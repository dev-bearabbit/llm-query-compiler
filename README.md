# llm-query-compiler

🚀 Turn natural language into structured, machine-readable queries using OpenAI + Pydantic.  
Perfect for building AI-powered search, recommendation, or query routing systems.

---

## 🔍 What is this?

This tool helps you convert free-form user inputs like:

> `"서울 근처 맛집 추천해줘"`

into a **structured query object** based on a schema you define —  
so that your backend, search engine, or recommender system knows exactly what to do.

---

## ✅ Example

```python
from llm_query_compiler.compiler import LLMQueryCompiler
from llm_query_compiler.model_drivers.openai_driver import OpenAIModelDriver
import os, json

# Load your schema (defined in JSON)
with open("tests/schema.json", "r", encoding="utf-8") as f:
    schema = json.load(f)

# Setup the model driver
driver = OpenAIModelDriver(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize the compiler with schema and driver
compiler = LLMQueryCompiler(schema=schema, model_driver=driver)

# Compile a user input
result = compiler.compile("서울 근처 맛집 추천해줘")

print(result.model_dump_json(indent=2))

{
  "intent": "맛집 추천",
  "category": "음식",
  "filters": {
    "location": "서울 근처"
  },
  "sort": null
}
```

# 🧠 Why this is useful

- Convert messy, ambiguous user text into clean query data
- Avoid brittle regex-based intent parsing
- Fully pluggable: bring your own schema, your own LLM
