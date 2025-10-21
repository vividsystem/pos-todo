from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, Literal


class UsbSettings(BaseSettings):
    vendor_id: str
    product_id: str


class NetworkSettings(BaseSettings):
    host: str


class MqttSettings(BaseSettings):
    host: str
    port: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="PRINTER__",
        env_file="../.env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )
    mqtt: MqttSettings
    profile: Optional[str] = None
    connection: Literal["USB", "NETWORK"] = Field("USB")
    network: Optional[NetworkSettings] = None
    usb: Optional[UsbSettings] = None

    @model_validator(mode="after")
    def check_connections(cls, values):
        if values.connection == "USB" and values.usb:
            return values
        if values.connection == "NETWORK" and values.network:
            return values
        raise ValueError("you have to specify your connection type")
