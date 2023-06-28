from pydantic import BaseModel, Field
from typing import Any, Literal, Optional

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
    country_code: str = Field("+1", alias="countryCode")


class LoginResponse(BaseModel):
    user: object
    access_token: str = Field(alias="at")
    refresh_token: str = Field(alias="rt")
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
    groups: Optional[list[DeviceGroup]] = Field(alias="devGroups")
    tags: Optional[dict[str, Any]]
    config: Optional[DeviceConfig] = Field(alias="devConfig")
    settings: Optional[DeviceSettings]
    family: Family
    shared_by: Optional[Shared] = Field(alias="sharedBy")
    shared_to: Optional[list[Shared]] = Field(alias="shareTo")
    devicekey: str
    online: bool
    params: Optional[dict[str, Any]]
