from fastapi import FastAPI, Query, Path
from typing import Annotated
from models import CreateBook
from uuid import UUID, uuid4

app = FastAPI(
    version='1.0.0',
    title='Library Project'
)

books = []

@app.get("/", tags=['Home'])
async def say_hello():
    return {'Hello':'World'}


@app.post('/create-book', tags=['Library'])
async def create_book(book: Annotated[CreateBook, Query()]):
    book.id = uuid4()
    books.append(book)
    return books


@app.get('/list_books', tags=['Library'])
async def list_books() -> list:
    #print(books)
    return books

@app.get('/view-book/{book_id}/', response_model=CreateBook, tags=['Library'])
async def view_book(book_id: Annotated[UUID, Path(title='The ID of Book')]) -> dict:
    for book in books: 
        if book.id == book_id:
            return book
    else:
        return {}
    
@app.put('/update-book/{book_id}/', tags=['Library'])
async def update_book(book_id: Annotated[UUID, Path()], book_update: Annotated[CreateBook, Query()]):
    for b in books:
        if b.id == book_id:
            b.title = book_update.title
            b.author = book_update.author
            b.year = book_update.year
    return b 

@app.delete('/delete-book/{book_id}/', tags=['Library'])
async def delete_book(book_id: Annotated[UUID, Path(title='The ID of book')]):
    for book in books:
        if book.id == book_id:
            books.remove(book)
    return books