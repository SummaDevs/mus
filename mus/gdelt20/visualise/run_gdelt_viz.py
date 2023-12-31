import logging

import folium
import geemap.foliumap
import pandas as pd

from mus.config.config import app_config
from mus.constant.cons_gdelt20 import EVENT_CODE_FIELD
from mus.constant.cons_gdelt20 import FOLIUM_MAP_CENTER
from mus.constant.cons_gdelt20 import LATITUDE_FIELD
from mus.constant.cons_gdelt20 import LONGTITUDE_FIELD
from mus.constant.cons_gdelt20 import SOURCE_URL_FIELD
from mus.core.location.location_utils import get_norm_location
from mus.data_models.gdelt20.gdelt_thesaurus.cameo_eventcodes import ASSAULT_CODE_SET
from mus.data_models.gdelt20.gdelt_thesaurus.cameo_eventcodes import CAMEO_CODE_DESC
from mus.data_models.gdelt20.gdelt_thesaurus.cameo_eventcodes import COERCE_CODE_SET
from mus.data_models.gdelt20.gdelt_thesaurus.cameo_eventcodes import FIGHT_CODE_SET
from mus.data_models.gdelt20.gdelt_thesaurus.cameo_eventcodes import INTEL_CODE_SET
from mus.data_models.gdelt20.gdelt_thesaurus.cameo_eventcodes import INTEREST_CODE_SET
from mus.data_models.gdelt20.gdelt_thesaurus.cameo_eventcodes import MIL_CODE_SET

logger = logging.getLogger(app_config["PROJECT_NAME"])

COLOR_ICON = {
    "intel": ('pink', 'bookmark'),
    "mil": ('purple', 'flag'),
    "coerce": ('lightred', 'glass'),
    "assault": ('orange', 'home'),
    "fight": ("red", 'star'),
    "default": ('gray', None)
}


def get_icon_att(ev_code):
    color, icon = COLOR_ICON["default"]

    if ev_code in INTEL_CODE_SET:
        color, icon = COLOR_ICON["intel"]
    elif ev_code in MIL_CODE_SET:
        color, icon = COLOR_ICON["mil"]
    elif ev_code in COERCE_CODE_SET:
        color, icon = COLOR_ICON["coerce"]
    elif ev_code in ASSAULT_CODE_SET:
        color, icon = COLOR_ICON["assault"]
    elif ev_code in FIGHT_CODE_SET:
        color, icon = COLOR_ICON["fight"]

    return {"color": color, "icon": icon}


icon_func = lambda ev_code: folium.Icon(**get_icon_att(ev_code))


def read_geo_data(file_path):
    """
    query example 
    Babruysk = 53.15, 29.24
    Aktau = 43.65, 51.17
    
    lat_min = 43.65
    lat_max = 53.15
    
    long_min = 29.24
    long_max = 51.17

    SELECT 
      Actor1Name, 
      Actor2Name, 
      AvgTone, 
      Actor1Geo_Lat, 
      Actor1Geo_Long, 
      ActionGeo_Lat, 
      ActionGeo_Long, 
      EventCode, 
      SOURCEURL  
    FROM `gdelt20-bq.gdeltv2.events_partitioned` 
    WHERE 
      DATE(_PARTITIONTIME) >= "2023-05-17" AND
      ActionGeo_Lat >= {lat_min} AND ActionGeo_Lat <= {lat_max} AND
      ActionGeo_Long >= {long_min} AND ActionGeo_Long <= {long_max}
    LIMIT 100000;
    """

    data = pd.read_csv(
        file_path,
        dtype={EVENT_CODE_FIELD: str}
    )

    logger.info("Events per period - %s", data.shape[0])

    data = data[data.EventCode.isin(INTEREST_CODE_SET)]

    logger.info("Events of interests - %s", data.shape[0])

    data.drop_duplicates(
        subset=[SOURCE_URL_FIELD],
        keep="last",
        inplace=True,
        ignore_index=True
    )

    logger.info("Sources per period - %s", data.shape[0])

    data[LATITUDE_FIELD] = data[LATITUDE_FIELD].fillna(0)
    data[LONGTITUDE_FIELD] = data[LONGTITUDE_FIELD].fillna(0)

    return data


def folium_map(data):
    fmap = folium.Map(location=FOLIUM_MAP_CENTER, zoom_start=9)

    for _, row in data.iterrows():
        folium.Marker(
            get_norm_location(row[LATITUDE_FIELD], row[LONGTITUDE_FIELD]),
            popup=f'<a href="{row[SOURCE_URL_FIELD]}" target=”_blank”>{CAMEO_CODE_DESC[row[EVENT_CODE_FIELD]]}</a>',
            icon=icon_func(row[EVENT_CODE_FIELD])
        ).add_to(fmap)

    fmap.show_in_browser()

    return fmap


def geemap_show_in_browser(data):
    fmap = geemap.foliumap.Map(
        location=FOLIUM_MAP_CENTER,
        zoom_start=8,
        tiles="Evens in period",
        attr="GDELT & l"
    )

    for _, row in data.iterrows():
        geemap.foliumap.Marker(
            get_norm_location(row[LATITUDE_FIELD], row[LONGTITUDE_FIELD]),
            popup=f'<a href="{row[SOURCE_URL_FIELD]}" target=”_blank”>{CAMEO_CODE_DESC[row[EVENT_CODE_FIELD]]}</a>',
            icon=icon_func(row[EVENT_CODE_FIELD])
        ).add_to(fmap)

    fmap.show_in_browser()


def run_gdelt_viz(_, file_path):
    data = read_geo_data(file_path)

    folium_map(data)

    geemap_show_in_browser(data)
