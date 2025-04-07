from abc import ABC, abstractmethod

class BaseModelDriver(ABC):
    @abstractmethod
    def chat(self, user_input: str, schema_json: str) -> str:
        pass
