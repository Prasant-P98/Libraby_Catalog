class Book {
    constructor(id, title, author, category, isAvailable = true) {
        this.id = id;
        this.title = title;
        this.author = author;
        this.category = category;
        this.isAvailable = isAvailable;
    }
}

class FictionBook extends Book {
    constructor(id, title, author, subGenre, isAvailable) {
        super(id, title, author, 'Fiction', isAvailable);
        this.subGenre = subGenre;
    }
}

class NonFictionBook extends Book {
    constructor(id, title, author, subjectArea, isAvailable) {
        super(id, title, author, 'NonFiction', isAvailable);
        this.subjectArea = subjectArea;
    }
}

class ReferenceBook extends Book {
    constructor(id, title, author, edition, isAvailable) {
        super(id, title, author, 'Reference', isAvailable);
        this.edition = edition;
    }
}

class LibraryCatalogManager {
    constructor() {
        this.catalog = [];
        this.seedData();
    }

    seedData() {
        this.addBook(new FictionBook(1, "Dune", "Frank Herbert", "Sci-Fi"));
        this.addBook(new NonFictionBook(2, "Sapiens", "Yuval Noah Harari", "History"));
        this.addBook(new ReferenceBook(3, "Oxford Dictionary", "Oxford Press", "11th Edition"));
    }

    addBook(book) {
        this.catalog.push(book);
    }

    removeBook(id) {
        this.catalog = this.catalog.filter(book => book.id !== id);
    }

    toggleStatus(id) {
        const book = this.catalog.find(b => b.id === id);
        if (book && !(book instanceof ReferenceBook)) {
            book.isAvailable = !book.isAvailable;
        }
    }
}

const manager = new LibraryCatalogManager();
let currentFilter = 'all';

document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    render();
});

function setupEventListeners() {
    document.getElementById('book-type').addEventListener('change', (e) => {
        const label = document.getElementById('dynamic-label');
        const input = document.getElementById('dynamic-val');
        if (e.target.value === 'Fiction') {
            label.innerText = 'Sub-Genre';
            input.placeholder = 'e.g., Sci-Fi';
        } else if (e.target.value === 'NonFiction') {
            label.innerText = 'Subject Area';
            input.placeholder = 'e.g., History';
        } else {
            label.innerText = 'Edition';
            input.placeholder = 'e.g., 2nd Edition';
        }
    });

    document.getElementById('add-book-form').addEventListener('submit', (e) => {
        e.preventDefault();
        const type = document.getElementById('book-type').value;
        const title = document.getElementById('book-title').value;
        const author = document.getElementById('book-author').value;
        const extra = document.getElementById('dynamic-val').value;

        const id = Date.now();
        let book;
        if (type === 'Fiction') book = new FictionBook(id, title, author, extra);
        else if (type === 'NonFiction') book = new NonFictionBook(id, title, author, extra);
        else book = new ReferenceBook(id, title, author, extra);

        manager.addBook(book);
        e.target.reset();
        render();
    });

    document.getElementById('search-input').addEventListener('input', render);

    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            currentFilter = e.target.dataset.filter;
            render();
        });
    });
}

function render() {
    const grid = document.getElementById('catalog-grid');
    const query = document.getElementById('search-input').value.toLowerCase();
    grid.innerHTML = '';

    let books = manager.catalog.filter(b => 
        b.title.toLowerCase().includes(query) || 
        b.author.toLowerCase().includes(query)
    );

    if (currentFilter === 'available') books = books.filter(b => b.isAvailable);
    if (currentFilter === 'borrowed') books = books.filter(b => !b.isAvailable);

    document.getElementById('total-count').innerText = manager.catalog.length;
    document.getElementById('avail-count').innerText = manager.catalog.filter(b => b.isAvailable).length;
    document.getElementById('borrowed-count').innerText = manager.catalog.filter(b => !b.isAvailable).length;

    books.forEach(book => {
        const extraDetail = book.subGenre ? `Sub-Genre: ${book.subGenre}` :
                            book.subjectArea ? `Subject: ${book.subjectArea}` :
                            `Edition: ${book.edition}`;

        const card = document.createElement('div');
        card.className = 'book-card';
        card.innerHTML = `
            <div>
                <span class="badge ${book.category}">${book.category}</span>
                <h3>${book.title}</h3>
                <p>by ${book.author}</p>
                <div class="book-meta">
                    <div>${extraDetail}</div>
                    <div style="margin-top: 5px;">
                        <span class="status-indicator ${book.isAvailable ? 'available' : 'borrowed'}"></span>
                        <strong>${book.isAvailable ? 'Available' : 'Checked Out'}</strong>
                    </div>
                </div>
            </div>
            <div class="card-actions">
                ${book instanceof ReferenceBook ? 
                    `<button class="btn-sm" disabled style="opacity:0.6; cursor:not-allowed;">Ref Only</button>` : 
                    `<button class="btn-sm ${book.isAvailable ? 'btn-borrow' : 'btn-return'}" onclick="toggleBook(${book.id})">
                        ${book.isAvailable ? 'Borrow' : 'Return'}
                    </button>`
                }
                <button class="btn-sm btn-delete" onclick="deleteBook(${book.id})">Delete</button>
            </div>
        `;
        grid.appendChild(card);
    });
}

function toggleBook(id) {
    manager.toggleStatus(id);
    render();
}

function deleteBook(id) {
    manager.removeBook(id);
    render();
}