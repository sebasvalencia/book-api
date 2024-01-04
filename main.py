from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


# Base book model
class Book(BaseModel):
    title: str
    author: str
    publication_year: int


# Basic book list
books: list[Book] = [
    Book(
        title="El señor de los anillos", author="J.R.R. Tolkien", publication_year=1954
    ),
    Book(title="1984", author="George Orwell", publication_year=1949),
    Book(
        title="Cien años de soledad",
        author="Gabriel García Márquez",
        publication_year=1967,
    ),
    Book(title="To Kill a Mockingbird", author="Harper Lee", publication_year=1960),
    Book(
        title="Harry Potter y la piedra filosofal",
        author="J.K. Rowling",
        publication_year=1997,
    ),
]


# Basic CRUD
@app.get("/books", response_model=List[Book])
def get_books(skip: int = 0, limit: int = 10):
    return books[skip : skip + limit]


@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    if book_id < 0 or book_id >= len(books):
        raise HTTPException(status_code=404, detail="Book not found")
    return books[book_id]


@app.post("/books/", response_model=Book)
def create_book(book: Book):
    print("book: ", book)
    print(type(book))
    books.append(book)
    return book


@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book: Book):
    try:
        if book_id < 0 or book_id >= len(books):
            raise HTTPException(status_code=404, detail="Book not found")
        books[book_id] = book
        return book
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/books/{book_id}", response_model=Book)
def delete_book(book_id: int):
    if book_id < 0 or book_id >= len(books):
        raise HTTPException(status_code=404, detail="Book not found")
    book = books.pop(book_id)
    return book