from fastapi import FastAPI, Query, Path, HTTPException
from typing import Annotated
from models import CreateBook
from uuid import UUID, uuid4
from local_functions import read_book, save_book, delete_book_new, edit_book

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
    return read_book()


@app.get('/list_books', tags=['Library'])
async def list_books() -> list:
    return read_book()

@app.get('/view-book/{book_id}/', response_model=CreateBook, tags=['Library'])
async def view_book(book_id: UUID) -> dict:
    list_books = await read_book()
    for book in list_books: 
        if book['id'] == str(book_id):
            return book

    
@app.put('/update-book/{book_id}/', tags=['Library'])
async def update_book(book_id: Annotated[UUID, Path()], book_update: Annotated[CreateBook, Query()]):
    book_id_str = str(book_id)
    list_books = read_book()
    
    book_exists = any(str(book.get('id')) == book_id_str for book in list_books)
    
    if book_exists:
        for book in list_books:
            book.update({
                'title': book_update.title,
                'author': book_update.author,
                'category': book_update.category,
                'year':book_update.year,
                'reading':book_update.reading,
                'score':book_update.score
            })
            
        u_book = edit_book(book_id_str, book)
    
    return {'messages':f'Book with ID {u_book} update successfully'}
        
    """for b in books:
        if b.id == book_id:
            b.title = book_update.title
            b.author = book_update.author
            b.year = book_update.year
    return b """

@app.delete('/delete-book/{book_id}/', tags=['Library'])
async def delete_book(book_id: Annotated[UUID, Path(title='The ID of book')]):
    book_id_str = str(book_id)
    
    list_books = read_book()
    book_exists = any(str(book.get('id')) == book_id_str for book in list_books)
    
    if not book_exists:
        raise HTTPException(status_code=404, detail=f'Book with ID {book_id} not found')
    
    deleted_id = await delete_book_new(book_id_str)
    
    if deleted_id:
        return {
            'message':f'Book with ID {book_id} deleted successfully'
        }
    else:
        raise HTTPException(status_code=500, detail='Failed to delete book')