from pydantic import BaseModel
from typing import List


class IngestDataRequest(BaseModel):
    items: List[str]
