from dagster import HourlyPartitionsDefinition

hourly_partitions_def = HourlyPartitionsDefinition(
    start_date="2023-03-01-00:00", timezone="Asia/Taipei"
)
