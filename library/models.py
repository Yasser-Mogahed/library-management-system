"""Library items (abstraction, inheritance, polymorphism) and loans (composition)."""
from abc import ABC, abstractmethod
from datetime import date, timedelta
from typing import Optional

from .exceptions import InvalidDataError, ItemNotAvailableError


class LibraryItem(ABC):
    """Abstract base class for everything the library can lend."""

    _items_created = 0  # class-level (static) member shared by all items

    def __init__(self, item_id: str, title: str, year: int):
        if not item_id or not item_id.strip():
            raise InvalidDataError("Item ID cannot be empty.")
        if not title or not title.strip():
            raise InvalidDataError("Title cannot be empty.")
        if not isinstance(year, int) or not 1000 <= year <= date.today().year:
            raise InvalidDataError(f"Invalid publication year: {year!r}")

        self._item_id = item_id.strip()      # protected (convention)
        self._title = title.strip()
        self._year = year
        self.__available = True              # private (name-mangled)
        LibraryItem._items_created += 1

    # ---- encapsulation: read-only access through properties ----
    @property
    def item_id(self) -> str:
        return self._item_id

    @property
    def title(self) -> str:
        return self._title

    @property
    def year(self) -> int:
        return self._year

    @property
    def is_available(self) -> bool:
        return self.__available

    def checkout(self) -> None:
        if not self.__available:
            raise ItemNotAvailableError(f"'{self._title}' is already on loan.")
        self.__available = False

    def give_back(self) -> None:
        self.__available = True

    @classmethod
    def total_created(cls) -> int:
        return LibraryItem._items_created

    # ---- abstraction: subclasses must implement these ----
    @property
    @abstractmethod
    def loan_period_days(self) -> int:
        """How many days the item can be borrowed."""

    @abstractmethod
    def describe(self) -> str:
        """Human-readable description of the item."""

    def __str__(self) -> str:
        status = "available" if self.is_available else "on loan"
        return f"[{self._item_id}] {self.describe()} ({status})"


class Book(LibraryItem):
    def __init__(self, item_id: str, title: str, year: int, author: str, pages: int):
        super().__init__(item_id, title, year)
        if not author.strip():
            raise InvalidDataError("Author cannot be empty.")
        if pages <= 0:
            raise InvalidDataError("Pages must be positive.")
        self._author = author.strip()
        self._pages = pages

    @property
    def author(self) -> str:
        return self._author

    @property
    def loan_period_days(self) -> int:
        return 21

    def describe(self) -> str:
        return f"Book: '{self._title}' by {self._author}, {self._year}, {self._pages} pages"


class Magazine(LibraryItem):
    def __init__(self, item_id: str, title: str, year: int, issue: int):
        super().__init__(item_id, title, year)
        if issue <= 0:
            raise InvalidDataError("Issue number must be positive.")
        self._issue = issue

    @property
    def loan_period_days(self) -> int:
        return 7

    def describe(self) -> str:
        return f"Magazine: '{self._title}' issue #{self._issue}, {self._year}"


class DVD(LibraryItem):
    def __init__(self, item_id: str, title: str, year: int, duration_min: int):
        super().__init__(item_id, title, year)
        if duration_min <= 0:
            raise InvalidDataError("Duration must be positive.")
        self._duration_min = duration_min

    @property
    def loan_period_days(self) -> int:
        return 3

    def describe(self) -> str:
        return f"DVD: '{self._title}', {self._year}, {self._duration_min} min"


class Loan:
    """Records that a member borrowed an item (a Loan cannot exist without an item)."""

    def __init__(self, item: LibraryItem, member_id: str, borrowed_on: date):
        self.item = item
        self.member_id = member_id
        self.borrowed_on = borrowed_on
        self.due_date = borrowed_on + timedelta(days=item.loan_period_days)
        self.returned_on: Optional[date] = None

    def days_overdue(self, on: date) -> int:
        return max(0, (on - self.due_date).days)

    def __str__(self) -> str:
        return f"{self.item.title} (due {self.due_date.isoformat()})"
