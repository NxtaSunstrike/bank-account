from typing import Self
from dataclasses import dataclass
from uuid import UUID
from decimal import Decimal

from app.domain.exceptions import ValidationError


@dataclass(frozen=True)
class AccountId:
    uuid: UUID

    def __post_init__(self: Self) -> None:
        if self.id is None:
            raise ValidationError(messgae='id must not be empty')
        if not isinstance(self.id, UUID):
            raise ValidationError(message=f'id must be UUID, not {type(self.id)}')
        

@dataclass(frozen=True)
class Amount:
    amount: Decimal
    
    def __post_init__(self: Self) -> None:
        if self.amount is None:
            raise ValidationError(messgae='amount must not be empty')
        if not isinstance(self.amount, Decimal):
            raise ValidationError(message=f'amount must be Decimal, not {type(self.amount)}')
        if self.amount < 0:
            raise ValidationError(message=f'amount must be positive, not {self.amount}')
    