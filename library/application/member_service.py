from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, NoResultFound
from library.infrastructure.repositories.memberRepository import MemberRepository
from library.presentation.models.members import MemberCreate, MemberUpdate
from fastapi import HTTPException

class MemberService:
    def __init__(self, member_repo: MemberRepository):
        self.member_repo = member_repo

    def add_member(self, member_data: MemberCreate, session: Session):
        try:
            return self.member_repo.add(member_data.name, member_data.email, session)
        except IntegrityError as e:
            if "duplicate key" in str(e.orig):
                raise HTTPException(status_code=400, detail="Email address already exists.")
            raise HTTPException(status_code=500, detail="An unexpected error occurred.")

    def get_member(self, member_id: int, session: Session):
        try:
            member = self.member_repo.get(member_id, session)
            if not member:
                raise HTTPException(status_code=404, detail="Member not found")
            return member
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Member not found")

    def list_members(self, session: Session):
        return self.member_repo.list(session)

    def delete_member(self, member_id: int, session: Session):
        try:
            result = self.member_repo.delete(member_id, session)
            if not result:
                raise HTTPException(status_code=404, detail="Member not found")
            return {"detail": "Member deleted successfully"}
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Member not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def update_member(self, member_id: int, member_data: MemberUpdate, session: Session):
        try:
            updated_member = self.member_repo.update(member_id, session, member_data.name, member_data.email)
            if not updated_member:
                raise HTTPException(status_code=404, detail="Member not found")
            return updated_member
        except IntegrityError as e:
            if "duplicate key" in str(e.orig):
                raise HTTPException(status_code=400, detail="Email address already exists.")
            raise HTTPException(status_code=500, detail="An unexpected error occurred.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))