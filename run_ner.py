"""

Named entity recognition (NER), Terminology extraction

"""

import sys

import click

from mus.config.config import app_config
from mus.constant.cons_nlp import NLP_LANG
from mus.core.app_logger.fabrics.config_init import init_logger_from_config
from mus.core.file_utils.path_utils import norm_dir_path
from mus.ner.run_ner import run_ner

logger = init_logger_from_config(name=app_config["PROJECT_NAME"], config=app_config["LOGGER"])


@click.group(help="NER Runner")
@click.pass_context
def cli(ctx):
    ctx.obj.update(app_config)


@cli.command("ner", help="Named entities recognition from json archive text ")
@click.option("--text_path", "-t",
              type=click.Path(),
              required=True,
              help="extracted text json file base path")
@click.option("--lang_list", "-l",
              type=str,
              multiple=True,
              default=["ru"],
              help="comma separated list of languages to analyse, excepted values are {}".format(",".join(NLP_LANG)))
@click.option("--update",
              is_flag=True,
              show_default=True,
              default=False,
              help="Update json docs metadata")
@click.pass_obj
def ner(config_obj, text_path, lang_list, update):
    logger.info("Starting named entity recognition")

    run_ner(config_obj, norm_dir_path(text_path), lang_list, update)

    logger.info("Finish  named entity recognition")

    sys.exit()


@cli.command("benchmarks", help="NER Benchmarks")
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
