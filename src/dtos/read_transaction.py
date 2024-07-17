from pydantic import BaseModel, model_validator, ValidationError


class ReadTransactionDto(BaseModel):
    success: bool
    limite: int
    saldo: int

    @model_validator(mode="after")
    def validate(self) -> "ReadTransactionDto":
        if self.saldo < self.limite * -1:
            raise ValidationError("Inconsistent post transaction state")
        return self

    @staticmethod
    def from_english_fields(data: dict) -> "ReadTransactionDto":
        return ReadTransactionDto(**{
            "success": data["success"],
            "limite": data["current_limit"],
            "saldo": data["new_balance"]
        })

    def get_body_data(self) -> dict:
        return {"limite": self.limite, "saldo": self.saldo}
