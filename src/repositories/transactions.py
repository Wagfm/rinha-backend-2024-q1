from dtos.create_transaction import CreateTransactionDto
from models.operation import Operation
from repositories.base import BaseRepository


class TransactionsRepository(BaseRepository):
    def __init__(self):
        super().__init__()

    @BaseRepository._with_connection
    def create_transaction(self, customer_id: int, dto: CreateTransactionDto) -> Operation | None:
        parameters = [customer_id, dto.valor, dto.descricao]
        if dto.tipo == "c":
            result = self._cursor.execute("""
                SELECT * FROM credit_operation(%s, %s, %s);
            """.encode(), parameters)
            data = result.fetchone()
            return Operation(**data)
        if dto.tipo == "d":
            result = self._cursor.execute("""
                SELECT * FROM debit_operation(%s, %s, %s);
            """.encode(), parameters)
            data = result.fetchone()
            return Operation(**data)
        raise ValueError(f"Invalid transaction type: {dto.tipo}")
