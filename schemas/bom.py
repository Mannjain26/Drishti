from pydantic import BaseModel
from typing import List

class BOMItem(BaseModel):
    category: str
    description: str
    required_quantity: int
    mandatory_for_batch: bool = True

class SanctionedBOM(BaseModel):
    centre_id: str
    scheme_code: str = "PMKVY-4.0"
    centre_name: str
    items: List[BOMItem]
