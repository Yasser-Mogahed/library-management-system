"""Demo of the Library Management System."""
from datetime import date, timedelta

from library import (
    DVD, Book, FacultyMember, Library, LibraryError, Magazine, StudentMember,
)


def section(title: str) -> None:
    print(f"\n=== {title} ===")


def main() -> None:
    lib = Library("Central University Library")

    section("Adding items and members")
    lib.add_item(Book("B1", "Clean Code", 2008, "Robert C. Martin", 464))
    lib.add_item(Book("B2", "Fluent Python", 2015, "Luciano Ramalho", 792))
    lib.add_item(Magazine("M1", "Wired", 2024, 5))
    lib.add_item(DVD("D1", "The Social Network", 2010, 120))
    lib.register_member(StudentMember("S1", "Yasser", "yasser@example.com"))
    lib.register_member(FacultyMember("F1", "Dr. Amira", "amira@example.com"))

    for item in lib.available_items():   # polymorphism: describe() differs per class
        print(item)

    section("Borrowing")
    lib.borrow_item("S1", "B1")
    lib.borrow_item("S1", "M1")
    print(lib.get_member("S1"))

    section("Error handling")
    attempts = [
        ("F1", "B1"),        # already on loan
        ("S9", "B2"),        # unknown member
        ("S1", "X99"),       # unknown item
    ]
    for member_id, item_id in attempts:
        try:
            lib.borrow_item(member_id, item_id)
        except LibraryError as error:
            print(f"  ! {type(error).__name__}: {error}")

    lib.borrow_item("S1", "D1")
    try:
        lib.borrow_item("S1", "B2")      # student limit is 3
    except LibraryError as error:
        print(f"  ! {type(error).__name__}: {error}")

    section("Returning (late DVD, 5 days overdue)")
    fine = lib.return_item("S1", "D1", today=date.today() + timedelta(days=3 + 5))
    print(f"Fine charged: ${fine:.2f}")

    section("Search")
    for item in lib.search("python"):
        print(item)

    print(f"\nTotal items created: {Book.total_created()}")


if __name__ == "__main__":
    main()
