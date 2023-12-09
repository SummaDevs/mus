"""

Text knowledge visualization

"""

import sys

import click

from mus.config.config import app_config
from mus.core.app_logger.fabrics.config_init import init_logger_from_config
from mus.core.file_utils.path_utils import norm_dir_path
from mus.vizualisation.run_visualisation import run_wordcloud_viz

logger = init_logger_from_config(name=app_config["PROJECT_NAME"], config=app_config["LOGGER"])


@click.group(help="Data visualisation Runner")
@click.pass_context
def cli(ctx):
    ctx.obj.update(app_config)


@cli.command("wordcloud_viz", help="Visualise wordcloud for structured text ")
@click.option("--text_path", "-t",
              type=click.Path(),
              required=True,
              help="extracted text json file base path")
@click.option("--per_subdir",
              is_flag=True,
              show_default=True,
              default=False,
              help="Visualize wordcloud per subdirectory")
@click.option("--per_topic",
              is_flag=True,
              show_default=True,
              default=False,
              help="Visualize wordcloud per subdirectory")
@click.pass_obj
def wordcloud_viz(config_obj, text_path, per_subdir, per_topic):
    logger.info("Starting wordcloud visualization")

    run_wordcloud_viz(config_obj, norm_dir_path(text_path), per_subdir, per_topic)

    logger.info("Finish wordcloud visualization")

    sys.exit()


@cli.command("benchmarks", help="Visualisation Benchmarks")
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
