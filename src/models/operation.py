from dataclasses import dataclass


@dataclass(frozen=True)
class Operation:
    success: bool
    current_limit: int
    new_balance: int
