from fastapi import FastAPI
from routers import department
import uvicorn

app = FastAPI()
app.include_router(department.router)

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)    