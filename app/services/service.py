import os

import jwt


class Service:

    @staticmethod
    async def get_id_from_jwt_token(jwt_token: str) -> int:
        """Returns user_id from JWT token. Used PyJWT lib."""

        secret = os.environ.get('JWT_SECRET_KEY')
        payload = jwt.decode(jwt_token, secret, algorithms=["HS256"])
        return payload.get('user_id')

    @staticmethod
    def get_database_url() -> str:
        """Returns connection string to db."""
        from dotenv import load_dotenv
        load_dotenv()

        return (f'postgresql://'
                f'{os.environ.get("DB_USER")}:{os.environ.get("DB_PASSWORD")}@'
                f'{os.environ.get("DB_HOST")}:{os.environ.get("DB_PORT")}/'
                f'{os.environ.get("DB_NAME")}')
