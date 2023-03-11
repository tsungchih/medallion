from dagster import load_assets_from_package_module

from medallion_weather.assets import bronze, external, gold, silver

EXTERNAL_GROUP_NAME = "external"
BRONZE_GROUP_NAME = "bronze"
SILVER_GROUP_NAME = "silver"
GOLD_GROUP_NAME = "gold"
ALL_ASSET_GROUPS = [BRONZE_GROUP_NAME, SILVER_GROUP_NAME, GOLD_GROUP_NAME]

bronze_layer_assets = load_assets_from_package_module(
    package_module=bronze,
    group_name=BRONZE_GROUP_NAME,
)

silver_layer_assets = load_assets_from_package_module(
    package_module=silver,
    group_name=SILVER_GROUP_NAME,
)

gold_layer_assets = load_assets_from_package_module(
    package_module=gold,
    group_name=GOLD_GROUP_NAME,
)

external_source_assets = load_assets_from_package_module(
    package_module=external,
    group_name=EXTERNAL_GROUP_NAME,
)
