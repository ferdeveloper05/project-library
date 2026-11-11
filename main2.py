from fastapi import FastAPI
from endpoints import auth

app = FastAPI()
app.include_router(auth.router, prefix='/api/v1')

@app.get("/", tags=['Home'])
async def say_hello():
    return {'Hello':'World'}