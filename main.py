from fastapi import FastAPI
import uvicorn
import logging
import src.api as api_router

logging.basicConfig(level=logging.INFO)


def get_app():
    app = FastAPI()
    app.include_router(api_router.get_api())
    return app


if __name__ == "__main__":
    uvicorn.run("main:get_app", reload=True)
