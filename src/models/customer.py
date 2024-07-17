from dataclasses import dataclass


@dataclass(frozen=True)
class Customer:
    id: int
    name: str
    balance: int
    account_limit: int
