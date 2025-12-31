import json
import logging
from typing import cast

from automa.bot import AsyncAutoma, CodeProposeParams
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
    body = json.loads(payload)

    # Skip if not `task.created` event
    if "type" not in body or body["type"] != "task.created":
        return Response(status_code=204)

    # Verify request
    if signature is None or not verify_webhook(
        env().automa_webhook_secret, signature, payload
    ):
        logging.warning(
            "Invalid signature",
        )

        return Response(status_code=401)

    base_url = request.headers.get("x-automa-server-host")

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
        update(folder, body["data"]["task"])

        # Propose code
        await automa.code.propose(
            cast(
                CodeProposeParams,
                {
                    **body["data"],
                    "proposal": {
                        "title": "We changed your code",
                    },
                },
            )
        )
    finally:
        # Clean up
        await automa.code.cleanup(body["data"])

    return Response(status_code=200)
