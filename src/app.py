from fastapi import FastAPI
from application.config import uvicorn_config
from controllers.bootstrap import setup_routers, setup_handlers
import uvicorn


app = FastAPI()

setup_routers(app)
setup_handlers(app)


if __name__ == '__main__':
    uvicorn.run('app:app', **uvicorn_config)
