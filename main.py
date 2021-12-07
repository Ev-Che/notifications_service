from fastapi import FastAPI

from app.routes import router
from core.base import Base
from core.database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router=router)
