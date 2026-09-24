from datetime import datetime
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.database import Base, engine
from app.routers import profiles, projects, technologies


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DevShowcase API",
    description="API com regras avançadas de domínio, persistência em nuvem e métricas.",
    version="2.0.0"
)


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "status_code": exc.status_code,
            "message": exc.detail,
            "timestamp": datetime.utcnow().isoformat()
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        field = " -> ".join([str(loc) for loc in err["loc"]])
        errors.append({"field": field, "issue": err["msg"]})

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "success": False,
            "status_code": 400,
            "message": "Erro de validação nos dados enviados.",
            "errors": errors,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

app.include_router(profiles.router)
app.include_router(projects.router)
app.include_router(technologies.router)


@app.get("/")
def root():
    return {"message": "DevShowcase API v2 está ativa."}