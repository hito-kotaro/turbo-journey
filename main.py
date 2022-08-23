from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import db.models as models
from db.database import engine
from routes import (
    auth_routes,
    user_routes,
    bank_routes,
    request_router,
    approve_router,
    line_routes,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(bank_routes.router)
app.include_router(request_router.router)
app.include_router(approve_router.router)
app.include_router(line_routes.router)


models.Base.metadata.create_all(bind=engine)


@app.get("/")
def index():
    return {"message": "ok"}
