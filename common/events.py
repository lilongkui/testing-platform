from typing import Callable
from fastapi import FastAPI
from aioredis import Redis

from db.redis import redis


def startup(app: FastAPI) -> Callable:
    """
    FastApi 启动完成事件
    :param app: FastAPI
    :return: start_app
    """

    async def app_start() -> None:
        # APP启动完成后触发
        print("fast-api已启动")
        # 注入缓存到app state
        app.state.cache = await redis()

    return app_start


def stopping(app: FastAPI) -> Callable:
    """
    FastApi 停止事件
    :param app: FastAPI
    :return: stop_app
    """

    async def stop_app() -> None:
        print("fast-api已停止")
        cache: Redis = await app.state.cache
        await cache.close()

    return stop_app
