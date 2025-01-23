from fastapi import FastAPI
from library.presentation.routers import books, members

app = FastAPI()

# Include the routers
app.include_router(members.app, prefix='/api', tags=["Members"])
app.include_router(books.app, prefix='/api', tags=["Books"])