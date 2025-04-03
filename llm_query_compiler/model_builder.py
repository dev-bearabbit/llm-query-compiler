from pydantic import BaseModel, create_model
from typing import Any, Dict, Tuple, Type, Optional
from enum import Enum

TYPE_MAP = {
    "string": str,
    "float": float,
    "integer": int,
    "bool": bool,
    "list": list,
    "dict": dict
}

def build_enum(name: str, values: list[str]) -> Type[Enum]:
    """
    Creates a dynamic Enum class from a list of categorical values.
    """
    safe_dict = {str(v).upper().replace(" ", "_"): v for v in values}
    return Enum(name, safe_dict)

def parse_schema_field(key: str, value: Any) -> Tuple:
    """
    Parses a schema field and returns a (type, default) tuple suitable for create_model.
    Supports label + description style categorical definitions.
    """
    if isinstance(value, str):
        return (str, ...)

    elif value is None:
        return (Optional[str], None)

    elif isinstance(value, dict):
        required = value.get("required", True)
        type_name = value.get("type", "string")
        py_type = TYPE_MAP.get(type_name, str)

        if "categorical" in value and isinstance(value["categorical"], list):
            categorical_list = value["categorical"]

            labels = [
                item["label"]
                for item in categorical_list
                if isinstance(item, dict) and "label" in item
            ]

            if labels:
                enum_name = f"{key.capitalize()}Enum"
                py_type = build_enum(enum_name, labels)

        if not required:
            return (Optional[py_type], None)
        else:
            return (py_type, ...)

    else:
        return (str, ...)

def build_model_from_schema(schema_dict: Dict[str, Any], model_name: str = "DynamicQuery") -> Type[BaseModel]:
    """
    Builds a dynamic Pydantic model from the provided schema dict.
    """
    fields = {}
    for key, val in schema_dict.items():
        fields[key] = parse_schema_field(key, val)
    return create_model(model_name, **fields)
