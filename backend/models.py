class Book:
    """Base class representing a general book in the library."""
    
    def __init__(self, title: str, author: str, is_available: bool = True):
        self.title = title.strip()
        self.author = author.strip()
        self.is_available = is_available

    def display_details(self):
        status = "Available" if self.is_available else "Checked Out"
        print(f"Title: {self.title}")
        print(f"Author: {self.author}")
        print(f"Status: {status}")

    def check_availability(self) -> bool:
        return self.is_available

    def set_availability(self, status: bool):
        self.is_available = status


class FictionBook(Book):
    """Subclass representing fiction books."""
    
    def __init__(self, title: str, author: str, sub_genre: str, is_available: bool = True):
        super().__init__(title, author, is_available)
        self.sub_genre = sub_genre.strip()

    def display_details(self):
        super().display_details()
        print(f"Category: Fiction")
        print(f"Sub-Genre: {self.sub_genre}")


class NonFictionBook(Book):
    """Subclass representing non-fiction books."""
    
    def __init__(self, title: str, author: str, subject_area: str, is_available: bool = True):
        super().__init__(title, author, is_available)
        self.subject_area = subject_area.strip()

    def display_details(self):
        super().display_details()
        print(f"Category: Non-Fiction")
        print(f"Subject Area: {self.subject_area}")


class ReferenceBook(Book):
    """Subclass representing reference books (cannot be borrowed)."""
    
    def __init__(self, title: str, author: str, edition: str, is_available: bool = True):
        super().__init__(title, author, is_available)
        self.edition = edition.strip()

    def display_details(self):
        super().display_details()
        print(f"Category: Reference (Library Use Only)")
        print(f"Edition: {self.edition}")


class LibraryCatalog:
    """Manager class that handles the collection of books."""
    
    def __init__(self):
        self.catalog = []

    def add_book(self, book: Book):
        self.catalog.append(book)

    def remove_book(self, title: str) -> bool:
        for book in self.catalog:
            if book.title.lower() == title.lower():
                self.catalog.remove(book)
                return True
        return False

    def search_books(self, query: str):
        q = query.lower()
        return [
            book for book in self.catalog
            if q in book.title.lower() or q in book.author.lower()
        ]

    def get_available_books(self):
        return [book for book in self.catalog if book.is_available]

    def find_exact_book(self, title: str):
        for book in self.catalog:
            if book.title.lower() == title.lower():
                return book
        return None