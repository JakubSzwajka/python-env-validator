# Environment Variable Validator

This repository contains a Python implementation of an environment variable validator inspired by the [Create T3 App documentation](https://create.t3.gg/en/usage/env-variables) for Next.js applications. The Python version is with example Django like env variables. Adjust it to suite your needs.

## Overview

The environment variable validator uses the Pydantic library to validate Django-specific environment variables at runtime. This ensures that your Django application only runs if the required environment variables are properly set.

The example validation includes the following Django environment variables:

1. TIME_ZONE
2. DATABASE_URL
3. DEBUG

## How it Works

1. Define the Django environment variables schema in the `Env` class with appropriate validators.
2. Read environment variables from the `.env` file using the `os` library.
3. Validate the environment variables using the `Env` schema.
4. If the environment variables are valid, store them in the `env` object.

You can then import the `env` object in your Django application and use the validated environment variables.

## Example Usage

```python
from env_validator import env

# Access TIME_ZONE environment variable
time_zone = env.TIME_ZONE

# Access DATABASE_URL environment variable
database_url = env.DATABASE_URL

# Access DEBUG environment variable
debug = env.DEBUG
```
