import click

from mus.gdelt20.extract.run_extract import run_extract
from mus.gdelt20.load.run_load import run_load
from mus.config.config import app_config
from mus.constant import cons_gdelt20
from mus.core.app_logger.fabrics.config_init import init_logger_from_config

logger = init_logger_from_config(name=app_config["PROJECT_NAME"], config=app_config["LOGGER"])


@click.group(help="Extract")
@click.pass_context
def cli(ctx):
    ctx.obj.update(app_config)


@cli.command("extract", help="Extract gdelt20 data into storage")
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
def extract(config_obj, base_path, start_date, finish_date, languages, object_types):
    run_extract(
        config_obj,
        base_path,
        start_date,
        finish_date,
        languages,
        object_types
    )

@cli.command("load", help="Load gdelt20 data into db")
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
def load(config_obj, base_path, target_service, start_date, finish_date, languages, object_types):
    # TODO: implement extraction into targets directly from api
    run_load(
        config_obj,
        base_path,
        target_service,
        start_date,
        finish_date,
        languages,
        object_types
    )


if __name__ == "__main__":
    cli(obj={})
