from models.customer import Customer
from models.transaction import Transaction
from repositories.base import BaseRepository


class CustomersRepository(BaseRepository):
    def __init__(self):
        super().__init__()

    @BaseRepository._with_connection
    def get_statement(self, customer_id: int) -> tuple[Customer | None, list[Transaction]]:
        parameters = [customer_id]
        result = self._cursor.execute("""
            SELECT * FROM customers WHERE id = %s;
        """, parameters)
        customer_data = result.fetchone()
        if customer_data is None:
            return None, []
        customer = Customer(**customer_data)
        result = self._cursor.execute("""
            SELECT * FROM transactions
                WHERE customer_id = %s ORDER BY value DESC LIMIT 10;
        """, parameters)
        transactions_data = result.fetchall()
        transactions = [Transaction(**data) for data in transactions_data]
        return customer, transactions
