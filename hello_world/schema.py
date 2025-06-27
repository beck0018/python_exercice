from pydantic import BaseModel, ConfigDict

class Pokemon(BaseModel):
    #avoid conflicts
    model_config = ConfigDict(extra="ignore")
    name: str
    weight : int
