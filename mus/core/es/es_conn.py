from elasticsearch_dsl import connections


def create_es_conn(config: dict):
    # TODO: hosts
    host = f"{config['ES']['ES_HOST_SCHEMA']}://{config['ES']['ES_HOST']}:{config['ES']['ES_PORT']}"

    connections.configure(**{
        'default': {'hosts': host},
        config["PROJECT_NAME"]: {'hosts': host}
    })
