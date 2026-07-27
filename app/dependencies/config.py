from app.core.config.settings import settings, Settings

def get_settings() -> Settings:
    """
    Dependency injection accessor for Settings.
    """
    return settings
