from fastapi import FastAPI

from app.routers.departments import router as department_router
from app.routers.divisions import router as division_router
from app.routers.employees import router as employee_router
from app.routers.structures import router as structure_router

app = FastAPI(root_path="/org")

app.include_router(structure_router, prefix="/teams", tags=["teams"])
app.include_router(division_router, prefix="/teams", tags=["divisions"])
app.include_router(department_router, prefix="/teams", tags=["departments"])
app.include_router(employee_router, prefix="/departments", tags=["employees"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
