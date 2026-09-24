"""Custom exceptions for the Library Management System."""


class LibraryError(Exception):
    """Base class for every error raised by this project."""


class InvalidDataError(LibraryError):
    """Raised when an object is created with invalid data."""


class ItemNotFoundError(LibraryError):
    """Raised when a library item ID does not exist."""


class MemberNotFoundError(LibraryError):
    """Raised when a member ID does not exist."""


class ItemNotAvailableError(LibraryError):
    """Raised when trying to borrow an item that is already on loan."""


class BorrowLimitExceededError(LibraryError):
    """Raised when a member tries to exceed their borrowing limit."""


class LoanNotFoundError(LibraryError):
    """Raised when returning an item the member did not borrow."""
