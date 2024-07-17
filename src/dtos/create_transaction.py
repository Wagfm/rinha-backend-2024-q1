from pydantic import BaseModel, field_validator


class CreateTransactionDto(BaseModel):
    valor: int
    tipo: str
    descricao: str

    @field_validator("valor")
    @classmethod
    def validate_valor(cls, valor: int) -> int:
        if valor < 0:
            raise ValueError("valor must be positive")
        return valor

    @field_validator("tipo")
    @classmethod
    def validate_tipo(cls, tipo: str) -> str:
        if tipo not in ["c", "d"]:
            raise ValueError("tipo must be c or d")
        return tipo

    @field_validator("descricao")
    @classmethod
    def validate_descricao(cls, descricao: str) -> str:
        if len(descricao) < 1:
            raise ValueError("descricao must be at least 1 character")
        if len(descricao) > 10:
            raise ValueError("descricao must be 10 or less characters")
        return descricao
