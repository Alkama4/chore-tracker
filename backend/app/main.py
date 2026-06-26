import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app import config
from app.routers import root

_ = config  # Load ENVs
proxy_root_path = os.getenv("PROXY_ROOT_PATH", "")

app = FastAPI(root_path=proxy_root_path)

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

@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    redirect_url = f"{proxy_root_path}/docs" if proxy_root_path else "/docs"
    return RedirectResponse(url=redirect_url)
