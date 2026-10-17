from __future__ import annotations
from dataclasses import dataclass, field


class LibraryError(Exception):
    """Base exception for library-related errors."""


class DuplicateIDError(LibraryError):
    """Raised when an ID is already in use."""


class DuplicateTitleError(LibraryError):
    """Raised when a book title already exists."""


@dataclass
class Book:
    """Represents a book in the library catalog."""

    title: str
    id: int


@dataclass
class Reader:
    """Represents a library reader and the IDs of books they have read."""

    name: str
    id: int
    # Use a factory so each reader receives their own list.
    books_read: list[int] = field(default_factory=list)


class Library:
    """Manages readers, the book catalog, and reading histories."""

    def __init__(self) -> None:
        # Store readers and books by their IDs for quick lookup.
        self.readers: dict[int, Reader] = {}
        self.books: dict[int, Book] = {}

        # IDs are assigned automatically, starting at 1.
        self._next_reader_id = 1
        self._next_book_id = 1

    def create_reader(self, name: str) -> Reader | None:
        """Create a reader with a validated name and an automatically assigned ID."""
        name = _required_text(name, "Name")
        reader_id = self._next_reader_id

        # Avoid overwriting a reader if the next ID is already in use.
        if reader_id in self.readers:
            print(f"A reader with ID {reader_id} already exists.")
            return None

        reader = Reader(name=name, id=reader_id)
        self.readers[reader_id] = reader
        self._next_reader_id += 1
        return reader

    def update_reader(self, reader_id: int, name: str) -> bool:
        """Update a reader's name; return False if the reader does not exist."""
        reader = self.readers.get(reader_id)
        if reader is None:
            print(f"No reader with ID {reader_id} exists.")
            return False

        reader.name = _required_text(name, "Name")
        return True

    def delete_reader(self, reader_id: int) -> bool:
        """Delete a reader; return False if the reader does not exist."""
        if reader_id not in self.readers:
            print(f"No reader with ID {reader_id} exists.")
            return False

        del self.readers[reader_id]
        print(f"Reader with ID {reader_id} has been deleted.")
        return True

    def list_reader_books(self, reader_id: int) -> list[Book] | None:
        """Return the books a reader has read, or None if the reader is missing."""
        reader = self.readers.get(reader_id)
        if reader is None:
            print(f"No reader with ID {reader_id} exists.")
            return None

        # Ignore any IDs that no longer refer to books in the catalog.
        return [
            self.books[book_id]
            for book_id in reader.books_read
            if book_id in self.books
        ]

    def add_book(self, title: str, book_id: int | None = None) -> Book:
        """Add a book, assigning an ID when one is not provided."""
        title = _required_text(title, "Title")

        # Compare case-insensitively so titles differing only by letter case
        # are treated as duplicates.
        if any(
            book.title.casefold() == title.casefold()
            for book in self.books.values()
        ):
            raise DuplicateTitleError(f"A book titled '{title}' already exists.")

        if book_id is None:
            # Find the next available ID, in case the current one is occupied.
            book_id = self._next_book_id
            while book_id in self.books:
                book_id += 1
        elif not isinstance(book_id, int) or book_id < 1:
            raise ValueError("Book ID must be a positive integer.")

        if book_id in self.books:
            raise DuplicateIDError(f"A book with ID {book_id} already exists.")

        book = Book(title=title, id=book_id)
        self.books[book_id] = book

        # Keep the next automatic ID above every ID currently assigned.
        self._next_book_id = max(self._next_book_id, book_id + 1)
        return book

    def update_book(self, book_id: int, title: str) -> bool:
        """Change a book's title; return False if the book does not exist."""
        book = self.books.get(book_id)
        if book is None:
            print(f"No book with ID {book_id} exists.")
            return False

        title = _required_text(title, "Title")

        # Exclude the current book when checking for duplicate titles.
        if any(
            other.id != book_id
            and other.title.casefold() == title.casefold()
            for other in self.books.values()
        ):
            raise DuplicateTitleError(f"A book titled '{title}' already exists.")

        book.title = title
        print(f"Book with ID {book_id} has been updated.")
        return True

    def delete_book(self, book_id: int) -> bool:
        """Delete a book and remove its ID from all readers' histories."""
        if book_id not in self.books:
            print(f"No book with ID {book_id} exists.")
            return False

        del self.books[book_id]

        # Remove the deleted book from every reader's reading history.
        for reader in self.readers.values():
            if book_id in reader.books_read:
                reader.books_read.remove(book_id)

        print(f"Book with ID {book_id} has been deleted.")
        return True

    def register_book_read(self, reader_id: int, book_id: int) -> bool:
        """Record that a reader has read a book."""
        reader = self.readers.get(reader_id)
        if reader is None:
            print(f"No reader with ID {reader_id} exists.")
            return False

        if book_id not in self.books:
            print(f"No book with ID {book_id} exists.")
            return False

        # Add the book only once to avoid duplicate entries in the history.
        if book_id not in reader.books_read:
            reader.books_read.append(book_id)

        print(f"Book with ID {book_id} added to reader with ID {reader_id}.")
        return True


def _required_text(value: str, field_name: str) -> str:
    """Validate that a value is a non-empty string and return it trimmed."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} cannot be empty.")
    return value.strip()


def create_reader(library: Library, name: str) -> Reader | None:
    """Create and return a reader with an automatically assigned ID."""
    return library.create_reader(name)


def add_book(library: Library, title: str, book_id: int | None = None) -> Book:
    """Add a book; duplicate IDs or titles raise specific exceptions."""
    return library.add_book(title, book_id)


def delete_book(library: Library, book_id: int) -> bool:
    """Delete a book and remove it from every reader's history."""
    return library.delete_book(book_id)


def main() -> None:
    """Run the interactive command-line interface for the library."""
    library = Library()

    # Map menu choices to the labels displayed to the user.
    options = {
        "1": "Create reader",
        "2": "Update reader",
        "3": "Delete reader",
        "4": "Add book",
        "5": "Update book",
        "6": "Delete book",
        "7": "Register a book as read",
        "8": "List a reader's books",
        "9": "View catalog",
        "0": "Exit",
    }

    # Keep showing the menu until the user chooses to exit.
    while True:
        print("\n=== Library ===")
        for number, label in options.items():
            print(f"{number}. {label}")

        choice = input("Choose an options: ").strip()

        try:
            if choice == "0":
                print("Goodbye.")
                break

            elif choice == "1":
                reader = create_reader(library, input("Reader name: "))
                if reader:
                    print(f"Reader created: {reader.name} (ID {reader.id})")

            elif choice == "2":
                reader_id = int(input("Reader ID: "))
                if library.update_reader(reader_id, input("New name: ")):
                    print("Reader updated.")

            elif choice == "3":
                library.delete_reader(int(input("Reader ID: ")))

            elif choice == "4":
                book = add_book(library, input("Book title: "))
                print(f"Book added: {book.title} (ID {book.id}).")

            elif choice == "5":
                book_id = int(input("Book ID: "))
                if library.update_book(book_id, input("New title: ")):
                    print("Book updated.")

            elif choice == "6":
                delete_book(library, int(input("Book ID: ")))

            elif choice == "7":
                reader_id = int(input("Reader ID: "))
                book_id = int(input("Book ID: "))
                if library.register_book_read(reader_id, book_id):
                    print("Reading history updated.")

            elif choice == "8":
                books = library.list_reader_books(int(input("Reader ID: ")))
                if books is not None:
                    if books:
                        for book in books:
                            print(f"{book.id}: {book.title}")
                    else:
                        print("This reader has not read any books yet.")

            elif choice == "9":
                if library.books:
                    for book in library.books.values():
                        print(f"{book.id}: {book.title}")
                else:
                    print("The catalog is empty.")

            else:
                print("Invalid option.")

        # Handle invalid integer input and empty text values.
        except ValueError as error:
            print(f"Invalid input: {error}")

        # Handle library-specific errors such as duplicate IDs or titles.
        except LibraryError as error:
            print(f"The operation could not be completed: {error}")


# Run the command-line interface only when this file is executed directly.
if __name__ == "__main__":
    main()