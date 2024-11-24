from app.domain.bank_account import BankAccount
from app.domain.value_objects import Amount, AccountId
from app.domain.events import AccountCreated, BaseDomainEvent, AccountCredited, AccountDebited, WithdrawalLimitChanged
from app.domain.exceptions import StateRestoringError


class BankAccountFactory:
    @staticmethod
    def create_account(id: AccountId, balance: Amount) -> BankAccount: 
        withdrawal_limit: Amount = Amount(1000.0)
        account: BankAccount = BankAccount(id=id, balance=balance, withdrawal_limit=withdrawal_limit)

        event: AccountCreated = AccountCreated(
            agregate_id=id.uuid,
            account_id=id.uuid,
            balance=balance.amount,
            withdrawal_limit=withdrawal_limit.amount
        )

        account.add_event(event=event)
        return account