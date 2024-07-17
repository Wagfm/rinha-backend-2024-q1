from fastapi import Response

from dtos.create_transaction import CreateTransactionDto
from services.transactions import TransactionsService


class TransactionsController:
    def __init__(self):
        self._service = TransactionsService()

    async def create_transaction(self, customer_id: int, dto: CreateTransactionDto, response: Response) -> dict:
        read_transaction_dto = self._service.create_transaction(customer_id, dto)
        if not read_transaction_dto.success:
            response.status_code = 422
            return {"message": "invalid transaction"}
        return read_transaction_dto.model_dump(exclude={"success"})
