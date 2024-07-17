from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Transaction:
    id: int
    customer_id: int
    value: int
    type: str
    description: str
    created_at: datetime
