import socketio

static_files = {
    '/static': './public',
}

# for asyncio-based ASGI applications
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins="*")
secondapp = socketio.ASGIApp(sio, static_files=static_files)


@sio.event
def connect(sid, environ, auth):
    print('connect ', sid)


@sio.event
def disconnect(sid):
    print('disconnect ', sid)
