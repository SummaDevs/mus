# latitude coordinates before longitude
# latitude coordinate is between -90 and 90.
# longitude coordinate is between -180 and 180.
# Babruysk = 53.15, 29.24
# Aktau = 43.65, 51.17

lat_min = 43.65
lat_max = 53.15

long_min = 29.24
long_max = 51.17

query = f"""
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
FROM `gdelt-bq.gdeltv2.events_partitioned` 
WHERE 
  DATE(_PARTITIONTIME) >= "2023-05-17" AND
  ActionGeo_Lat >= {lat_min} AND ActionGeo_Lat <= {lat_max} AND
  ActionGeo_Long >= {long_min} AND ActionGeo_Long <= {long_max}
LIMIT 50000;
"""
