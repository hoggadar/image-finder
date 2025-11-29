from dataclasses import dataclass


@dataclass
class LoginDTO:
    email: str
    password: str


@dataclass
class SignupDTO:
    first_name: str
    last_name: str
    username: str
    email: str
    password: str