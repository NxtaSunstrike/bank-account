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

    @staticmethod
    async def get_bank_account_state(events: list[BaseDomainEvent]) -> BankAccount:
        if not isinstance(events[0], AccountCreated):
            raise StateRestoringError("Invalid event type")
        first_event: AccountCreated = events[0]
        bank_account: BankAccount = BankAccount(
            id=AccountId(first_event.account_id),
            balance=Amount(first_event.balance),
            withdrawal_limit=Amount(first_event.withdrawal_limit)
        )

        for event in events[1:]:
            if isinstance(event, AccountCredited) or isinstance(event, AccountDebited):
                bank_account.balance = Amount(event.amount)
            if isinstance(event, WithdrawalLimitChanged):
                bank_account.withdrawal_limit = Amount(event.amount)

        return bank_account