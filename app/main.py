from fastapi import FastAPI
from app.database import engine
from app import models
from app.auth import router as auth_router
from app.contacts import router as contacts_router
app = FastAPI(title="Multi-Tenant CRM API")

# create tables
models.Base.metadata.create_all(bind=engine)

# register auth routes
app.include_router(auth_router, prefix="/auth", tags=["Auth"])


app.include_router(contacts_router, prefix="/contacts", tags=["Contacts"])
