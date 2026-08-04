import os


database_url = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgre123@127.0.0.1:5432/grade_horaria"
)

if database_url.startswith("postgres://"):
    database_url = database_url.replace(
        "postgres://",
        "postgresql://",
        1
    )


class Config:
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "remada-desenvolvimento"
    )

    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False