"""

Image and video description

"""

import sys

import click

from mus.config.config import app_config
from mus.core.app_logger.fabrics.config_init import init_logger_from_config

logger = init_logger_from_config(name=app_config["PROJECT_NAME"], config=app_config["LOGGER"])


@click.group(help="Video description Runner")
@click.pass_context
def cli(ctx):
    ctx.obj.update(app_config)


@cli.command("benchmarks", help="Video description Benchmarks")
@click.option("--data_path", "-d",
              type=click.Path(),
              required=True,
              help="benchmarks test data base path")
@click.option("--benchmarks_path", "-b",
              type=click.Path(),
              required=True,
              help="benchmarks results base path")
@click.pass_obj
def benchmarks(config_obj, data_path, benchmarks_path):
    logger.info("Start benchmarking")

    _ = config_obj, data_path, benchmarks_path

    logger.info("Benchmarking finished")

    sys.exit()


if __name__ == "__main__":
    cli(obj={})
