from dagster import load_assets_from_package_module

from medallion_air.assets import bronze, gold, silver

BRONZE_GROUP_NAME = "bronze"
SILVER_GROUP_NAME = "silver"
GOLD_GROUP_NAME = "gold"

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
    key_prefix=["GCP"],
    group_name=GOLD_GROUP_NAME,
)
