## Usage

**To add a module (admin for example) :**

- Add `admin` directory in `api/modules/admin`
- Create your `api/modules/admin/routes.py`
- Add this route to `api/routes.py` :
  `api.routes.include_router(admin_router, tags=["Admin"])`

**To add a model, do this :**

- Create a `models.py` in your modules :

```python
from sqlalchemy import Boolean, Column, String

from mus.core.db import Base
from mus.core.db import BaseFeaturesMixin


class User(Base, BaseFeaturesMixin):
    __tablename__ = "user"

    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
```

# LOGGER

Logger extension:

- fabric to init logger from standard params / config
- exists handlers: stdout / file / http / es
- already checked trafaret validator on sub-dicts
- full-wraps time tracing instead standard getLogger
- JSON formatter with serialize special types
- special syntax to do filter attach handlers before send log
- multiprocessing supports

> **important**: *stdout* logging use anyway even if not transmitted in parameters,
> but others handlers use only if they get configuration in params

### config logger

- Config logger from config object

  Logging supports config from config object with user-define params

  Config expect structure:

        STREAM_LEVEL: INFO
        FILE_NAME: app_log.log
        FILE_LEVEL: INFO
        HTTP_URL: https://logging.com
        HTTP_TOKEN: my_token
        HTTP_LEVEL: INFO

  Use code below to load logger params from config object

```python

from mus.core.app_config.config import Config
from mus.core.app_logger.fabrics.config_init import init_logger_from_config

config = Config().from_yaml(file_path="some_path to config.yaml")

logger = init_logger_from_config(
    name="SpecialUniqueName",
    config=config
)
```    

1. Create config use config_ext or any config fabric that return dict with expect params
2. Init config use *config* object and **init_from_config** fabric

> **important**: not all handlers config is required, stdout is useed by-default

### logger usage

Once configured logger with set unique name can use in all modules in package

**file**: *run.py*

```python
from mus.core.app_config.config import Config
from mus.core.app_logger.fabrics.config_init import init_logger_from_config

config = Config().from_yaml(file_path="some_path to config.yaml")

logger = init_logger_from_config(
    name="SpecialUniqueName",
    config=config
)
```    

**file**: *extractor.py*

```python
    
import logging

logger = logging.getLogger("SpecialUniqueName")  # the same logger as logger in run_load_gdelt.py

# logger mesage as dict
logger.info({
    "step": ...,
    "status": ...
})
```    

**file**: *saver.py*

 ```python
   
import logging

logger = logging.getLogger("SpecialUniqueName")  # the same logger as logger in run_load_gdelt.py

# logger mesage as string
logger.info("Start saver")
```    

1. Create logger use one of **init_logger_from_config** or **init_from_config** fabrics with special logger name
2. Use standard **getLogger** method with special logger name to get logger instance in any package module

### filter by send handlers

Inits logger use fabric in extensions create a special logger
which each send can configure pool of send handlers

```python
from mus.core.app_config.config import Config
from mus.core.app_logger.fabrics.config_init import init_logger_from_config

config = Config().from_yaml(file_path="some_path to config.yaml")

logger = init_logger_from_config(
    name="SpecialUniqueName",
    config=config
)

# do not send log msg to file
logger.info({
    "step": ...,
    "_skip_handlers": "file"
})

# do not send log msg to file and http
logger.info({
    "step": ...,
    "_skip_handlers": ["file", "http"]
})
```

> **warning**: can use only with json formatter (log message as dict)

For two frequent cases for handlers pool better use two different loggers,
but you can create **message creator** function / method

```python
from mus.core.app_config.config import Config
from mus.core.app_logger.fabrics.config_init import init_logger_from_config

config = Config().from_yaml(file_path="some_path to config.yaml")

logger = init_logger_from_config(
    name="SpecialUniqueName",
    config=config
)


def create_es_msg(log_msg):
    return {
        **log_msg,
        "_skip_handlers": ["stream", "http", "file"]
    }


# send log message only for es
logger.info(
    create_es_msg({
        "step": ...,
        "status": ...
    })
)
```

1. Create logger use one of **init_logger_from_config** or **init_from_config** fabrics
2. Create special **create_es_msg** function / method to extend logger message by *_skip_handlers* param
3. Use **create_es_msg** to create log message which send only to es handler

### time-tracing logger

The most interesting feature in logger package is time-tracing logger.
It can use as a complete replacement of base logger (instead getLogger)

**file**: *run.py*

```python
from mus.core.app_config.config import Config
from mus.core.app_logger.fabrics.config_init import init_logger_from_config

config = Config().from_yaml(file_path="some_path to config.yaml")

logger = init_logger_from_config(
    name="SpecialUniqueName",
    config=config
)
```

**file**: *extractor.py*

```python
from mus.core.app_logger.tracing_wrappers.time_tracing import TimeTracingLogger

# trace time for all methods and classes in module
logger = TimeTracingLogger("SpecialUniqueName")

# logger mesage as dict
logger.info({
    "step": ...,
    "status": ...
})
```        

> **important**: TimeTracingLogger uses a storage process (for usage time tracing in different
> scripts parts use different TimeTracingLogger instance)

**file**: *run.py*

```python    
from mus.core.app_config.config import Config
from mus.core.app_logger.fabrics.config_init import init_logger_from_config

config = Config().from_yaml(file_path="some_path to config.yaml")

logger = init_logger_from_config(
    name="SpecialUniqueName",
    config=config
)
```

**file**: *saver.py*

```python    

from mus.core.app_logger.tracing_wrappers.time_tracing import TimeTracingLogger


class Saver:

    def __init__(self):
        # tace from 00:00 for class Saver 
        self.logger = TimeTracingLogger("SpecialUniqueName")

    def some_method(self):
        self.logger.info("start save...")


class Processor:

    def __init__(self):
        # tace from 00:00 for class Processor
        self.logger = TimeTracingLogger("SpecialUniqueName")

    def some_method(self):
        self.logger.info("start save...")  
```

### exists handlers info

| Handler Name | Handler init param name | Handler Alias |
|--------------|-------------------------|---------------|
| Stdout       | log_std                 | stream        |
| File         | log_file                | file          |
| Http         | log_http                | http          |

> **important**: use handler 'alias' to skip some handlers use *_skip_handlers* param

# CONFIG

Config extension:

- same as dict object...
- load data from different sources: yaml / json / env / object / py-module
- can use with any validators /adapt to use trafaret without any wrappers/
- supports deep update
- sub-config get methods
- user-friendly work with prefixes to separate two or more configs in one config object
- config update as chain process
- supports serialize and de-serialize operations

### create config from yaml and deep update it from env

Example:

```python
from mus.core.app_config.config import Config

config = (
    Config()
    .from_yaml(file_path="some_path to config.yaml")
    .from_env(deep_update=True)
)
```

1. Create empty config object: **config = Config()**
2. Download config data to config from yml file: **.from_yaml**
3. Deep update current config data by env variables: **.from_env**

> **important**: You can update config without use chain

```python
from mus.core.app_config.config import Config

config = Config()
config = config.from_yaml(
    file_path="some_path to config.yaml"
)
config = config.from_env(
    deep_update=True
)
```    

> **important**: You can use any update sources direction (from_yaml > from_object > from_env > e.t.c)

### config validation before create / update

Example validate with trafaret:

```python
import trafaret as t

from mus.core.app_config.config import Config

# validator to validate config data from yaml file 
yaml_validator = t.Dict({
    t.Key("SOME_FIRST_CONFIG_KEY", optional=False): t.Int(),
    t.Key("SOME_SECOND_CONFIG_KEY", optional=True): t.Null() | t.Int()
})

# validator to validate data from env
env_validator = t.Dict({
    t.Key("SOME_SECOND_CONFIG_KEY", optional=False): t.Int()
})

# config with full validation
config = (
    Config()
    .from_yaml(
        file_path="some_path to config.yaml",
        validator=yaml_validator
    )
    .from_env(
        validator=env_validator,
        deep_update=True
    )
)
```

1. Create validators for expect config sources use trafaret
2. Download config data from any source use parameter: **validator**

> **important**: validation config data is good practice to work with some user-define data:
> try to use it every time

### add some other source loader

Example to add new source load_method <-> loader:

```python
from mus.core.app_config.abstracts import AbstractLoader
from mus.core.app_config.config import Config


class IniLoader(AbstractLoader):
    @classmethod
    def load(file_path):
        # some code
        pass


config = (
    Config()
    .load_from_file(
        file_path="some_path to config.ini",
        loader=IniLoader
    )
)
```

1. Create new source loader
2. Use special method **.load_from_file** to load data use new loader

### config prefix work

Example to work with prefixes in config

```python
from mus.core.app_config.config import Config

config = (
    Config()
    .from_yaml(
        file_path="some_path to config.yaml"
    )
    .add_with_prefix(
        prefix="PG_"
    )
)
```

1. Create config
2. Filter all config params and leave only parameters with prefix **PG_**
3. Can use **inversion** flag to leave only parameters without prefix **PG_**

> **important**: alternative of **add_with_prefix** method exists method **remove_with_prefix**
> to load all params without define prefix
