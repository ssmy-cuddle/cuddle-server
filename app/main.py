import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from db.session import engine
from models import Base
from routes import auth_routes, user_routes, pet_routes

def create_app():
    Base.metadata.create_all(bind=engine)

    app = FastAPI()

    origins = [
        "*"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
    app.include_router(user_routes.router, prefix="/users", tags=["Users"])
    app.include_router(pet_routes.router, prefix="/pets", tags=["Pets"])

    @app.get("/")
    def read_root():
        return {"message": "API is up and running!"}
    
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)