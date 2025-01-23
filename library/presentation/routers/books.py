from fastapi import APIRouter, HTTPException, Depends, Path
from sqlalchemy.orm import Session
from typing import List, Annotated

from library.infrastructure.database.engine import get_session
from library.presentation.models.books import BookCreate, BookUpdate
from library.infrastructure.repositories.bookRepository import BookRepository
from library.application.book_service import BookService

app = APIRouter()

# Dependency to get a session
def get_db():
    session = get_session()
    try:
        yield session
    finally:
        session.close()


book_repo = BookRepository()
book_service = BookService(book_repo)

@app.post("/books/", response_model=BookCreate)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    return book_service.add_book(book, session=db)

@app.get("/books/", response_model=List[BookCreate])
def get_books(db: Session = Depends(get_db)):
    return book_service.list_books(session=db)

@app.get("/books/{book_id}", response_model=BookCreate)
def get_book(book_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    return book_service.get_book(book_id, session=db)

@app.put("/books/{book_id}", response_model=BookUpdate)
def update_book(book: BookUpdate, book_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    return book_service.update_book(book_id, book, session=db)

@app.delete("/books/{book_id}")
def delete_book(book_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    return book_service.delete_book(book_id, session=db)

@app.post("/borrow/{book_id}/{member_id}")
def borrow_book(book_id: int = Path(..., ge=1), member_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    return book_service.borrow_book(book_id, member_id, session=db)

@app.post("/return/{book_id}")
def return_book(book_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    return book_service.return_book(book_id, session=db)
