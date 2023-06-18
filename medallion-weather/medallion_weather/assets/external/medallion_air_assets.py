from dagster import AssetKey, SourceAsset

from medallion_weather.assets.partitions import hourly_partitions_def

medallion_air_aqi_with_pm_asset = SourceAsset(
    key=AssetKey(["GCP", "gold_aqi_with_pm_asset"]),
    description="Source asset originating from `medallion-air` repository.",
    io_manager_key="gcs_io_manager",
    partitions_def=hourly_partitions_def,
)
