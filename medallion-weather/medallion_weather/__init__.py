import os

from dagster import Definitions, load_assets_from_modules
from dotenv import load_dotenv

from medallion_weather import assets
from medallion_weather.jobs import all_assets_job
from medallion_weather.resources import resource_defs_by_env
from medallion_weather.sensors.asset_sensors import from_air_gold_aqi_with_pm_asset

load_dotenv()

deploy_env = os.environ.get("MEDALLION_WEATHER_ENV", "dev")
all_assets = load_assets_from_modules([assets])
all_jobs = [all_assets_job]
all_sensors = [from_air_gold_aqi_with_pm_asset]
resource_defs = resource_defs_by_env[deploy_env]

medallion_weather_defs = Definitions(
    assets=all_assets, jobs=all_jobs, sensors=all_sensors, resources=resource_defs
)
