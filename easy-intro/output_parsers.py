from typing import List, Any, Dict

from langchain_core.output_parsers import PydanticOutputParser
from pydantic import Field, BaseModel


class Summary(BaseModel):
    summary: str = Field(descripton="The summary of the information")
    facts: List[str] = Field(description="Two interesting facts about the person")

    def to_dict(self) -> Dict[str, Any]:
        return {"summary": self.summary, "facts": self.facts}


summary_parser = PydanticOutputParser(pydantic_object=Summary)
