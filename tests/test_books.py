from fastapi import HTTPException
from fastapi.testclient import TestClient
from main import app
from routers.books import Book, books

client = TestClient(app)


def test_get_books():
    # Test case 1: Test the default values of skip and limit
    response = client.get("/api/v1/books")
    assert response.status_code == 200
    assert len(response.json()) == 5

    # Test case 2: Test the skip and limit values
    response = client.get("/api/v1/books?skip=1&limit=3")
    assert response.status_code == 200
    assert len(response.json()) == 3

    # Test case 3: Test skip value greater than the length of books
    response = client.get("/api/v1/books?skip=15")
    assert response.status_code == 200
    assert len(response.json()) == 0

    # Test case 4: Test limit value greater than the remaining books after skipping
    response = client.get("/api/v1/books?skip=5&limit=10")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_get_book_valid_id():
    # Test case: Valid book_id
    response = client.get("/api/v1/books/4")
    assert response.status_code == 200
    assert Book(**response.json()) == books[4]


def test_get_book_invalid_id():
    # Test case: Invalid book_id (less than 0)
    response = client.get("/api/v1/books/-1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"

    # Test case: Invalid book_id (greater than or equal to len(books))
    response = client.get(f"/api/v1/books/{len(books)}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"


def test_create_book():
    # Test case 1: Creating a book with valid data
    book_data = Book(
        title="El señor de los anillos", author="J.R.R. Tolkien", publication_year=1954
    )
    response = client.post("/api/v1/books/", json=book_data.model_dump())
    assert response.status_code == 201
    assert Book(**response.json()) == book_data

    # Test case 2: Creating a book with missing data
    book_data = {
        "title": "Harry Potter and the Chamber of Secrets",
        "author": "J.K. Rowling",
    }
    response = client.post("/api/v1/books/", json=book_data)
    assert response.status_code == 422

    # Test case 3: Creating a book with invalid data
    book_data = {
        "title": "Harry Potter and the Prisoner of Azkaban",
        "author": "J.K. Rowling",
        "year": "1999",
    }
    response = client.post("/api/v1/books/", json=book_data)
    assert response.status_code == 422


def test_update_book():
    # Test case 1: Updating an existing book
    book_id = 0
    book_data = Book(
        title="El señor de los anillos", author="J.R.R. Tolkien", publication_year=1954
    )
    response = client.put(f"/api/v1/books/{book_id}", json=book_data.model_dump())
    assert response.status_code == 200
    assert response.json() == book_data.model_dump()

    # Test case 2: Updating a non-existing book
    book_id = 100
    book_data = Book(title="New Title", author="New Author", publication_year=2022)
    try:
        response = client.put(f"/api/v1/books/{book_id}", json=book_data.model_dump())
    except Exception as e:
        assert e.status_code == 404
        assert e.detail == "Book not found"

    # Test case 3: Updating a book with an invalid ID
    book_id = -1
    book_data = Book(title="New Title", author="New Author", publication_year=2022)
    try:
        response = client.put(f"/api/v1/books/{book_id}", json=book_data.model_dump())
    except Exception as e:
        assert e.status_code == 404
        assert e.detail == "Book not found"

    # Test case 4: Updating a book with invalid data
    book_id = 0
    book_data = Book(title="", author="New Author", publication_year=2022)
    try:
        response = client.put(f"/api/v1/books/{book_id}", json=book_data.model_dump())
    except Exception as e:
        assert response.status_code == 422
        assert response.json() == {
            "detail": [
                {
                    "loc": ["body", "title"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ]
        }


def test_update_book_internal_error():
    # Test case 5: Error 500
    book_id = 0
    book = Book(title="New Title", author="New Author", publication_year=2022)

    # Guardar la función original para poder restaurarla después de la prueba
    try:
        response = client.put(f"/api/v1/books/{book_id}", json=book.model_dump())
    except HTTPException as e:
        assert e.status_code == 500
        assert e.detail == "Simulated internal error"


def test_delete_existing_book():
    book_id = 1
    response = client.delete(f"/api/v1/books/{book_id}")
    assert response.status_code == 200


def test_delete_non_existing_book():
    book_id = 20
    response = client.delete(f"/api/v1/books/{book_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}


def test_delete_book_with_negative_id():
    book_id = -1
    response = client.delete(f"/api/v1/books/{book_id}")
    assert response.status_code == 404
