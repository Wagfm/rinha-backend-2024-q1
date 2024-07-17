from fastapi import APIRouter

from controllers.customers import CustomersController
from routes.transactions import TransactionsRouter


class CustomersRoute(APIRouter):
    def __init__(self):
        super().__init__(prefix="/clientes/{customer_id}")
        self._transactions_router = TransactionsRouter()
        self._controller = CustomersController()
        self._setup_routes()

    def _setup_routes(self):
        self.get("/extrato")(self._controller.get_statement)
        self.include_router(self._transactions_router)
