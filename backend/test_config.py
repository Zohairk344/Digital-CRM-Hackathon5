from app.core.config import settings

def test_config():
    try:
        url = settings.DATABASE_URL
        print(f"DATABASE_URL: {url}")
        # Mask the password
        if settings.POSTGRES_PASSWORD:
            masked_url = url.replace(settings.POSTGRES_PASSWORD, "****")
            print(f"Masked DATABASE_URL: {masked_url}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_config()
