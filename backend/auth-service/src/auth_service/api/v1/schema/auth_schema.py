from pydantic import BaseModel


class LoginSchema(BaseModel):
    email: str
    password: str


class SignupSchema(BaseModel):
    first_name: str
    last_name: str
    user_name: str
    email: str
    password: str
