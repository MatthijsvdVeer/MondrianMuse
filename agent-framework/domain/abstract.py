from pydantic import BaseModel, ConfigDict
class Abstract(BaseModel):
    title: str
    abstract: str
    model_config = ConfigDict(extra="forbid")
