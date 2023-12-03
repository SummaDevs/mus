"""
Config Factories based on Config schemes.

"""
from .base_schema import TrafaretConfigSchemaBase
from .config_sources import DotEnvConfig
from .config_sources import EnvConfig
from .config_sources import JsonConfig
from .config_sources import YamlConfig


class BaseConfigFactory:
    """
    Base Config Factory.

    """
    schema = TrafaretConfigSchemaBase

    @classmethod
    def get_config_from_env(cls, **kwargs):
        """
        Load config from environment variables.

        **kwargs arguments can be used to add extra fields
        to config before validation.

        :param kwargs: Extra config fields
        :type kwargs: dict[Any]

        :return: Built structured config
        :rtype: dict

        """
        return EnvConfig(
            schema=cls.schema(),
            **kwargs,
        ).as_dict

    @classmethod
    def get_config_from_dotenv(cls, file_path, **kwargs):
        """
        Load config from .env file.

        **kwargs arguments can be used to add extra fields
        to config before validation.

        :param file_path: .env file full path
        :type file_path: str

        :param kwargs: Extra config fields
        :type kwargs: dict[Any]

        :return: Built structured config
        :rtype: dict

        """
        return DotEnvConfig(
            file_path=file_path,
            schema=cls.schema(),
            **kwargs,
        ).as_dict

    @classmethod
    def get_config_from_json(cls, file_path, sub_path=None, **kwargs):
        """
        Load config from JSON file.

        **kwargs arguments can be used to add extra fields
        to config before validation.

        :param file_path: JSON file full path
        :type file_path: str

        :param sub_path: JSON structure sub path to load only
        :type sub_path: Optional[str]

        :param kwargs: Extra config fields
        :type kwargs: dict[Any]

        :return: Built structured config
        :rtype: dict

        """
        return JsonConfig(
            file_path=file_path,
            schema=cls.schema(),
            sub_path=sub_path,
            **kwargs,
        ).as_dict

    @classmethod
    def get_config_from_yaml(cls, file_path, sub_path=None, **kwargs):
        """
        Load config from YAML file.

        **kwargs arguments can be used to add extra fields
        to config before validation.

        :param file_path: JSON file full path
        :type file_path: str

        :param sub_path: JSON structure sub path to load only
        :type sub_path: Optional[str]

        :param kwargs: Extra config fields
        :type kwargs: dict[Any]

        :return: Built structured config
        :rtype: dict

        """
        return YamlConfig(
            file_path=file_path,
            schema=cls.schema(),
            sub_path=sub_path,
            **kwargs,
        ).as_dict
