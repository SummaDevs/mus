"""

Data cleansing and transformation, optical character recognition (OCR)

"""

import sys

import click

from mus.cleansing.run_extract_text import run_extract_text_json
from mus.cleansing.run_get_json_text import run_get_json_text
from mus.cleansing.run_index_text import run_index_text
from mus.config.config import app_config
from mus.core.app_logger.fabrics.config_init import init_logger_from_config
from mus.core.file_utils.path_utils import norm_dir_path

logger = init_logger_from_config(name=app_config["PROJECT_NAME"], config=app_config["LOGGER"])


@click.group(help="OCR & cleansing Runner")
@click.pass_context
def cli(ctx):
    ctx.obj.update(app_config)


@cli.command("extract_text_json", help="Extract unstructured archive text with metadata")
@click.option("--arc_path", "-a",
              type=click.Path(),
              required=True,
              help="file archive base path")
@click.option("--text_path", "-t",
              type=click.Path(),
              required=True,
              help="extracted json file base path")
@click.pass_obj
def extract_text_json(config_obj, arc_path, text_path):
    logger.info("Extracting text and metadata")

    run_extract_text_json(config_obj, norm_dir_path(arc_path), norm_dir_path(text_path))

    logger.info("Extraction finished")

    sys.exit()


@cli.command("index_json_text", help="Index jsom archive text ")
@click.option("--text_path", "-t",
              type=click.Path(),
              required=True,
              help="extracted text json file base path")
@click.option("--ci",
              is_flag=True,
              show_default=False,
              default=False,
              help="create new elastic search index, drop existed one if exists")
@click.pass_obj
def index_json_text(config_obj, text_path, ci):
    logger.info("Indexing text")

    run_index_text(config_obj, norm_dir_path(text_path), ci)

    logger.info("Indexing finished")

    sys.exit()


@cli.command("get_json_text", help="Extract text from json into silos")
@click.option("--json_text_path", "-t",
              type=click.Path(),
              required=True,
              help="file json base archive path")
@click.option("--text_path", "-d",
              type=click.Path(),
              required=True,
              help="extracted text file database base path")
@click.pass_obj
def get_json_text(config_obj, json_text_path, text_db_path):
    logger.info("Get text from json")

    run_get_json_text(config_obj, norm_dir_path(json_text_path), norm_dir_path(text_db_path))

    logger.info("Get text from json finished")

    sys.exit()


@cli.command("benchmarks", help="Cleansing Benchmarks")
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