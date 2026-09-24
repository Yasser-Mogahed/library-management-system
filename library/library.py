"""The Library service: coordinates items, members and loans."""
from datetime import date
from typing import Dict, List, Optional

from .exceptions import (
    BorrowLimitExceededError,
    ItemNotAvailableError,
    ItemNotFoundError,
    MemberNotFoundError,
)
from .members import Member
from .models import LibraryItem, Loan
from .notifier import ConsoleNotifier, Notifier


class Library:
    def __init__(self, name: str, notifier: Optional[Notifier] = None):
        self.name = name
        self._items: Dict[str, LibraryItem] = {}
        self._members: Dict[str, Member] = {}
        self._notifier = notifier or ConsoleNotifier()  # dependency injection

    # ---- catalogue management (aggregation: items/members exist independently) ----
    def add_item(self, item: LibraryItem) -> None:
        self._items[item.item_id] = item

    def register_member(self, member: Member) -> None:
        self._members[member.member_id] = member

    def get_item(self, item_id: str) -> LibraryItem:
        try:
            return self._items[item_id]
        except KeyError:
            raise ItemNotFoundError(f"No item with ID '{item_id}'.") from None

    def get_member(self, member_id: str) -> Member:
        try:
            return self._members[member_id]
        except KeyError:
            raise MemberNotFoundError(f"No member with ID '{member_id}'.") from None

    def search(self, keyword: str) -> List[LibraryItem]:
        keyword = keyword.lower()
        return [i for i in self._items.values() if keyword in i.title.lower()]

    def available_items(self) -> List[LibraryItem]:
        return [i for i in self._items.values() if i.is_available]

    # ---- core operations ----
    def borrow_item(self, member_id: str, item_id: str, today: Optional[date] = None) -> Loan:
        today = today or date.today()
        member = self.get_member(member_id)
        item = self.get_item(item_id)

        if not item.is_available:
            raise ItemNotAvailableError(f"'{item.title}' is already on loan.")
        if not member.can_borrow():
            raise BorrowLimitExceededError(
                f"{member.name} reached the limit of {member.max_loans} loans."
            )

        item.checkout()
        loan = Loan(item, member.member_id, today)
        member.add_loan(loan)
        self._notifier.send(member.email, f"You borrowed '{item.title}'. Due {loan.due_date}.")
        return loan

    def return_item(self, member_id: str, item_id: str, today: Optional[date] = None) -> float:
        """Returns the item and gives back the fine (0.0 if on time)."""
        today = today or date.today()
        member = self.get_member(member_id)
        loan = member.remove_loan(item_id)  # raises LoanNotFoundError if not borrowed
        loan.returned_on = today
        loan.item.give_back()

        fine = loan.days_overdue(today) * member.fine_per_day
        message = f"You returned '{loan.item.title}'."
        if fine:
            message += f" Late fine: ${fine:.2f}."
        self._notifier.send(member.email, message)
        return fine
