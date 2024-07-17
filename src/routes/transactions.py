from fastapi import APIRouter

from controllers.transactions import TransactionsController


class TransactionsRouter(APIRouter):
    def __init__(self):
        super().__init__()
        self._controller = TransactionsController()
        self._setup_routes()

    def _setup_routes(self):
        self.post("/transacoes")(self._controller.create_transaction)
