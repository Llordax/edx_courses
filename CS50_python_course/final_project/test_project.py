# Import pytest to use its test helpers, including exception checks.
import pytest

# Import the library classes, exceptions, and helper functions being tested.
from project import (
    DuplicateIDError,
    DuplicateTitleError,
    Library,
    add_book,
    create_reader,
    delete_book,
)


def test_create_reader():
    """Check that readers receive sequential IDs and separate reading histories."""
    library = Library()

    # Create two readers through the public helper function.
    first = create_reader(library, "Ana")
    second = create_reader(library, "Luis")

    # IDs start at 1 and increase with each new reader.
    assert first.id == 1
    assert second.id == 2

    # A new reader should have an empty reading history.
    assert first.books_read == []


def test_add_book():
    """Check that duplicate book IDs and titles raise the right exceptions."""
    library = Library()
    add_book(library, "The Library", 10)

    # Reusing an existing ID should raise DuplicateIDError.
    with pytest.raises(DuplicateIDError):
        add_book(library, "Another title", 10)

    # Titles are compared without regard to capitalization.
    with pytest.raises(DuplicateTitleError):
        add_book(library, "the LIBRARY", 11)


def test_delete_book():
    """Check that deleting a book removes it from the catalog and reading history."""
    library = Library()
    reader = create_reader(library, "Ana")
    book = add_book(library, "The Book")

    # Record that the reader has read the book before deleting it.
    library.register_book_read(reader.id, book.id)

    # Deletion should succeed and remove the book from the catalog.
    assert delete_book(library, book.id) is True
    assert book.id not in library.books

    # The deleted book should also be removed from the reader's history.
    assert reader.books_read == []
    assert library.list_reader_books(reader.id) == []


def test_update_book():
    """Check that updating a book to an existing title is rejected."""
    library = Library()
    first = add_book(library, "First")
    add_book(library, "Second")

    # A duplicate title should raise an exception and leave the original unchanged.
    with pytest.raises(DuplicateTitleError):
        library.update_book(first.id, "Second")

    assert first.title == "First"