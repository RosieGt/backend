from fastapi import FastAPI
from app.database import Base, engine
from app.routers import profiles, projects, technologies


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DevShowcase API",
    description="API para portfólio de perfis e projetos de desenvolvedores.",
    version="1.0.0"
)


app.include_router(profiles.router)
app.include_router(projects.router)
app.include_router(technologies.router)


@app.get("/")
def root():
    return {"message": "DevShowcase API está online. Acesse /docs para testar os endpoints."}