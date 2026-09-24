import unittest
from datetime import date, timedelta

from library import (
    Book, BorrowLimitExceededError, FacultyMember, InvalidDataError,
    ItemNotAvailableError, LibraryItem, Library, LoanNotFoundError,
    SilentNotifier, StudentMember,
)


class LibraryTests(unittest.TestCase):
    def setUp(self):
        self.lib = Library("Test", notifier=SilentNotifier())
        for i in range(1, 5):
            self.lib.add_item(Book(f"B{i}", f"Book {i}", 2020, "Author", 100))
        self.lib.register_member(StudentMember("S1", "Sara", "sara@example.com"))
        self.lib.register_member(FacultyMember("F1", "Omar", "omar@example.com"))

    def test_cannot_instantiate_abstract_class(self):
        with self.assertRaises(TypeError):
            LibraryItem("X", "Title", 2020)

    def test_invalid_data(self):
        with self.assertRaises(InvalidDataError):
            Book("", "Title", 2020, "A", 10)
        with self.assertRaises(InvalidDataError):
            StudentMember("S2", "Bad", "not-an-email")

    def test_borrow_and_double_borrow(self):
        self.lib.borrow_item("S1", "B1")
        with self.assertRaises(ItemNotAvailableError):
            self.lib.borrow_item("F1", "B1")

    def test_limits_differ_by_member_type(self):
        for i in (1, 2, 3):
            self.lib.borrow_item("S1", f"B{i}")
        with self.assertRaises(BorrowLimitExceededError):
            self.lib.borrow_item("S1", "B4")
        self.lib.borrow_item("F1", "B4")  # faculty is still fine

    def test_fine_calculation(self):
        start = date(2025, 1, 1)
        self.lib.borrow_item("S1", "B1", today=start)
        fine = self.lib.return_item("S1", "B1", today=start + timedelta(days=21 + 4))
        self.assertAlmostEqual(fine, 2.0)

    def test_return_without_borrow(self):
        with self.assertRaises(LoanNotFoundError):
            self.lib.return_item("S1", "B1")


if __name__ == "__main__":
    unittest.main()
