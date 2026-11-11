from pydantic import BaseModel, EmailStr, Field
from uuid import UUID


class User(BaseModel):
    id: UUID | None = Field(default=None, title='The ID of user')
    username: str = Field(..., title='The username of user')
    email: EmailStr = Field(..., title='The email of user')
    is_active: bool = Field(default=True, title='The active status of user')
    
    model_config = {
        'json_schema_extra':{
            'username':'john_doe',
            'email':'johndoe@gmail.com', 
            'is_active': True, 
        }
    }
    
    
class UserInDB(User):
    hashed_password: str = Field(..., title='The hashed password of user')
    
    
class Token(BaseModel):
    access_token: str
    token_type: str
    

class TokenData(BaseModel):
    username: str | None = None
