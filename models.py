from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional, List
from enum import Enum

class CategoryBook(Enum):
    historia = 'historia'
    aventura = 'aventura'
    fantasia = 'fantasia'
    distopia = 'distopia'
    otro = 'otro'

class CreateBook(BaseModel):
    id: Optional[UUID] = None
    title: str = Field(title='The title of book', min_length=5)
    author: str = Field(title='Enter the author', min_length=5, max_length=15)
    category: List[CategoryBook]
    year: int = Field(gt=1700, lt=2026)
    reading: bool = False
    score: int = Field(ge=1, le=5)
    
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
    title: str = Field(title='The title of book', min_length=5)
    author: str = Field(title='Enter the author', min_length=5, max_length=15)
    category: List[CategoryBook]
    year: int = Field(gt=1700, lt=2026)
    reading: bool = False
    score: int = Field(ge=1, le=5)