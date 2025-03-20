import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from exceptions import register_error_handlers
from routers.downtimes import router as downtimes_router


app = FastAPI(title='downtime service',
              version='0.1.0',
              debug=settings.ENVIRONMENT != 'production'
              )

app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],
                   allow_methods=['GET', 'POST', 'DELETE', 'PATCH'],
                   allow_credentials=True,
                   allow_headers=['*']
                   )


@app.get("/", tags=["root"])
async def get_root():
    return JSONResponse(status_code=200, content="It's Alive!")

app.include_router(downtimes_router)

register_error_handlers(app)
