from fastapi import APIRouter, HTTPException, Depends, Path
from sqlalchemy.orm import Session
from typing import List, Annotated

from library.infrastructure.database.engine import get_session
from library.presentation.models.members import MemberCreate, MemberUpdate
from library.infrastructure.repositories.memberRepository import MemberRepository
from library.application.member_service import MemberService

app = APIRouter()

# Dependency to get a session
def get_db():
    session = get_session()
    try:
        yield session
    finally:
        session.close()


member_repo = MemberRepository()
member_service = MemberService(member_repo)

@app.post("/members/", response_model=MemberCreate)
def create_member(member: MemberCreate, db: Session = Depends(get_db)):
    return member_service.add_member(member, session=db)

@app.get("/members/", response_model=List[MemberCreate])
def get_members(db: Session = Depends(get_db)):
    return member_service.list_members(session=db)

@app.get("/members/{member_id}", response_model=MemberCreate)
def get_member(member_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    return member_service.get_member(member_id, session=db)

@app.put("/members/{member_id}", response_model=MemberUpdate)
def update_member(member: MemberUpdate, member_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    return member_service.update_member(member_id, member, session=db)

@app.delete("/members/{member_id}")
def delete_member(member_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    return member_service.delete_member(member_id, session=db)
