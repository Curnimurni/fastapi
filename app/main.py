
from fastapi import FastAPI
from pydantic import BaseModel
from . import models
from .database import engine
from .routers import post, user, auth, vote
from pydantic import BaseSettings
from .config import settings
from fastapi.middleware.cors import CORSMiddleware


#class Settings(BaseSettings):
#    database_hostname: str
#    database_port: str
#    database_password: str
#    database_name: str
#    database_username: str
#    secret_key: str
#    algorithm: str
#    access_token_expire_minutes: int
     

#settings = Settings()    

print(settings.database_username)

#models.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)






class Post(BaseModel):
    title:str
    content:str
    published: bool = True









app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)



@app.get("/")
def root():
    return {"message": "welcome to my API"}




