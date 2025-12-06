#!/usr/bin/env python3
import logging
import sys

# Configure logging (safe to do at module level)
logging.basicConfig(
    filename="library.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def safe_input(prompt: str) -> str:
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print("\nExiting...")
        sys.exit(0)

def add_book_interactive(inventory, Book):
    title = safe_input("Title: ")
    author = safe_input("Author: ")
    isbn = safe_input("ISBN: ")
    if not title or not author or not isbn:
        print("Title, author and ISBN are required.")
        return
    book = Book(title, author, isbn)
    try:
        inventory.add_book(book)
        inventory.save_to_file()
        logging.info("Added book: %s by %s (ISBN=%s)", title, author, isbn)
        print("Book added successfully.")
    except Exception as exc:
        logging.exception("Failed to add book: %s", exc)
        print("Failed to add book. See library.log for details.")

def issue_book_by_isbn(inventory, isbn):
    books = inventory.search_by_isbn(isbn)
    if not books:
        return False
    for b in books:
        try:
            if b.issue():
                logging.info("Issued book: %s | ISBN: %s", getattr(b, "title", "Unknown"), isbn)
                return True
        except Exception as exc:
            logging.exception("Error issuing book (ISBN=%s): %s", isbn, exc)
            continue
    return False

def return_book_by_isbn(inventory, isbn):
    books = inventory.search_by_isbn(isbn)
    if not books:
        return False
    for b in books:
        try:
            if b.return_book():
                logging.info("Returned book: %s | ISBN: %s", getattr(b, "title", "Unknown"), isbn)
                return True
        except Exception as exc:
            logging.exception("Error returning book (ISBN=%s): %s", isbn, exc)
            continue
    return False

def main():
    # Local imports to avoid circular-import problems and to ensure names exist before use
    from librarymanagerinventory import LibraryInventory
    from librarymanagerbook import Book

    inventory = LibraryInventory()
    try:
        inventory.load_from_file()
    except Exception as exc:
        logging.exception("Failed to load inventory from file: %s", exc)
        print("Warning: could not load inventory. Starting with empty inventory.")

    while True:
        print("\n--- Library Menu ---")
        print("1. Add Book")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. View All Books")
        print("5. Search Book")
        print("6. Exit")

        choice = safe_input("Enter choice: ")

        if choice == "1":
            add_book_interactive(inventory, Book)

        elif choice == "2":
            isbn = safe_input("Enter ISBN to issue: ")
            if not isbn:
                print("ISBN required.")
                continue
            success = issue_book_by_isbn(inventory, isbn)
            if success:
                try:
                    inventory.save_to_file()
                except Exception:
                    logging.exception("Failed to save inventory after issuing ISBN=%s", isbn)
                print("Book issued.")
            else:
                print("Book not available.")

        elif choice == "3":
            isbn = safe_input("Enter ISBN to return: ")
            if not isbn:
                print("ISBN required.")
                continue
            success = return_book_by_isbn(inventory, isbn)
            if success:
                try:
                    inventory.save_to_file()
                except Exception:
                    logging.exception("Failed to save inventory after returning ISBN=%s", isbn)
                print("Book returned.")
            else:
                print("Book not issued or not found.")

        elif choice == "4":
            try:
                books = inventory.display_all()
                if not books:
                    print("No books in inventory.")
                else:
                    for b in books:
                        print(b)
            except Exception as exc:
                logging.exception("Failed to display all books: %s", exc)
                print("Failed to display books. See library.log for details.")

        elif choice == "5":
            title = safe_input("Enter title: ")
            if not title:
                print("Title required.")
                continue
            try:
                results = inventory.search_by_title(title)
                if results:
                    for b in results:
                        print(b)
                else:
                    print("No book found.")
            except Exception as exc:
                logging.exception("Search failed for title=%s: %s", title, exc)
                print("Search failed. See library.log for details.")

        elif choice == "6":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()