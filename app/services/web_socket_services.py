from asyncio import sleep

from loguru import logger
from starlette.websockets import WebSocket, WebSocketDisconnect

from app.services.connection_manager import ConnectionManager
from app.services.service import Service
from core.db_handler import DBHandler


class WebSocketService:

    manager = ConnectionManager()

    async def process_connection(self, websocket: WebSocket, client_jwt: str):
        user_id = await Service.get_id_from_jwt_token(client_jwt)
        await self.manager.connect(websocket)

        try:
            await WebSocketService()._send_messages_to_client(
                user_id=user_id, websocket=websocket)
        except WebSocketDisconnect:
            self.manager.disconnect(websocket)

    async def _send_messages_to_client(self, user_id: int, websocket):
        while True:
            notifications = await self._check_db(user_id=user_id)
            for notification in notifications:
                await self.manager.send_personal_message(
                    f"New notification: {notification.message}", websocket)
            await DBHandler().deactivate_notifications(notifications)

    @staticmethod
    async def _check_db(user_id: int):
        await sleep(5)
        logger.debug(f'Checking db for {user_id}')
        return DBHandler().get_user_notifications(user_id=user_id)
