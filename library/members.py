"""Members: abstraction, inheritance, and polymorphic borrowing rules."""
import re
from abc import ABC, abstractmethod
from typing import Tuple

from .exceptions import InvalidDataError, LoanNotFoundError
from .models import Loan

_EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class Person(ABC):
    """Abstract person with validated name and email."""

    def __init__(self, name: str, email: str):
        if not name or not name.strip():
            raise InvalidDataError("Name cannot be empty.")
        if not _EMAIL_PATTERN.match(email or ""):
            raise InvalidDataError(f"Invalid email: {email!r}")
        self._name = name.strip()
        self._email = email

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email

    @property
    @abstractmethod
    def role(self) -> str:
        """Role label shown in reports."""


class Member(Person, ABC):
    """A library member. Subclasses define limits and fines (polymorphism)."""

    def __init__(self, member_id: str, name: str, email: str):
        super().__init__(name, email)
        if not member_id or not member_id.strip():
            raise InvalidDataError("Member ID cannot be empty.")
        self._member_id = member_id.strip()
        self._loans: list[Loan] = []   # composition: loans live and die with the member

    @property
    def member_id(self) -> str:
        return self._member_id

    @property
    @abstractmethod
    def max_loans(self) -> int:
        """Maximum number of items borrowed at the same time."""

    @property
    @abstractmethod
    def fine_per_day(self) -> float:
        """Fine charged per overdue day."""

    @property
    def active_loans(self) -> Tuple[Loan, ...]:
        return tuple(self._loans)  # immutable copy protects internal state

    def can_borrow(self) -> bool:
        return len(self._loans) < self.max_loans

    def add_loan(self, loan: Loan) -> None:
        self._loans.append(loan)

    def remove_loan(self, item_id: str) -> Loan:
        for loan in self._loans:
            if loan.item.item_id == item_id:
                self._loans.remove(loan)
                return loan
        raise LoanNotFoundError(f"{self._name} has not borrowed item '{item_id}'.")

    def __str__(self) -> str:
        return f"{self.role} {self._name} ({self._member_id}) - {len(self._loans)}/{self.max_loans} loans"


class StudentMember(Member):
    @property
    def role(self) -> str:
        return "Student"

    @property
    def max_loans(self) -> int:
        return 3

    @property
    def fine_per_day(self) -> float:
        return 0.50


class FacultyMember(Member):
    @property
    def role(self) -> str:
        return "Faculty"

    @property
    def max_loans(self) -> int:
        return 10

    @property
    def fine_per_day(self) -> float:
        return 0.25
