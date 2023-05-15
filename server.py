from json import JSONDecodeError
from marshmallow import ValidationError
from schemas import MessageSchema
from aiohttp import web
from bot import send_message_to_all, send_message
from aiohttp_apispec import docs, request_schema, setup_aiohttp_apispec

routes = web.RouteTableDef()


@docs(
   tags=["telegram"],
   summary="GET message API",
   description="This end-point GET message to telegram bot user/users",
)
@request_schema(MessageSchema())
@routes.get("/")
async def index_get(request: web.Request) -> web.Response:
    await send_message_to_all("Hello, bitch!")
    return web.json_response({"result": "OK"})


@docs(
   tags=["telegram"],
   summary="POST message API",
   description="This end-point POST message to telegram bot user/users",
)
@request_schema(MessageSchema())
@routes.post("/")
async def index_get(request: web.Request) -> web.Response:
    try:
        payload = await request.json()
    except JSONDecodeError:
        return web.json_response({"status": "Request data is invalid"})

    try:
        schema = MessageSchema()
        data = schema.load(payload)
    except ValidationError as e:
        return web.json_response({"status": "Validation Error", "error": e.messages})

    if data.get("chat_id"):
        await send_message(data.get("chat_id"), data.get("message"))
    else:
        await send_message_to_all(data.get("message"))
    return web.json_response({"result": "KO"})


if __name__ == "__main__":
    app = web.Application()
    setup_aiohttp_apispec(
        app=app, title="Lightl Bot documentation", version="v0.1",
        url="/api/docs/swagger.json", swagger_path="/api/docs",
    )
    app.add_routes(routes)
    web.run_app(app, port=5000)
