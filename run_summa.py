"""

Automatic summarization

"""

import sys

import click

from mus.config.config import app_config
from mus.core.app_logger.fabrics.config_init import init_logger_from_config
from mus.gdelt20.summa.run_gdelt_sum import run_gdelt_sum

logger = init_logger_from_config(name=app_config["PROJECT_NAME"], config=app_config["LOGGER"])


@click.group(help="Summarization Runner")
@click.pass_context
def cli(ctx):
    ctx.obj.update(app_config)


@cli.command("gdelt_sum", help="Summarise gdelt20 data")
@click.option("--file_path", "-p",
              type=click.Path(),
              required=True,
              help="gdelt20 data source file path")
@click.pass_obj
def gdelt_sum(config_obj, file_path):
    logger.info("Start gdelt2 data loading")

    run_gdelt_sum(config_obj, file_path)

    logger.info("Finish gdelt2 data loading")

    sys.exit()


@cli.command("benchmarks", help="Summarization Benchmarks")
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
