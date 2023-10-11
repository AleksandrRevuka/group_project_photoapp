import logging

import click
import redis.asyncio as redis_async
import uvicorn
from fastapi import Depends, FastAPI, HTTPException

from fastapi_limiter import FastAPILimiter
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.conf.config import init_async_redis
from src.database.db import get_db
from src.routes import auth, users

logger = logging.getLogger("uvicorn")

app = FastAPI()

app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")


@app.on_event("startup")
async def startup() -> FastAPILimiter:
    """
    The startup function is called when the server starts up.
    It's a good place to initialize things that are needed by your application,
    such as databases and caches.  It can also be used to pre-load data into memory,
    or do other tasks that need to happen before the server begins serving requests.

    :return: A fastapilimiter object
    """
    try:
        r = await init_async_redis()
        await FastAPILimiter.init(r)
    except redis_async.ConnectionError as e:
        click.secho(f"ERROR redis: {e}", bold=True, fg="red", italic=True)
        raise HTTPException(status_code=500, detail="Error connecting to the redis")


@app.on_event("startup")
async def on_startup() -> None:
    """
    The on_startup function is called when the application starts.
    It prints a message to the console, so that you know where to go in your browser.

    :return: None
    """
    message = "Open http://127.0.0.1:8000/docs to start api 🚀 🌘 🪐"
    color_url = click.style("http://127.0.0.1:8000/docs", bold=True, fg="green", italic=True)
    color_message = f"Open {color_url} to start api 🚀 🌘 🪐"
    logger.info(message, extra={"color_message": color_message})


@app.get("/api/healthchecker", tags=["healthchecker"])
async def healthchecker(db: AsyncSession = Depends(get_db)) -> dict:
    """
    The healthchecker function is a simple function that checks the database connection.
    It returns a JSON response with the message "Welcome to FastAPI!" if everything is working correctly.

    :param db: Session: Pass the database connection to the function
    :return: A dictionary with a message
    """
    try:
        result = await db.execute(text("SELECT 1"))
        fetched_result = result.fetchone()
        if fetched_result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
