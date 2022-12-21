from fastapi import FastAPI
from . import models
from .database import engine
from .routes import bottle, user, auth, diaper
from .config import settings

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# removed when switching to alembic
# models.Base.metadata.create_all(bind=engine)

app.include_router(bottle.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(diaper.router)


@app.get("/")
def root():
    return {"message": "WHAT THE FUCK! IM TRAPPED IN A WEB BROWSER!"}
