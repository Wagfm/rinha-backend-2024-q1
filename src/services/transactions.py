from dtos.create_transaction import CreateTransactionDto
from dtos.read_transaction import ReadTransactionDto
from repositories.transactions import TransactionsRepository


class TransactionsService:
    def __init__(self):
        self._repository = TransactionsRepository()

    def create_transaction(self, customer_id: int, dto: CreateTransactionDto) -> ReadTransactionDto:
        operation = self._repository.create_transaction(customer_id, dto)
        return ReadTransactionDto(
            success=operation.success, limite=operation.current_limit, saldo=operation.new_balance
        )
