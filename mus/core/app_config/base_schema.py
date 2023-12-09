"""
Base config schema class.
Based on trafaret module.

"""


class TrafaretConfigSchemaBase:
    """
    Base config schema class.

    Main "get_validator" method should be
    overwritten in child classes.

    """

    # pylint: disable=R0201
    def get_validator(self):
        """
        Get current validation schema (validator).
        Should be overwritten in child classes.

        :return: Validation schema (validator)
        :rtype: Callable

        """
        return lambda x: x

    def validate_and_build(self, raw_config):
        """
        Validate raw config data against given schema
        nd build config structure.

        :param raw_config: Raw config data
        :type raw_config: duct[Any]

        :return: Validated structured config data
        :rtype: dict[Any]

        """
        return self.get_validator()(raw_config)
