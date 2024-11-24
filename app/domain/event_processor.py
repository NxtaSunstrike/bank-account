from app.domain.events import BaseDomainEvent, AccountCreated, AccountCredited, AccountDebited, WithdrawalLimitChanged
from app.domain.value_objects import AccountId, Amount
from app.domain.bank_account import BankAccount
from app.domain.exceptions import StateRestoringError


class EventStateProccessor:
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