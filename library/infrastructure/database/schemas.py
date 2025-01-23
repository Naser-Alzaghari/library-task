from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime, Boolean, UniqueConstraint
from sqlalchemy import MetaData


metadata = MetaData()


member_table = Table(
    'members',
    metadata,
    Column("member_id", Integer, primary_key=True),  
    Column("name", String, nullable=False),         
    Column("email", String, nullable=False, unique=True),        
    UniqueConstraint('email') 
)


book_table = Table(
    'books',
    metadata,
    Column("book_id", Integer, primary_key=True),         
    Column("title", String, nullable=False),             
    Column("author", String, nullable=False),            
    Column("is_borrowed", Boolean, default=False, nullable=False),  
    Column("borrowed_date", DateTime, default=None, nullable=True),  
    Column("borrowed_by", Integer, ForeignKey("members.member_id"), nullable=True),  
)
