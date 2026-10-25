from models import FictionBook, NonFictionBook, ReferenceBook, LibraryCatalog


def seed_initial_data(catalog: LibraryCatalog):
    catalog.add_book(FictionBook("Dune", "Frank Herbert", "Sci-Fi"))
    catalog.add_book(NonFictionBook("Sapiens", "Yuval Noah Harari", "History"))
    catalog.add_book(ReferenceBook("Encyclopedia Britannica", "Britannica Inc", "15th Edition"))


def print_menu():
    print("\n" + "=" * 45)
    print("      LIBRARY CATALOG SYSTEM (CLI)")
    print("=" * 45)
    print("1. Add a New Book")
    print("2. Remove a Book")
    print("3. Search for Books")
    print("4. Display Available Books")
    print("5. Borrow a Book")
    print("6. Return a Book")
    print("7. Exit")
    print("=" * 45)


def handle_add(catalog: LibraryCatalog):
    print("\n--- Select Category ---")
    print("1. Fiction")
    print("2. Non-Fiction")
    print("3. Reference")
    cat = input("Choice (1-3): ").strip()

    title = input("Enter Title: ").strip()
    author = input("Enter Author: ").strip()

    if not title or not author:
        print("\n[Error] Title and Author cannot be empty.")
        return

    if cat == "1":
        sub_genre = input("Enter Sub-Genre (e.g. Sci-Fi): ").strip()
        catalog.add_book(FictionBook(title, author, sub_genre))
    elif cat == "2":
        subject = input("Enter Subject Area (e.g. History): ").strip()
        catalog.add_book(NonFictionBook(title, author, subject))
    elif cat == "3":
        edition = input("Enter Edition (e.g. 1st Edition): ").strip()
        catalog.add_book(ReferenceBook(title, author, edition))
    else:
        print("\n[Error] Invalid category selection.")
        return

    print(f"\n[Success] '{title}' successfully added!")


def handle_borrow(catalog: LibraryCatalog):
    title = input("\nEnter Title to Borrow: ").strip()
    book = catalog.find_exact_book(title)

    if not book:
        print(f"\n[Error] Book '{title}' not found.")
        return
    if isinstance(book, ReferenceBook):
        print(f"\n[Notice] '{book.title}' is a Reference book and cannot be checked out.")
        return
    if not book.check_availability():
        print(f"\n[Notice] '{book.title}' is currently checked out.")
        return

    book.set_availability(False)
    print(f"\n[Success] You borrowed '{book.title}'.")


def handle_return(catalog: LibraryCatalog):
    title = input("\nEnter Title to Return: ").strip()
    book = catalog.find_exact_book(title)

    if not book:
        print(f"\n[Error] Book '{title}' not found.")
        return
    if book.check_availability():
        print(f"\n[Notice] '{book.title}' is already in the library.")
        return

    book.set_availability(True)
    print(f"\n[Success] You returned '{book.title}'.")


def main():
    catalog = LibraryCatalog()
    seed_initial_data(catalog)

    while True:
        print_menu()
        choice = input("Enter option (1-7): ").strip()

        if choice == "1":
            handle_add(catalog)
        elif choice == "2":
            t = input("\nEnter title to remove: ").strip()
            if catalog.remove_book(t):
                print(f"[Success] Removed '{t}'.")
            else:
                print(f"[Error] Book '{t}' not found.")
        elif choice == "3":
            q = input("\nEnter search query: ").strip()
            res = catalog.search_books(q)
            print(f"\nFound {len(res)} book(s):")
            for b in res:
                print("-" * 20)
                b.display_details()
        elif choice == "4":
            books = catalog.get_available_books()
            print(f"\nAvailable Books ({len(books)}):")
            for b in books:
                print("-" * 20)
                b.display_details()
        elif choice == "5":
            handle_borrow(catalog)
        elif choice == "6":
            handle_return(catalog)
        elif choice == "7":
            print("\nExiting Library System. Goodbye!")
            break
        else:
            print("[Error] Invalid option. Enter 1-7.")


if __name__ == "__main__":
    main()