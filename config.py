# config.py
# Flask configuration classes for the Stroke Risk Monitoring API.
# Loaded by create_app() via app.config.from_object().

import os
from dotenv import load_dotenv

load_dotenv()  # reads .env if present; no-op in production containers


class BaseConfig:
    """Shared settings for all environments."""

    # ── watsonx.ai ────────────────────────────────────────────────────────────
    # Use .get() so the class can be imported without the env var set
    # (tests override this value on the app.config dict directly).
    WATSONX_API_KEY: str = os.getenv("WATSONX_API_KEY", "")
    WATSONX_URL: str = os.getenv(
        "WATSONX_URL", "https://us-south.ml.cloud.ibm.com"
    )
    WATSONX_PROJECT_ID: str = os.getenv(
        "WATSONX_PROJECT_ID", "746c612f-47a6-4d52-96df-87c9aa25f468"
    )

    # ── Flask ─────────────────────────────────────────────────────────────────
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-production")
    JSON_SORT_KEYS: bool = False


class DevelopmentConfig(BaseConfig):
    DEBUG: bool = True
    TESTING: bool = False


class TestingConfig(BaseConfig):
    DEBUG: bool = True
    TESTING: bool = True
    # Allow tests to override WATSONX_API_KEY with a dummy value
    WATSONX_API_KEY: str = os.getenv("WATSONX_API_KEY", "test-key")


class ProductionConfig(BaseConfig):
    DEBUG: bool = False
    TESTING: bool = False
