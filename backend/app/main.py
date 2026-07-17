from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings

from .database import init_db
from .routes.category import category_router
from .routes.product import product_router

app = FastAPI(
    debug=settings.debug,
    title=settings.app_name,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.add_middleware(
    CORSMiddleware, allow_credentials=True, allow_origins=settings.cors_origins
)

app.include_router(product_router)
app.include_router(category_router)


@app.on_event("startup")
async def startup():
    await init_db()


@app.get("/")
def root():
    return {"message": "Hello, World!"}


@app.get("/health")
def health():
    return {"status": "ok"}
