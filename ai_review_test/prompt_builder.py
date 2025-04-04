import json

class PromptBuilder:
    def __init__(self):
        pass

    def extract_enum_hints(self, schema_dict: dict) -> str:
        hints = []
        for key, val in schema_dict.items():
            if isinstance(val, dict) and "categorical" in val:
                items = val["categorical"]
                if isinstance(items, list):
                    options = [
                        f'"{item.get("label")}": {item.get("description", "")}'
                        for item in items if "label" in item
                    ]
                    hint_block = f'- {key} options:\n  ' + "\n  ".join(options)
                    hints.append(hint_block)
        return "\n".join(hints)

    def build(self, user_input: str, schema_json: str, schema_dict: dict) -> str:
        schema_obj = json.loads(schema_json)
        required_fields = schema_obj.get("required", [])
        enum_hint_text = self.extract_enum_hints(schema_dict)

        full_prompt = f"""
You are an assistant that extracts structured data from natural language.

Schema:
{schema_json}

User input:
"{user_input}"

Instructions:
- Include these required fields: {required_fields}
- Optional fields must be included with null if missing
- Always include all fields as keys
# {enum_hint_text}
Respond with a valid JSON object only.
""".strip()

        return full_prompt
