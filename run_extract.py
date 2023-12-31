import click

from mus.config.config import app_config
from mus.constant import cons_gdelt20
from mus.core.app_logger.fabrics.config_init import init_logger_from_config
from mus.gdelt20.extract.run_extract_gdelt import run_extract_gdelt
from mus.gdelt20.load.run_load_gdelt import run_load_gdelt

logger = init_logger_from_config(name=app_config["PROJECT_NAME"], config=app_config["LOGGER"])


@click.group(help="Extract")
@click.pass_context
def cli(ctx):
    ctx.obj.update(app_config)


def check_params(start_date, finish_date):
    assert start_date <= finish_date, f"{start_date} gt {finish_date}"


@cli.command("extract_gdelt", help="Extract gdelt20 data into storage")
@click.option("--base_path", "-b",
              type=click.Path(),
              required=True,
              default=cons_gdelt20.DEFAULT_DATA_PATH,
              help="gdelt20 data target path")
@click.option("--start_date", "-s",
              type=click.DateTime(),
              required=True,
              help="gdelt20 data set start day")
@click.option("--finish_date", "-f",
              type=click.DateTime(),
              required=True,
              help="gdelt20 data set finish date")
@click.option("--languages", "-l",
              type=click.Choice(cons_gdelt20.GDELT_LANGUAGE, case_sensitive=True),
              required=True,
              default=cons_gdelt20.GDELT_LANGUAGE,
              multiple=True,
              help="gdelt20 data set language corpus")
@click.option("--object_types", "-o",
              type=click.Choice(cons_gdelt20.GDELT_OBJ_TYPE, case_sensitive=True),
              required=True,
              default=cons_gdelt20.GDELT_OBJ_TYPE,
              multiple=True,
              help="gdelt20 data set object type to load")
@click.pass_obj
def extract_gdelt(config_obj, base_path, start_date, finish_date, languages, object_types):
    check_params(start_date, finish_date)

    logger.info("Start gdelt2 data extraction")
    run_extract_gdelt(
        config_obj,
        base_path,
        start_date,
        finish_date,
        languages,
        object_types
    )
    logger.info("Finish gdelt2 data extraction")


@cli.command("load_gdelt", help="Load gdelt20 data into db")
@click.option("--base_path", "-b",
              type=click.Path(),
              required=True,
              default=cons_gdelt20.DEFAULT_DATA_PATH,
              help="gdelt20 data source path")
@click.option("--target_service", "-t",
              required=True,
              default=cons_gdelt20.TARGET_SERVICES[0],
              help="gdelt20 data source path")
@click.option("--start_date", "-s",
              type=click.DateTime(),
              required=True,
              help="gdelt20 data set start day")
@click.option("--finish_date", "-f",
              type=click.DateTime(),
              required=True,
              help="gdelt20 data set finish date")
@click.option("--languages", "-l",
              type=click.Choice(cons_gdelt20.GDELT_LANGUAGE, case_sensitive=True),
              required=True,
              default=cons_gdelt20.GDELT_LANGUAGE,
              multiple=True,
              help="gdelt20 data set language corpus")
@click.option("--object_types", "-o",
              type=click.Choice(cons_gdelt20.GDELT_OBJ_TYPE, case_sensitive=True),
              required=True,
              default=cons_gdelt20.GDELT_OBJ_TYPE,
              multiple=True,
              help="gdelt20 data set object type to load")
@click.pass_obj
def load_gdelt(config_obj, base_path, target_service, start_date, finish_date, languages, object_types):
    check_params(start_date, finish_date)

    logger.info("Start gdelt2 data loading")
    run_load_gdelt(
        config_obj,
        base_path,
        target_service,
        start_date,
        finish_date,
        languages,
        object_types
    )
    logger.info("Finish gdelt2 data loading")


if __name__ == "__main__":
    cli(obj={})
