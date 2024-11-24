from typing import Self
from decimal import Decimal
from uuid import UUID
from dataclasses import dataclass

from app.domain.value_objects import AccountId, Amount
from app.domain.bank_account import BankAccount
from app.application.interfaces import AccountReader


@dataclass(frozen=True)
class AccountResponse:
    id: UUID
    balance: Decimal
    withdrawal_limit: Decimal

    @staticmethod
    def from_bank_account(bank_account: BankAccount) -> 'AccountResponse':
        return AccountResponse(
            id = bank_account.id.uuid,
            balance = bank_account.balance.amount,
            withdrawal_limit = bank_account.withdrawal_limit.amount
        )


class GetBankAccountBalanceQueryHandler:
    def __init__(self: Self, account_reader: AccountReader) -> None:
        self.account_reader: AccountReader = account_reader

    async def __call__(self: Self, account_id: UUID) -> Decimal:
        account_uuid: AccountId = AccountId(uuid = account_id)
        balance: Amount = await self.account_reader.get_account_balance(
            account_id = account_uuid
        )

        return balance.amount
    

class GetBankAccountQueryHandler:
    def __init__(self: Self, account_reader: AccountReader) -> None:
        self.account_reader: AccountReader = account_reader

    async def __call__(self: Self, account_id: UUID) -> AccountResponse:
        account_uuid: AccountId = AccountId(uuid = account_id)
        bank_account: BankAccount = await self.account_reader.get_account(
            account_id = account_uuid
        )

        return AccountResponse.from_bank_account(bank_account = bank_account)