from fastapi import FastAPI                                 # , Body, Response, status, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from . import models                                       # , schemas, utils
from .database import engine                                # , Base, get_db
from .routers import post, user, auth, vote
from .config import Settings


app = FastAPI()

# Creates the tables not needed if using alembic
# models.Base.metadata.create_all(bind=engine)


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




"""
_______________________________________________________________________________________________________
                                                Routes                              
_______________________________________________________________________________________________________
"""





app.include_router(post.router)
app.include_router(user.router) 
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return {"message": "main page"}





