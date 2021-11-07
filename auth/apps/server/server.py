import socketio

static_files = {
    '/static': './public',
}

# for asyncio-based ASGI applications
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins="*")
secondapp = socketio.ASGIApp(sio, static_files=static_files)


@sio.event
async def connect(sid, environ, auth):
    await sio.emit("my message", {"first": "message"})


@sio.event
async def disconnect(sid):
    print("I'm disconnected!")


@sio.event
async def send_message(sid, data):
    print("movida")
