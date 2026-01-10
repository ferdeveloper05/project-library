from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional, List


class CategoryBook(BaseModel):
    name: str = Field(title='Enter the category book', min_length=5)

class CreateBook(BaseModel):
    id: Optional[UUID] = None
    title: str = Field(title='The title of book', min_length=5)
    author: str = Field(title='Enter the author', min_length=5, max_length=15)
    #category: List[CategoryBook]
    year: int = Field(gt=1700, lt=2026)
    
    model_config = {
        'json_schema_extra':{
            'title':'Percy Jackson y el mar de los monstruos',
            'author':'Rick Riordian',
            'category':'Aventure',
            'year':2001
        }
    }