import sys

import click

from mus.api.config.config import api_config
from mus.api.setup_api import create_api
from mus.core.app_logger.fabrics.config_init import init_logger_from_config

logger = init_logger_from_config(name=api_config["PROJECT_NAME"], config=api_config["LOGGER"])

app = create_api()


@click.group(help="Api Runner")
@click.pass_context
def cli(ctx):
    ctx.obj.update(api_config)


# periodical tasks here
# from fastapi_utils.tasks import repeat_every
# @app.on_event("startup")
# @repeat_every(seconds=15, logger=logger)
# def periodical_task() -> None:
#     logger.info({"status": "ok"})


@cli.command("run_api", help="Run Unicorn to expose api")
@click.option('--reload', is_flag=True, help="Reload Unicorn")
@click.pass_obj
def run_api(app_obj, reload):
    """
    """
    import uvicorn

    _ = app_obj

    logger.info("Starting uvicorn")
    logger.info(
        "Host: %s, port: %s, reload: %s",
        api_config["UVICORN_HOST"],
        api_config["UVICORN_PORT"],
        reload
    )

    uvicorn.run(
        app,
        host=api_config["UVICORN_HOST"],
        reload=reload,
        port=int(api_config["UVICORN_PORT"]),
    )

    logger.info("Shutted down")
    sys.exit()


if __name__ == "__main__":
    cli(obj={})
