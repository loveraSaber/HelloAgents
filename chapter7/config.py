import os
from typing import Optional,Dict,Any
from pydantic import BaseModel
class Config(BaseModel):
    default_model:str=""
    default_provider:str=""
    temperature:float=0.7
    max_tokens:Optional[int]=None
    #system config
    debug:bool=False
    log_level:str="INFO"
    
    max_history_length:int=100
    @classmethod
    def from_env(cls)->"Config":
        return cls(
            debug=os.getenv("DEBUG","false").lower()=="true",
            log_level=os.getenv("LOG_LEVEL","INFO"),
            temperature=float(os.getenv("TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("MAX_TOKENS")) if os.getenv("MAX_TOKENS") else None,
        )
    def to_dict(self)->Dict[str,Any]:
        return self.model_dump()