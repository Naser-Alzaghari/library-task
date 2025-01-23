from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, NoResultFound
from fastapi import HTTPException
from library.infrastructure.repositories.bookRepository import BookRepository
from library.presentation.models.books import BookCreate, BookUpdate
from sqlalchemy import select, update, func
from library.infrastructure.database.schemas import book_table, member_table


class BookService:
    def __init__(self, book_repo: BookRepository):
        self.book_repo = book_repo

    def add_book(self, book_data: BookCreate, session: Session):
        try:
            return self.book_repo.add(book_data.title, book_data.author, session)
        except IntegrityError as e:
            if "duplicate key" in str(e.orig):
                raise HTTPException(status_code=400, detail="Duplicate entry detected.")
            raise HTTPException(status_code=500, detail="An unexpected error occurred.")

    def get_book(self, book_id: int, session: Session):
        try:
            book = self.book_repo.get(book_id, session)
            if not book:
                raise HTTPException(status_code=404, detail="Book not found")
            return book
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Book not found")

    def list_books(self, session: Session):
        return self.book_repo.list(session)

    def delete_book(self, book_id: int, session: Session):
        try:
            result = self.book_repo.delete(book_id, session)
            if not result:
                raise HTTPException(status_code=404, detail="Book not found")
            return {"detail": "Book deleted successfully"}
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Book not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def update_book(self, book_id: int, book_data: BookUpdate, session: Session):
        try:
            updated_book = self.book_repo.update(book_id, session, book_data.title, book_data.author)
            if not updated_book:
                raise HTTPException(status_code=404, detail="Book not found")
            return updated_book
        except IntegrityError as e:
            if "duplicate key" in str(e.orig):
                raise HTTPException(status_code=400, detail="Duplicate entry detected.")
            raise HTTPException(status_code=500, detail="An unexpected error occurred.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def borrow_book(self, book_id: int, member_id: int, session: Session):
        try:
            # Check if the book exists and is not borrowed
            stmt = select(book_table).where(book_table.c.book_id == book_id)
            book = session.execute(stmt).mappings().fetchone()  # Use mappings() for dict-like access
            if not book:
                raise HTTPException(status_code=404, detail=f"Book with ID {book_id} does not exist.")
            if book["is_borrowed"]:
                raise HTTPException(status_code=400, detail=f"Book with ID {book_id} is already borrowed.")
            
            # Check if the member exists
            stmt = select(member_table).where(member_table.c.member_id == member_id)
            member = session.execute(stmt).mappings().fetchone()
            if not member:
                raise HTTPException(status_code=404, detail=f"Member with ID {member_id} does not exist.")
            
            # Update book to borrowed state
            stmt = update(book_table).where(book_table.c.book_id == book_id).values(
                is_borrowed=True,
                borrowed_date=func.now(),
                borrowed_by=member_id,
            )
            session.execute(stmt)
            session.commit()
            return {"detail": "Book borrowed successfully"}
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def return_book(self, book_id: int, session: Session):
        try:
            # Check if the book exists and is borrowed
            stmt = select(book_table).where(book_table.c.book_id == book_id)
            book = session.execute(stmt).mappings().fetchone()  # Use mappings() for dict-like access
            if not book:
                raise HTTPException(status_code=404, detail=f"Book with ID {book_id} does not exist.")
            if not book["is_borrowed"]:
                raise HTTPException(status_code=400, detail=f"Book with ID {book_id} is not currently borrowed.")

            # Update book to available state
            stmt = update(book_table).where(book_table.c.book_id == book_id).values(
                is_borrowed=False,
                borrowed_date=None,
                borrowed_by=None,
            )
            session.execute(stmt)
            session.commit()
            return {"detail": "Book returned successfully"}
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=str(e))
