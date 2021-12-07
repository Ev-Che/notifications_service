from fastapi import APIRouter
from starlette.responses import HTMLResponse
from starlette.websockets import WebSocket

from app.services.web_socket_services import WebSocketService

router = APIRouter()


@router.get("/")
async def get():
    return HTMLResponse(html)


@router.websocket("/ws/{client_jwt}")
async def websocket_endpoint(websocket: WebSocket, client_jwt: str):
    await WebSocketService().process_connection(websocket=websocket,
                                                client_jwt=client_jwt)


html = """
<!DOCTYPE html>
<html>
<head>
    <title>Chat</title>
</head>
<body>
<h1>Notifications</h1>
<ul id='messages'>
</ul>
<script>
    var client_jwt = window.prompt("JWT: ");
    var ws = new WebSocket(`ws://0.0.0.0:8002/ws/${client_jwt}`);
    ws.onmessage = function (event) {
        var messages = document.getElementById('messages')
        var message = document.createElement('li')
        var content = document.createTextNode(event.data)
        message.appendChild(content)
        messages.appendChild(message)
    };
</script>
</body>
</html>
"""
