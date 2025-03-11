import os

PROJECT_NAME = "FastApi Project"
DEBUG = True
JWT_ALGORITHM = "HS256"
JWT_SECRET = ""
REFRESH_TOKEN_EXPIRE_DAYS = 7
ACCESS_TOKEN_EXPIRE_MINUTES = 24 * 24

ALLOW_ORIGINS = ["http://localhost", "http://localhost:8080", "https://example.com"]

CELERY_BROKER_URL: str = os.environ.get("CELERY_BROKER_URL", "")
CELERY_RESULT_BACKEND: str = os.environ.get("CELERY_RESULT_BACKEND", "")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_REGION = os.environ.get("AWS_REGION", "")
BROKER_URL = f"sqs://{AWS_ACCESS_KEY_ID}:{AWS_SECRET_ACCESS_KEY}@"
CELERY_BROKER_TRANSPORT_OPTIONS = {
    "region": AWS_REGION,
    "visibility_timeout": 3 * 60 * 60,
    "predefined_queues": {
        "producer_queue": {
            "url": CELERY_BROKER_URL,
            "access_key_id": AWS_ACCESS_KEY_ID,
            "secret_access_key": AWS_SECRET_ACCESS_KEY,
        },
    },
}


# Email settings
SMTP_SERVER: str = "smtp.gmail.com"
SMTP_PORT: int = 587
SMTP_USERNAME: str = "your-email@gmail.com"
SMTP_PASSWORD: str = "your-app-password"
DEFAULT_SENDER: str = "ratchanonth60@gmail.com"
EMAIL_TEMPLATES_DIR: str = "app/templates/email"
