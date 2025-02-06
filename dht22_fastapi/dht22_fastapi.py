"""Main module."""

import asyncio

from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:5500", # for vscode liveserver
    "http://dht22-fastapi.app.brisecom.net:8000/",
    "https://dht22-fastapi.app.brisecom.net:8000/",
    "http://dht22-fastapi.app.brisecom.net/",
    "https://dht22-fastapi.app.brisecom.net/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

from sse_starlette.sse import EventSourceResponse

from dht22_parse.dht22_parse import DHT22Parse

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("test-sse-deployed.html", {"request": request})

@app.get("/stream")
async def main():

    dht22 = DHT22Parse()
    dht22.init()

    # split request for sending only one chunk at a time
    return StreamingResponse(dht22.dht22_reader_generator_json(), media_type="application/xndjson")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    dht22 = DHT22Parse()
    await dht22.init()
    async for message in dht22.dht22_reader_generator_json():
        print (message)
        await websocket.send_text(f"{message}")

@app.get("/sse")
async def sse():

    dht22 = DHT22Parse()
    dht22.init()

    return EventSourceResponse(dht22.dht22_reader_generator_json(), media_type="application/json")
