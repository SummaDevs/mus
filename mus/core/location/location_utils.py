def to_float(val):
    try:
        return float(val)
    except TypeError as _:
        return 0.0


def norm_lat(lat):
    lat = to_float(lat)
    return lat if -90.0 <= lat <= 90.0 else 0.0


def norm_lon(lon):
    lon = to_float(lon)
    return lon if -180.0 <= lon <= 180.0 else 0.0


def get_norm_location(lat, lon):
    return [norm_lat(lat), norm_lon(lon)]
