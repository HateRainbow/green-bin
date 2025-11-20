from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.dashboard import dashboard_route
from routes.picture import picture_route


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def index():
    return {"message": "Hello, World!"}


routes = [picture_route, dashboard_route]

for route in routes:
    app.include_router(prefix="/api", router=route)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app=app, port=8080)
