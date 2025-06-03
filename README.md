# bot-python
Starter kit for Python bot for Automa

Please read the [Bot Development](https://docs.automa.app/bot-development) docs to understand how an [Automa][automa] bot works and how to develop it.

* `/automa` endpoint is the receiver for the webhook from [Automa][automa]
* `update` function in `app/update.py` is the logic responsible for updating code.
* `AUTOMA_WEBHOOK_SECRET` environment variable is available to be set instead of hard-coding it.

### Production

Start the app in production mode:

```
PYTHON_ENV=production uv run fastapi run
```

Needs [git](https://git-scm.org) to be installed on production.

### Development

Start the app in development mode:

```
uv run fastapi dev
```

### Testing

Run tests with:

```
uv run pytest
```

### Stack

* Uses [uv](https://docs.astral.sh/uv/) as a package manager.
* Uses [fastapi](https://fastapi.tiangolo.com/) as a server.

[automa]: https://automa.app
