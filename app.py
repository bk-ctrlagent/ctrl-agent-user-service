from fastapi import FastAPI
from consul import Consul
import uvicorn
from pydantic import BaseModel
from controllers import user

class UserRequest(BaseModel):
    name: str
    email: str
    password: str

app = FastAPI()

app.include_router(user.router, prefix="/user")

def register():
    consul = Consul(host='consul', port=8500)
    consul.agent.service.register(
        name="user-service",
        service_id="user-service-1",
        address="user_service",
        port=8000,
        tags=["user-service"],
    )


if __name__ == "__main__":
    register()
    uvicorn.run(app, host="0.0.0.0", port=8000)