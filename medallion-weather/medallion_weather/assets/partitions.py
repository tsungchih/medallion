from dagster import HourlyPartitionsDefinition

hourly_partitions_def = HourlyPartitionsDefinition(
    start_date="2022-11-19-00:00", timezone="Asia/Taipei"
)
