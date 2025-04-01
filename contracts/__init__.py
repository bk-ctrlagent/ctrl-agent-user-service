from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    token: str
    token_type: str

class RegisterRequest(BaseModel):
    email: str
    password: str

class RegisterResponse(BaseModel):
    message: str

class ResetPasswordRequest(BaseModel):
    email: str
    new_password: str
    confirm_password: str

class ResetPasswordResponse(BaseModel):
    message: str
