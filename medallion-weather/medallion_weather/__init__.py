import os

from dagster import Definitions
from dotenv import load_dotenv

from .assets import (
    bronze_layer_assets,
    external_source_assets,
    gold_layer_assets,
    silver_layer_assets,
)
from .jobs import all_assets_job
from .resources import resource_defs_by_env
from .sensors.asset_sensors import from_air_gold_aqi_with_pm_asset

load_dotenv()

deploy_env = os.environ.get("MEDALLION_WEATHER_ENV", "dev")
all_assets = [
    *bronze_layer_assets,
    *silver_layer_assets,
    *gold_layer_assets,
    *external_source_assets,
]
all_jobs = [all_assets_job]
all_sensors = [from_air_gold_aqi_with_pm_asset]
resource_defs = resource_defs_by_env[deploy_env]

medallion_weather_defs = Definitions(
    assets=all_assets, jobs=all_jobs, sensors=all_sensors, resources=resource_defs
)
