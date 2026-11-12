from fastapi import FastAPI

from endpoints import authentication

app = FastAPI()
app.include_router(authentication.router)

@app.get("/", tags=['Home'])
async def say_hello():
    return {'Hello':'World'}