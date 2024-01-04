from fastapi.testclient import TestClient
from main import Book, app, books


client = TestClient(app)


def test_get_books():
    # Test case 1: Test the default values of skip and limit
    response = client.get("/books")
    assert response.status_code == 200
    assert len(response.json()) == 5

    # Test case 2: Test the skip and limit values
    response = client.get("/books?skip=1&limit=3")
    assert response.status_code == 200
    assert len(response.json()) == 3

    # Test case 3: Test skip value greater than the length of books
    response = client.get("/books?skip=15")
    assert response.status_code == 200
    assert len(response.json()) == 0

    # Test case 4: Test limit value greater than the remaining books after skipping
    response = client.get("/books?skip=5&limit=10")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_get_book_valid_id():
    # Test case: Valid book_id
    response = client.get("/books/4")
    assert response.status_code == 200
    assert Book(**response.json()) == books[4]


def test_get_book_invalid_id():
    # Test case: Invalid book_id (less than 0)
    response = client.get("/books/-1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"

    # Test case: Invalid book_id (greater than or equal to len(books))
    response = client.get(f"/books/{len(books)}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"
