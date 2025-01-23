from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import Session
from library.infrastructure.database.schemas import book_table

class BookRepository:
    def add(self, title, author, session: Session):
        book = {
            "title": title,
            "author": author,
            "is_borrowed": False,
            "borrowed_date": None,
            "borrowed_by": None
        }
        stmt = insert(book_table).values(book).returning(book_table)
        result = session.execute(stmt).fetchone()
        session.commit()
        return result

    def get(self, book_id, session: Session):
        stmt = select(book_table).where(book_table.c.book_id == book_id)
        result = session.execute(stmt).fetchone()
        return result

    def list(self, session: Session):
        stmt = select(book_table)
        result = session.execute(stmt).fetchall()
        return result

    def delete(self, book_id, session: Session):
        stmt = delete(book_table).where(book_table.c.book_id == book_id)
        result = session.execute(stmt)
        session.commit()
        return result.rowcount > 0

    def update(self, book_id, session: Session, title=None, author=None):
        updated_book = {
            "title": title,
            "author": author,
        }
        
        # Remove None values to avoid updating with None
        updated_book = {k: v for k, v in updated_book.items() if v is not None}

        stmt = update(book_table).where(book_table.c.book_id == book_id).values(updated_book).returning(book_table)
        result = session.execute(stmt).fetchone()
        session.commit()
        return result
