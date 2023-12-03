"""

Topic classification (TC), Hidden topic recognition (HTP), Topic segmentation (TS)

"""

import sys

import click

from mus.config.config import app_config
from mus.constant.cons_nlp import NLP_LANG
from mus.core.app_logger.fabrics.config_init import init_logger_from_config
from mus.core.file_utils.path_utils import norm_dir_path
from mus.topic.run_topic import run_model_topic

logger = init_logger_from_config(name=app_config["PROJECT_NAME"], config=app_config["LOGGER"])


@click.group(help="Data transform runner")
@click.pass_context
def cli(ctx):
    ctx.obj.update(app_config)


@cli.command("model_topic", help="Topics modeling from json archive text ")
@click.option("--text_path", "-t",
              type=click.Path(),
              required=True,
              help="extracted text json file base path")
@click.option("--lang_list", "-l",
              type=str,
              multiple=True,
              default=["ru"],
              help="comma separated list of languages to analyse, excepted values are {}".format(",".join(NLP_LANG)))
@click.option("--per_subdir",
              is_flag=True,
              show_default=True,
              default=False,
              help="Create topics list per subdirectory")
@click.option("--update",
              is_flag=True,
              show_default=True,
              default=False,
              help="Update json docs metadata")
@click.pass_obj
def model_topic(config_obj, text_path, lang_list, per_subdir, update):
    logger.info("Starting topic modeling")

    run_model_topic(config_obj, norm_dir_path(text_path), lang_list, per_subdir, update)

    logger.info("Finish topic modeling")

    sys.exit()


@cli.command("benchmarks", help="Topics Benchmarks")
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
