from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import image_gen
from middleware import ResponseTimeMiddleware

app = FastAPI(
    title="Image Gen API",
    description="API for generating images using Gemini",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(ResponseTimeMiddleware)

app.include_router(image_gen.router)

@app.get("/")
async def info():
    return {
        "message": "Image Gen API",
        "version": "1.0.0",
        "endpoint": {
            "upload": "POST /images-gen",
            "docs": "/docs"
        }
    }