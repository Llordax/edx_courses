Library Management System

#### Video Demo: https://youtu.be/Z2HGmgB8SXQ

#### Description

This project is a Python command-line application for managing a small library. It lets users register readers, maintain a book catalog, and record the books each reader has finished. The application keeps information in memory for the current session, so all data is cleared when the program exits. This keeps the project easy to install while focusing on object-oriented programming, input validation, and relationships between data.

The application assigns integer IDs automatically to readers and books. Each reader has a name, an ID, and a list of the IDs of books they have read. Each book has a title and an ID, and books are stored in a dictionary keyed by ID. Titles cannot be duplicated, even when capitalization differs. This prevents the catalog from containing multiple entries for the same title. The project defines custom exceptions for duplicate IDs and duplicate titles so that code using the library can handle each error separately.

The interactive menu can create, update, and delete readers; add, rename, and delete books; record a book as read; view a reader's reading history; and display the full catalog. Reader IDs are assigned when readers are created, and the application does not provide an operation to change them. When a book is deleted, the library automatically removes its ID from every reader's history. A reader cannot register the same book more than once. Operations that receive an ID that does not exist display a message and leave the data unchanged.

`project.py` contains the `Reader` and `Book` classes, the `Library` class and its management operations, the custom exceptions, and the main menu. It also defines top-level functions for creating readers, adding books, and deleting books. These functions provide a simple interface and meet the project requirement for additional top-level functions. The `main` function displays the menu and validates user input, including IDs that must be converted to integers.

`test_project.py` contains automated tests written with pytest. They check that IDs are assigned incrementally, duplicate IDs and titles are rejected, deleting a book clears it from reading histories, and a book cannot be renamed to a title that is already in use. To start the application, run `python project.py`. To run the tests, install pytest with `pip install pytest` and run `pytest` from the project folder. The application itself has no third-party dependencies, so a `requirements.txt` file is not needed.
