import os
from pydantic import BaseModel, HttpUrl, validator, EmailStr, AnyUrl


class DjangoEnv(BaseModel):
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


from pydantic import BaseModel, validator, AnyUrl, constr


class DatabaseEnv(BaseModel):
    DATABASE_NAME: str
    DATABASE_HOST: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_PORT: int

    @validator("DATABASE_NAME")
    def validate_database_name(cls, value):
        if not value:
            raise ValueError("DATABASE_NAME cannot be empty")
        return value

    @validator("DATABASE_HOST")
    def validate_database_host(cls, value):
        if not value:
            raise ValueError("DATABASE_HOST cannot be empty")
        return value

    @validator("DATABASE_USER")
    def validate_database_user(cls, value):
        if not value:
            raise ValueError("DATABASE_USER cannot be empty")
        return value

    @validator("DATABASE_PASSWORD")
    def validate_database_password(cls, value):
        if not value:
            raise ValueError("DATABASE_PASSWORD cannot be empty")
        return value

    @validator("DATABASE_PORT")
    def validate_database_port(cls, value):
        if not (0 < value <= 65535):
            raise ValueError("DATABASE_PORT must be between 1 and 65535")
        return value


class EnvEmail(BaseModel):
    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_USE_TLS: bool
    EMAIL_USE_SSL: bool
    EMAIL_HOST_USER: EmailStr
    EMAIL_HOST_PASSWORD: str

    @validator("EMAIL_PORT")
    def validate_email_port(cls, value):
        if not (1 <= value <= 65535):
            raise ValueError("EMAIL_PORT must be a valid port number (1-65535)")
        return value

    @validator("EMAIL_USE_TLS", "EMAIL_USE_SSL")
    def validate_tls_ssl(cls, value):
        if not isinstance(value, bool):
            raise ValueError("EMAIL_USE_TLS and EMAIL_USE_SSL must be boolean values")
        return value


class OAuthEnv(BaseModel):
    GOOGLE_OAUTH2_CLIENT_ID: str
    GOOGLE_OAUTH2_CLIENT_SECRET: str

    @validator("GOOGLE_OAUTH2_CLIENT_ID")
    def validate_google_oauth2_client_id(cls, value):
        if not value:
            raise ValueError("GOOGLE_OAUTH2_CLIENT_ID must not be empty")
        return value

    @validator("GOOGLE_OAUTH2_CLIENT_SECRET")
    def validate_google_oauth2_client_secret(cls, value):
        if not value:
            raise ValueError("GOOGLE_OAUTH2_CLIENT_SECRET must not be empty")
        return value


class PlatformEnv(BaseModel):
    PLATFORM_URL: HttpUrl

    @validator("PLATFORM_URL")
    def validate_platform_url(cls, value):
        if not value.startswith("http://") and not value.startswith("https://"):
            raise ValueError("PLATFORM_URL must be a valid HTTP or HTTPS URL")
        return value


class Merged(DjangoEnv, DatabaseEnv, EnvEmail, OAuthEnv, PlatformEnv):
    pass


def load_env_vars():
    env_vars = {
        "TIME_ZONE": os.environ.get("TIME_ZONE"),
        "DATABASE_URL": os.environ.get("DATABASE_URL"),
        "DEBUG": os.environ.get("DEBUG").lower() == "true"
        if os.environ.get("DEBUG")
        else False,
        # ------------
        "EMAIL_HOST": os.environ.get("EMAIL_HOST"),
        "EMAIL_PORT": int(os.environ.get("EMAIL_PORT", 0)),
        "EMAIL_USE_TLS": os.environ.get("EMAIL_USE_TLS").lower() == "true"
        if os.environ.get("EMAIL_USE_TLS")
        else False,
        "EMAIL_USE_SSL": os.environ.get("EMAIL_USE_SSL").lower() == "true"
        if os.environ.get("EMAIL_USE_SSL")
        else False,
        "EMAIL_HOST_USER": os.environ.get("EMAIL_HOST_USER"),
        "EMAIL_HOST_PASSWORD": os.environ.get("EMAIL_HOST_PASSWORD"),
        # ------------
        "DATABASE_NAME": os.environ.get("DATABASE_NAME"),
        "DATABASE_HOST": os.environ.get("DATABASE_HOST"),
        "DATABASE_USER": os.environ.get("DATABASE_USER"),
        "DATABASE_PASSWORD": os.environ.get("DATABASE_PASSWORD"),
        "DATABASE_PORT": int(os.environ.get("DATABASE_PORT", 5432)),
        # ------------
        "GOOGLE_OAUTH2_CLIENT_ID": os.environ.get("GOOGLE_OAUTH2_CLIENT_ID"),
        "GOOGLE_OAUTH2_CLIENT_SECRET": os.environ.get("GOOGLE_OAUTH2_CLIENT_SECRET"),
        # ------------
        "PLATFORM_URL": os.environ.get("PLATFORM_URL", "http://127.0.0.1:8000"),
    }
    return Merged(**env_vars)


env = load_env_vars()
