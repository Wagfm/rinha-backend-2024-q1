from fastapi import FastAPI

from routes.customers import CustomersRoute

router = CustomersRoute()
app = FastAPI()
app.include_router(router)
