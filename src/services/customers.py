from datetime import datetime

from dtos.read_statement import ReadStatementDto
from repositories.customers import CustomersRepository


class CustomersService:
    def __init__(self):
        self._repository = CustomersRepository()

    def get_statement(self, customer_id: int) -> ReadStatementDto | None:
        customer, transactions = self._repository.get_statement(customer_id)
        if customer is None:
            return None
        return ReadStatementDto(
            saldo={
                "total": customer.balance,
                "data_extrato": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "limite": customer.account_limit
            },
            ultimas_transacoes=[
                {
                    "valor": transaction.value,
                    "tipo": transaction.type,
                    "descricao": transaction.description,
                    "realizada_em": transaction.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                }
                for transaction in transactions
            ]
        )
