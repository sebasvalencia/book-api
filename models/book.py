from pydantic import BaseModel


class Book(BaseModel):
    title: str
    author: str
    publication_year: int
