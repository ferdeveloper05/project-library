from fastapi import FastAPI, Query, Path
from typing import Annotated
from models import CreateBook
from uuid import UUID, uuid4
from local_functions import save_book, read_book, delete_book

app = FastAPI(
    version='1.0.0',
    title='Personal Library Project'
)

books = []

@app.get("/", tags=['Home'])
async def say_hello():
    return {'Hello':'World'}


@app.post('/create-book', tags=['Library'])
async def create_book(book: Annotated[CreateBook, Query()]):
    book.id = str(uuid4())
    save_book(book.model_dump(mode='json'))
    #save_book(books)
    
    read = read_book()
    return read


@app.get('/list_books', tags=['Library'])
async def list_books() -> list:
    read = read_book()
    return read

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
    for book in read_book():
        if book['id'] == book_id:
            delete_book(book)
    print(read_book())
    #return read_book()