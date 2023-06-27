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


class DeviceExtraDescription(BaseModel):
    model: str
    ui: str
    uiid: int
    description: str
    manufacturer: str
    mac: str
    apmac: str
    model_info: str = Field(alias="modelInfo")
    brand_id: str = Field(alias="brandId")
    chip_id: str = Field(alias="chipid")


class DeviceGroup(BaseModel):
    ...


class DeviceConfig(BaseModel):
    ...


class DeviceSettings(BaseModel):
    ...


class Family(BaseModel):
    ...


class Shared(BaseModel):
    ...


class Device(BaseModel):
    name: str
    deviceid: str
    apikey: str
    extra: DeviceExtraDescription
    brand_name: str = Field(alias="brandName")
    brand_logo: str = Field(alias="brandLogo")
    show_brand: bool = Field(alias="showBrand")
    product_model: str = Field(alias="productModel")
    groups: list[DeviceGroup] = Field(alias="devGroups")
    tags: dict[str, Any]
    config: DeviceConfig = Field(alias="devConfig")
    settings: DeviceSettings
    family: Family
    shared_by: Shared = Field(alias="sharedBy")
    shared_to: Shared = Field(alias="shareTo")
    devicekey: str
    online: bool
    params: dict[str, Any]
