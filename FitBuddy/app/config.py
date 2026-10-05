import os

from dotenv import load_dotenv


# Load .env from the FitBuddy project root
load_dotenv()


class Settings:
    APP_NAME: str = os.getenv(
        "APP_NAME",
        "FitBuddy",
    )

    DEBUG: bool = os.getenv(
        "DEBUG",
        "true",
    ).lower() == "true"

    AI_ENABLED: bool = os.getenv(
        "AI_ENABLED",
        "false",
    ).lower() == "true"

    GEMINI_API_KEY: str = os.getenv(
        "GEMINI_API_KEY",
        "",
    )

    GEMINI_WORKOUT_MODEL: str = os.getenv(
        "GEMINI_WORKOUT_MODEL",
        "gemini-2.5-flash",
    )

    GEMINI_TIP_MODEL: str = os.getenv(
        "GEMINI_TIP_MODEL",
        "gemini-2.5-flash-lite",
    )

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./fitbuddy.db",
    )

    ADMIN_KEY: str = os.getenv(
        "ADMIN_KEY",
        "",
    )


# Global settings object used by the application
settings = Settings()