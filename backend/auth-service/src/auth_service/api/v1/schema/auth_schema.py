from pydantic import BaseModel


class LoginSchema(BaseModel):
    email: str
    password: str


class SignupSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str
