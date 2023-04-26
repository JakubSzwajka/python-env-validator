# Environment Variable Validator

This repository contains a Python implementation of an environment variable validator inspired by the [Create T3 App documentation](https://t3.ch/docs/usage/environment-variables) for Next.js applications. The Python version is designed for Django-like environment variables.

## Overview

The environment variable validator uses the Pydantic library to validate environment variables at runtime. This ensures that your application only runs if the required environment variables are properly set.

The validation is split into two parts:

1. Server-side environment variables
2. Client-side environment variables

Server-side environment variables are only accessible on the server, while client-side environment variables are accessible on both the server and client.

To add a new environment variable, you need to update both your `.env` file and the Python script that defines the validator.

## How it Works

1. Define server-side environment variables schema in the `ServerEnv` class.
2. Define client-side environment variables schema in the `ClientEnv` class.
3. Merge the schemas into the `MergedEnv` class.
4. Read environment variables from the `.env` file using the `os` library.
5. Validate the environment variables using the `MergedEnv` schema.
6. If the environment variables are valid, store them in the `env` object.

You can then import the `env` object in your application and use the validated environment variables.

## Example Usage

```python
from env_validator import env

# Access server-side environment variable
database_url = env.DATABASE_URL
```

## Inspiration
This implementation is inspired by the environment variable validation approach detailed in the [Create T3 App documentation](https://t3.ch/docs/usage/environment-variables) for Next.js applications.
