from fastapi import Response

from services.customers import CustomersService


class CustomersController:
    def __init__(self):
        self._service = CustomersService()

    async def get_statement(self, customer_id: int, response: Response) -> dict:
        statement = self._service.get_statement(customer_id)
        if statement is None:
            response.status_code = 404
            return {"message": f"customer with id {customer_id} not found"}
        response.status_code = 200
        return statement.model_dump()
