def dict_deep_update(update_to, update_from) -> dict:
    """
    Deep update

    :param update_to: updated object
    :type update_to: dict

    :param update_from: updating object
    :type update_from: dict

    :return: update result
    :rtype: dict

    """

    for param, param_val in update_from.items():
        if isinstance(param_val, dict):
            update_to[param] = dict_deep_update(
                update_to=update_to[param] if param in update_to else {},
                update_from=update_from[param]
            )

        else:
            # do not redefine are defined values with None
            if param_val or param not in update_to:
                update_to[param] = param_val

    return update_to
