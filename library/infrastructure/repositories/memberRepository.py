from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import Session
from library.infrastructure.database.schemas import member_table

class MemberRepository:
    def add(self, name, email, session: Session):
        member = {
            "name": name,
            "email": email
        }
        stmt = insert(member_table).values(member).returning(member_table)
        result = session.execute(stmt).first()
        session.commit()
        return result

    def get(self, member_id, session: Session):
        stmt = select(member_table).where(member_table.c.member_id == member_id)
        result = session.execute(stmt).fetchone()
        return result

    def list(self, session: Session):
        stmt = select(member_table)
        result = session.execute(stmt).fetchall()
        return result

    def delete(self, member_id: int, session: Session):
        stmt = select(member_table).where(member_table.c.member_id == member_id)
        result = session.execute(stmt).scalar()
        if not result:
            return False

        stmt = delete(member_table).where(member_table.c.member_id == member_id)
        session.execute(stmt)
        session.commit()
        return True


    def update(self, member_id, session: Session, name=None, email=None):
        updated_member = {}
        if name is not None:
            updated_member["name"] = name
        if email is not None:
            updated_member["email"] = email
        
        stmt = update(member_table).where(member_table.c.member_id == member_id).values(updated_member).returning(member_table)
        result = session.execute(stmt).first()
        session.commit()
        return result