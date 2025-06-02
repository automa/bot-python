import json
import logging

from automa.bot import AsyncAutoma
from automa.bot.webhook import verify_webhook
from fastapi import FastAPI, Request, Response

from .env import env
from .update import update

app = FastAPI()


@app.get("/health")
async def health_check():
    return Response(status_code=200)


@app.post("/automa")
async def automa_hook(request: Request):
    signature = request.headers.get("webhook-signature")
    payload = (await request.body()).decode("utf-8")

    # Verify request
    if not verify_webhook(env().automa_webhook_secret, signature, payload):
        logging.warning(
            "Invalid signature",
        )

        return Response(status_code=401)

    base_url = request.headers.get("x-automa-server-host")
    body = json.loads(payload)

    # Create client with base URL
    automa = AsyncAutoma(base_url=base_url)

    # Download code
    folder = await automa.code.download(body["data"])

    try:
        # Main logic for updating the code. It takes
        # the folder location of the downloaded code
        # and updates it.
        #
        # **NOTE**: If this takes a long time, make
        # sure to return a response to the webhook
        # before starting the update process.
        update(folder)

        # Propose code
        await automa.code.propose(
            {
                **body["data"],
                "proposal": {
                    "message": "We changed your code",
                },
            }
        )
    finally:
        # Clean up
        await automa.code.cleanup(body["data"])

    return Response(status_code=200)
