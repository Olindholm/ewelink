from pydantic import BaseModel, Field
from typing import Literal

Region = Literal["as", "cn", "eu", "us"]
DOMAINS: dict[Region, str] = {
    "as": "https://as-apia.coolkit.cc",
    "cn": "https://cn-apia.coolkit.cn",
    "eu": "https://eu-apia.coolkit.cc",
    "us": "https://us-apia.coolkit.cc",
}


class AppCredentials(BaseModel):
    id: str
    secret: str


class EmailUserCredentials(BaseModel):
    email: str
    password: str
    country_code: str = Field(alias="countryCode")


class LoginResponse(BaseModel):
    user: object
    access_token: str = Field(alias="countryCode")
    refresh_token: str = Field(alias="countryCode")
    region: Region
