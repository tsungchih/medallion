from dagster import AssetKey, HourlyPartitionsDefinition, SourceAsset

hourly_partitions_def = HourlyPartitionsDefinition(
    start_date="2022-11-19-00:00", timezone="Asia/Taipei"
)

medallion_air_aqi_with_pm_asset = SourceAsset(
    key=AssetKey(["GCP", "gold_aqi_with_pm_asset"]),
    description="Source asset originating from `medallion-air` repository.",
    io_manager_key="gcs_io_manager",
    partitions_def=hourly_partitions_def,
)
