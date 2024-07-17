from pydantic import BaseModel


class ReadStatementDto(BaseModel):
    saldo: dict
    ultimas_transacoes: list
