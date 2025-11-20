from fastapi import APIRouter


dashboard_route = APIRouter()


@dashboard_route.get("/dashboard")
async def get_dashboard():
    return {"message": "This is the dashboard endpoint."}
