from os import getenv

from fastapi import FastAPI
from fastapi.logger import logger
from fastapi.middleware.cors import CORSMiddleware


##################################################
# FastAPI
##################################################
tags_metadata = [{"name": "healthcheck", "description": "HealthCheck API"}]
application = FastAPI(
    title="Service",
    version="0.0.1",
    openapi_tags=tags_metadata,
    root_path=getenv("FASTAPI_ROOT_PATH", None),
)

application.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

##################################################
# Error handling
##################################################
from app.errors import *
from app.middlewares import *


##################################################
# Routers
##################################################
from app.routers import healthcheck, chat

router_infos = [
    (healthcheck.router, "healthcheck"),
    (chat.router, "chat"),
]
for router_info in router_infos:
    r = router_info[0]
    t = [router_info[1]]
    p = f"/{router_info[1]}"
    logger.info(f'Register router for prefix "{p}"')
    application.include_router(router=r, prefix=p)
