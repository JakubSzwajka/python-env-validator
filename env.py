import os
from pydantic import BaseModel, validator, AnyUrl


class Env(BaseModel):
    TIME_ZONE: str
    DATABASE_URL: AnyUrl
    DEBUG: bool

    @validator("TIME_ZONE")
    def validate_time_zone(cls, value):
        # Replace this list with the time zones you want to support
        valid_time_zones = ["UTC", "America/New_York", "Europe/London"]
        if value not in valid_time_zones:
            raise ValueError(
                f"Invalid time zone '{value}', allowed values: {', '.join(valid_time_zones)}"
            )
        return value

    @validator("DATABASE_URL")
    def validate_database_url(cls, value):
        if not value.startswith("postgres://"):
            raise ValueError("Only PostgreSQL database URLs are supported")
        return value

    @validator("DEBUG")
    def validate_debug(cls, value):
        if not isinstance(value, bool):
            raise ValueError("DEBUG must be a boolean value")
        return value


def load_env_vars():
    env_vars = {
        "TIME_ZONE": os.environ.get("TIME_ZONE"),
        "DATABASE_URL": os.environ.get("DATABASE_URL"),
        "DEBUG": os.environ.get("DEBUG").lower() == "true"
        if os.environ.get("DEBUG")
        else False,
    }
    return Env(**env_vars)


env = load_env_vars()
