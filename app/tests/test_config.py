from app.core.config.settings import settings

def test_settings_load_defaults():
    assert settings.APP_NAME == "Lee Kuan Yew AI Chatbot"
    assert settings.APP_VERSION == "0.4.0"
    assert isinstance(settings.ALLOWED_ORIGINS, list)
    assert settings.DATABASE_URL.startswith("sqlite")
