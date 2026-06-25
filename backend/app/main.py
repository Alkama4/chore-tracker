import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager

from app import config
from app.database import AsyncSessionLocal
from app.routers import auth, settings, user_settings, root, config
from app.settings.seed import init_settings

# Setup ENVs
config
PROXY_ROOT_PATH = os.getenv("PROXY_ROOT_PATH", "")

# Setup DB stuff
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with AsyncSessionLocal() as db:
        await init_settings(db)
    yield

app = FastAPI(
    root_path=PROXY_ROOT_PATH,
    lifespan=lifespan
)

origins=["http://localhost:5173"]

origin_regex = r"https?://192\.168\.0\.\d+(:\d+)?"

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=origin_regex,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True, # lets the browser send cookies / auth headers
)

app.include_router(root.router, prefix="", tags=["Root"])
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(settings.router, prefix="/settings", tags=["Settings"])
app.include_router(user_settings.router, prefix="/user_settings", tags=["User Settings"])

@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    redirect_url = f"{PROXY_ROOT_PATH}/docs" if PROXY_ROOT_PATH else "/docs"
    return RedirectResponse(url=redirect_url)
