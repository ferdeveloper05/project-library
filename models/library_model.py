from pydantic import BaseModel, Field, Enum
from uuid import UUID


class CategoryBook(str, Enum):
    FICTION = "Fiction"
    NON_FICTION = "Non-Fiction"
    MYSTERY = "Mystery"
    ROMANCE = "Romance"
    SCIENCE_FICTION = "Science Fiction"


class Book(BaseModel):
    id: UUID | None = Field(default=None, title='The ID of book')
    title: str = Field(..., title='The title of book', min_length=5)
    author: str = Field(title='Enter the author', min_length=5, max_length=15)
    category: list[CategoryBook] = Field(..., title='The category of book')
    year: int = Field(gt=1700, lt=2026)
    reading: bool = Field(default=False, title='The reading status of book')
    score: int = Field(ge=1, le=5, title='The score of book')
    
    model_config = {
        'json_schema_extra':{
            'title':'Percy Jackson y el mar de los monstruos',
            'author':'Rick Riordian',
            'category': [
                'aventura'
            ],
            'year':2001, 
            'reading': True, 
            'score': 5
        }
    }
    
    
class UpdateBook(BaseModel):
    title: str = Field(..., title='The title of book', min_length=5)
    author: str = Field(..., title='Enter the author', min_length=5, max_length=15)
    category: list[CategoryBook] = Field(..., title='The category of book')
    year: int = Field(..., gt=1700, lt=2026)
    reading: bool = Field(default=False, title='The reading status of book')
    score: int = Field(..., ge=1, le=5, title='The score of book')